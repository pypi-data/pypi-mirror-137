# -*- coding: utf-8 -*-
import ast
import copy
from types import FrameType
from typing import Any, Dict, Tuple


import pandas as pd


class _NodeMapper(ast.NodeVisitor):
    def __init__(self):
        self.traversal = []

    def __call__(self, node: ast.AST) -> Tuple[ast.AST, Dict[int, ast.AST]]:
        # for some bizarre reason we need to visit once to clear empty nodes apparently
        self.visit(node)
        self.traversal.clear()

        self.visit(node)
        orig_traversal = self.traversal
        self.traversal = []
        node_copy = copy.deepcopy(node)
        self.visit(node_copy)
        copy_traversal = self.traversal
        copy_to_orig_mapping = {}
        for no, nc in zip(orig_traversal, copy_traversal):
            copy_to_orig_mapping[id(nc)] = no
        self.traversal.clear()
        return node_copy, copy_to_orig_mapping

    def visit(self, node):
        self.traversal.append(node)
        for name, field in ast.iter_fields(node):
            if isinstance(field, ast.AST):
                self.visit(field)
            elif isinstance(field, list):
                for inner_node in field:
                    if isinstance(inner_node, ast.AST):
                        self.visit(inner_node)


_NOT_FOUND = object()


class _MaterializedReplacer(ast.NodeTransformer):
    def __init__(self, node_id_to_materialized_value: Dict[int, Any]) -> None:
        self.node_id_to_materialized_value: Dict[
            int, Any
        ] = node_id_to_materialized_value
        self.local_env_extras = {}
        self._node_mapper: _NodeMapper = _NodeMapper()
        self._copy_to_orig_mapping = {}

    def __call__(self, node):
        node_copy, copy_to_orig_mapping = self._node_mapper(node)
        self._copy_to_orig_mapping = copy_to_orig_mapping
        return self.visit(node_copy)

    def generic_visit(self, node: ast.AST) -> ast.AST:
        orig_id = id(self._copy_to_orig_mapping[id(node)])
        materialized = self.node_id_to_materialized_value.get(orig_id, _NOT_FOUND)
        if materialized is _NOT_FOUND:
            return super().generic_visit(node)
        else:
            name = f"_temp_{orig_id}"
            self.local_env_extras[name] = materialized
            ret = ast.Name(name, ast.Load())
            ast.copy_location(ret, node)
            return ret


class Plan:
    node_id_to_materialized_value: Dict[int, Any] = {}
    materialize_replacer = _MaterializedReplacer(node_id_to_materialized_value)
    counter = 0

    @classmethod
    def reset_counter(cls):
        ret = cls.counter
        cls.counter = 0
        return ret

    def __init__(self, node: ast.AST) -> None:
        self.node = node

    def materialize(self, frame: FrameType) -> Any:
        node_id = id(self.node)
        materialized = self.node_id_to_materialized_value.get(node_id, _NOT_FOUND)
        if materialized is not _NOT_FOUND:
            return materialized
        self.__class__.counter += 1
        text = ast.unparse(self.materialize_replacer(self.node))
        ret = pd.eval(
            text,
            engine="numexpr",
            local_dict=frame.f_locals | self.materialize_replacer.local_env_extras,
            global_dict=frame.f_globals,
        )
        self.materialize_replacer.local_env_extras.clear()
        self.node_id_to_materialized_value[node_id] = ret
        return ret
