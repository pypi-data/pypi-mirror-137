# -*- coding: utf-8 -*-
import pytest

import numpy as np
import pandas as pd
import pyccolo as pyc

from dfplanner.plan import Plan
from dfplanner.tracer import NumexprPlanner


@pytest.fixture(autouse=True)
def reset_plan_counter():
    Plan.reset_counter()


def test_add_two():
    x = np.arange(1, 5)
    y = np.arange(2, 6)
    with NumexprPlanner.instance():
        z = pyc.exec("z = x + y")["z"]
    assert np.all(z == x + y)
    assert Plan.reset_counter() == 1


def test_add_three():
    a = np.arange(1, 5)
    b = np.arange(2, 6)
    c = np.arange(3, 7)
    with NumexprPlanner.instance():
        x = pyc.exec("x = a + b + c")["x"]
    assert np.all(x == a + b + c)
    assert Plan.reset_counter() == 1


def test_method_call():
    df = pd.DataFrame({'x': [1, 2, 3, None, 4]})
    with NumexprPlanner.instance():
        env = pyc.exec(
            """
            df_dropna = df.dropna()
            assert Plan.reset_counter() == 0
            df_x_dropna = df.x.dropna()
            assert Plan.reset_counter() == 1
            df_x_dropna_times_three = df.x.dropna() + df.x.dropna() + df.x.dropna()
            assert Plan.reset_counter() == 4
            """
        )
    assert env["df_dropna"].equals(df.dropna())
    assert env["df_x_dropna"].equals(df.x.dropna())
    assert env["df_x_dropna_times_three"].equals(df.x.dropna() + df.x.dropna() + df.x.dropna())


def test_compare_two():
    x = np.arange(1, 5)
    y = np.arange(2, 6)
    with NumexprPlanner.instance():
        z = pyc.exec("z = x < y")["z"]
    assert np.all(z == (x < y))
    assert Plan.reset_counter() == 1


def test_filter():
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    with NumexprPlanner.instance():
        env = pyc.exec(
            """
            no_loc = df[(df.a.dropna() < 3) & (df.b < 5)]
            assert Plan.reset_counter() == 2
            with_loc = df.loc[(df.a.dropna() < 3) & (df.b < 5)]
            assert Plan.reset_counter() == 2
            """
        )
    assert env["no_loc"].equals(df[(df.a.dropna() < 3) & (df.b < 5)])
    assert env["with_loc"].equals(df.loc[(df.a.dropna() < 3) & (df.b < 5)])
