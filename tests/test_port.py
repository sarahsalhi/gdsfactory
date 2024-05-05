from __future__ import annotations

import pytest
from pytest_regressions.data_regression import DataRegressionFixture

import gdsfactory as gf
from gdsfactory.port import csv2port


def test_csv2port(data_regression) -> None:
    name = "straight"
    csvpath = gf.PATH.gdsdir / f"{name}.ports"

    ports = csv2port(csvpath)
    data_regression.check(ports)


def test_get_ports_sort_clockwise() -> None:
    """.. code::

        3   4
        |___|_
    2 -|      |- 5
       |      |
    1 -|______|- 6
        |   |
        8   7

    """
    c = gf.Component()
    nxn = gf.components.nxn(west=2, north=2, east=2, south=2)
    ref = c << nxn
    p = gf.port.get_ports_list(ref, sort_ports=True, clockwise=True)
    gf.port.pprint_ports(p)
    p1 = p[0]
    p8 = p[-1]

    nxn.show()

    assert p1.name == "o1", p1.name
    assert p1.orientation == 180, p1.orientation
    assert p8.name == "o8", p8.name
    assert p8.orientation == 270, p8.orientation


def test_get_ports_sort_counter_clockwise() -> None:
    """.. code::

        4   3
        |___|_
    5 -|      |- 2
       |      |
    6 -|______|- 1
        |   |
        7   8

    """
    c = gf.Component()
    nxn = gf.components.nxn(west=2, north=2, east=2, south=2)
    ref = c << nxn
    p = gf.port.get_ports_list(ref, sort_ports=True, clockwise=False)
    p1 = p[0]
    p8 = p[-1]
    assert p1.name == "o6", p1.name
    assert p1.orientation == 0, p1.orientation
    assert p8.name == "o7", p8.name
    assert p8.orientation == 270, p8.orientation


@pytest.mark.parametrize("port_type", ["electrical", "optical", "placement"])
def test_rename_ports(port_type, data_regression: DataRegressionFixture):
    c = gf.components.nxn(port_type=port_type)
    data_regression.check(c.to_dict())
