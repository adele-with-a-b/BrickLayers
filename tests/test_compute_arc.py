#!/usr/bin/env python3
"""
Unit tests for GCodeStateBBox.compute_arc()
Validates bounding box computation for G2/G3 arc moves.

Each test creates a known arc geometry and verifies the computed
bounding box matches the expected mathematical result.
"""
import sys, os, math

# Import BrickLayers classes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bricklayers import GCodeStateBBox, GCodeState

TOL = 0.15  # tolerance (bbox adds ±0.1 on first point)


def make_state(x, y):
    """Create a GCodeState with only x,y populated (rest are defaults)."""
    return GCodeState(x=x, y=y, z=0, e=0, f=0, retracted=0, width=0,
                      absolute_positioning=True, relative_extrusion=False,
                      is_moving=False, is_extruding=False, is_retracting=False,
                      just_started_extruding=False, just_stopped_extruding=False)


def check_bbox(name, bb, exp_min_x, exp_max_x, exp_min_y, exp_max_y):
    ok = True
    for label, got, exp in [
        ("min_x", bb.min_x, exp_min_x), ("max_x", bb.max_x, exp_max_x),
        ("min_y", bb.min_y, exp_min_y), ("max_y", bb.max_y, exp_max_y),
    ]:
        if abs(got - exp) > TOL:
            print(f"  FAIL {label}: got {got:.4f}, expected {exp:.4f}")
            ok = False
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    return ok


def test_quarter_circle_ccw():
    """CCW quarter circle: (10,0) -> (0,10), center (0,0), r=10
    Expected bbox: x=[0,10], y=[0,10]"""
    bb = GCodeStateBBox()
    bb.compute_arc(make_state(10, 0), make_state(0, 10), -10, 0, clockwise=False)
    return check_bbox("Quarter circle CCW", bb, 0, 10, 0, 10)


def test_quarter_circle_cw():
    """CW quarter circle: (0,10) -> (10,0), center (0,0), r=10
    Expected bbox: x=[0,10], y=[0,10]"""
    bb = GCodeStateBBox()
    bb.compute_arc(make_state(0, 10), make_state(10, 0), 0, -10, clockwise=True)
    return check_bbox("Quarter circle CW", bb, 0, 10, 0, 10)


def test_semicircle_ccw_top():
    """CCW semicircle: (10,0) -> (-10,0), center (0,0), r=10
    Sweeps through top. Expected bbox: x=[-10,10], y=[0,10]"""
    bb = GCodeStateBBox()
    bb.compute_arc(make_state(10, 0), make_state(-10, 0), -10, 0, clockwise=False)
    return check_bbox("Semicircle CCW (top)", bb, -10, 10, 0, 10)


def test_semicircle_cw_bottom():
    """CW semicircle: (10,0) -> (-10,0), center (0,0), r=10
    Sweeps through bottom. Expected bbox: x=[-10,10], y=[-10,0]"""
    bb = GCodeStateBBox()
    bb.compute_arc(make_state(10, 0), make_state(-10, 0), -10, 0, clockwise=True)
    return check_bbox("Semicircle CW (bottom)", bb, -10, 10, -10, 0)


def test_full_circle_ccw():
    """CCW full circle: (10,0) -> (10,0), center (0,0), r=10
    Expected bbox: x=[-10,10], y=[-10,10]"""
    bb = GCodeStateBBox()
    # Full circle: start == end, I=-10 (center is at origin)
    bb.compute_arc(make_state(10, 0), make_state(10, 0), -10, 0, clockwise=False)
    return check_bbox("Full circle CCW", bb, -10, 10, -10, 10)


def test_270_degree_arc():
    """CCW 270°: (10,0) -> (0,-10), center (0,0), r=10
    Sweeps through top and left. Expected bbox: x=[-10,10], y=[-10,10]"""
    bb = GCodeStateBBox()
    bb.compute_arc(make_state(10, 0), make_state(0, -10), -10, 0, clockwise=False)
    return check_bbox("270° arc CCW", bb, -10, 10, -10, 10)


def test_small_arc_no_cardinal_crossing():
    """Small CCW arc: 30° to 60° on r=10 circle centered at origin.
    Start: (10*cos30, 10*sin30), End: (10*cos60, 10*sin60)
    No cardinal angles crossed. Bbox = just start and end points."""
    s = make_state(10 * math.cos(math.radians(30)), 10 * math.sin(math.radians(30)))
    e = make_state(10 * math.cos(math.radians(60)), 10 * math.sin(math.radians(60)))
    i_off = -s.x  # center at origin
    j_off = -s.y
    bb = GCodeStateBBox()
    bb.compute_arc(s, e, i_off, j_off, clockwise=False)
    return check_bbox("Small arc (no cardinal crossing)", bb,
                       min(s.x, e.x), max(s.x, e.x),
                       min(s.y, e.y), max(s.y, e.y))


def test_arc_crossing_90_degrees():
    """CCW arc from 45° to 135° on r=10 circle. Crosses 90° cardinal.
    Expected: max_y = 10 (the 90° point), not just the endpoints."""
    s = make_state(10 * math.cos(math.radians(45)), 10 * math.sin(math.radians(45)))
    e = make_state(10 * math.cos(math.radians(135)), 10 * math.sin(math.radians(135)))
    i_off = -s.x
    j_off = -s.y
    bb = GCodeStateBBox()
    bb.compute_arc(s, e, i_off, j_off, clockwise=False)
    return check_bbox("Arc crossing 90°", bb,
                       min(s.x, e.x), max(s.x, e.x),
                       min(s.y, e.y), 10.0)


def test_tiny_radius_fallback():
    """Near-zero radius arc should not crash, just use endpoint."""
    bb = GCodeStateBBox()
    bb.compute_arc(make_state(5, 5), make_state(5.001, 5.001), 0.0001, 0.0001, clockwise=False)
    return check_bbox("Tiny radius fallback", bb, 4.9, 5.1, 4.9, 5.1)


def test_offset_center():
    """Arc not centered at origin. Quarter CCW: center at (50,50), r=10.
    Start: (60,50), End: (50,60). Expected bbox: x=[50,60], y=[50,60]"""
    bb = GCodeStateBBox()
    bb.compute_arc(make_state(60, 50), make_state(50, 60), -10, 0, clockwise=False)
    return check_bbox("Offset center quarter arc", bb, 50, 60, 50, 60)


if __name__ == "__main__":
    tests = [
        test_quarter_circle_ccw,
        test_quarter_circle_cw,
        test_semicircle_ccw_top,
        test_semicircle_cw_bottom,
        test_full_circle_ccw,
        test_270_degree_arc,
        test_small_arc_no_cardinal_crossing,
        test_arc_crossing_90_degrees,
        test_tiny_radius_fallback,
        test_offset_center,
    ]
    results = [t() for t in tests]
    passed = sum(results)
    total = len(results)
    print(f"\n{'='*40}")
    print(f"Results: {passed}/{total} passed")
    sys.exit(0 if passed == total else 1)
