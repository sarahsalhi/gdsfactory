import io
import pp
from pp.component_from_yaml import component_from_yaml


@pp.autoname
def coupler(wg_width: float = 0.5, gap: float = 0.236, length: float = 10.007):

    pp.drc.assert_on_1nm_grid(length)
    pp.drc.assert_on_2nm_grid(gap)

    netlist = io.StringIO(
        f"""
instances:
    sl:
      component: coupler_symmetric
      settings:
        gap: {gap}
        wg_width: {wg_width}
    sr:
      component: coupler_symmetric
      settings:
        gap: {gap}
        wg_width: {wg_width}
    cs:
      component: coupler_straight
      settings:
        gap: {gap}
        width: {wg_width}
        length: {length}

placements:
    cs:
        x: 0
        y: {gap/2}

connections:
    sl,W0: cs,W0
    sr,W0: cs,E0

ports:
    w0: sl,E0
    w1: sl,E1
    e0: sr,E0
    e1: sr,E1

    """
    )
    return component_from_yaml(netlist)


if __name__ == "__main__":
    c = coupler(pins=True)
    pp.show(c)
