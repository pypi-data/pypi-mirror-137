# -*- coding: utf-8 -*-
import ast
from types import FrameType

import numpy as np
import pyccolo as pyc
from pandas.core.base import PandasObject

from dfplanner.plan import Plan


_PRIMITIVE_TYPES = (
    int,
    float,
    np.int32,
    np.int64,
    np.float32,
    np.float64,
)


_TYPES_TO_INSTRUMENT = _PRIMITIVE_TYPES + (
    np.ndarray,
    PandasObject,
    Plan,
)


class NumexprPlanner(pyc.BaseTracer):
    node_id_to_plan = {}

    class DereferencesToPassedValue:
        def __init__(self, val):
            self.val = val

        def __getattr__(self, _):
            return self.val

        def __getitem__(self, _):
            return self.val

    class MaterializesBeforeSubscripting:
        def __init__(self, val, frame):
            self.val = val
            self.frame = frame

        def __getitem__(self, item):
            if isinstance(item, Plan):
                item = item.materialize(self.frame)
            return self.val[item]

    def is_outer_stmt(self, node_or_id):
        node_id = node_or_id if isinstance(node_or_id, int) else id(node_or_id)
        containing_stmt = self.node_id_to_containing_stmt.get(node_id, None)
        parent_stmt = self.parent_node_by_id.get(id(containing_stmt), None)
        while parent_stmt is not None and isinstance(
            parent_stmt, (ast.If, ast.Try, ast.With, ast.AsyncWith)
        ):
            parent_stmt = self.parent_node_by_id.get(id(parent_stmt), None)
        return parent_stmt is None or isinstance(parent_stmt, ast.Module)

    def make_instrumented_op(self, base_func, node, frame):
        def instrumented_op(*args):
            if all(isinstance(arg, _PRIMITIVE_TYPES) for arg in args):
                return base_func(*args)
            if all(isinstance(arg, _TYPES_TO_INSTRUMENT) for arg in args):
                return Plan(node)
            new_args = [
                arg.materialize(frame) if isinstance(arg, Plan) else arg for arg in args
            ]
            return base_func(*new_args)

        return instrumented_op

    @pyc.register_handler((pyc.before_binop, pyc.before_compare), when=is_outer_stmt)
    def handle_operations(self, base_func, node, frame: FrameType, *_, **__):
        return self.make_instrumented_op(base_func, node, frame)

    @pyc.register_raw_handler(
        (
            pyc.after_expr_stmt,
            pyc.after_if_test,
            pyc.after_while_test,
            pyc.after_assign_rhs,
            pyc.after_augassign_rhs,
            pyc.argument,
            pyc.after_return,
            pyc.after_lambda_body,
            pyc.list_elt,
            pyc.tuple_elt,
            pyc.dict_value,
        ),
        when=is_outer_stmt,
    )
    def handle_materialize_contexts(self, ret, _node_id, frame: FrameType, *_, **__):
        if isinstance(ret, Plan):
            ret = ret.materialize(frame)
        return ret

    @pyc.before_attribute_load(when=is_outer_stmt)
    def handle_attribute(self, ret, node, frame, *_, call_context, **__):
        if call_context:
            if isinstance(ret, Plan):
                ret = ret.materialize(frame)
            return ret
        elif isinstance(ret, _TYPES_TO_INSTRUMENT):
            return self.DereferencesToPassedValue(Plan(node))
        else:
            return ret

    @pyc.before_subscript_load(when=is_outer_stmt)
    def handle_before_subscript(self, ret, node, frame, *_, attr_or_subscript, **__):
        if isinstance(ret, _TYPES_TO_INSTRUMENT):
            return self.DereferencesToPassedValue(Plan(node))
        elif isinstance(attr_or_subscript, Plan):
            return self.MaterializesBeforeSubscripting(ret, frame)
        else:
            return ret

    @pyc.after_subscript_load(use_raw_node_id=True, when=is_outer_stmt)
    def handle_before_subscript(self, ret, _node_id, frame, *_, call_context, **__):
        if isinstance(ret, Plan) and call_context:
            ret = ret.materialize(frame)
        return ret

    @pyc.register_raw_handler(pyc.after_call, when=is_outer_stmt)
    def cache_call_result(self, ret, node_id, *_, **__):
        if not isinstance(ret, Plan):
            Plan.node_id_to_materialized_value[node_id] = ret
        return ret

    @pyc.register_handler(pyc.after_subscript_slice, when=is_outer_stmt)
    def cache_slice_result(self, ret, node, *_, **__):
        if not isinstance(ret, Plan):
            Plan.node_id_to_materialized_value[id(node.slice)] = ret
        return ret

    @pyc.after_stmt
    def reset_materialized(self, *_, **__):
        Plan.node_id_to_materialized_value.clear()
