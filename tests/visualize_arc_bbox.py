#!/usr/bin/env python3
"""
Visual proof: draws test arcs with their computed bounding boxes.
Generates pr-validation/arc_bbox_visual.png for the PR.
"""
import sys, os, math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bricklayers import GCodeStateBBox, GCodeState


def make_state(x, y):
    return GCodeState(x=x, y=y, z=0, e=0, f=0, retracted=0, width=0,
                      absolute_positioning=True, relative_extrusion=False,
                      is_moving=False, is_extruding=False, is_retracting=False,
                      just_started_extruding=False, just_stopped_extruding=False)


def draw_arc(ax, cx, cy, r, start_deg, end_deg, clockwise, color, label):
    """Draw an arc and its computed bounding box."""
    # Draw the arc curve
    if clockwise:
        if end_deg > start_deg:
            end_deg -= 360
        angles = np.linspace(math.radians(start_deg), math.radians(end_deg), 200)
    else:
        if end_deg < start_deg:
            end_deg += 360
        angles = np.linspace(math.radians(start_deg), math.radians(end_deg), 200)

    xs = cx + r * np.cos(angles)
    ys = cy + r * np.sin(angles)
    ax.plot(xs, ys, color=color, linewidth=2.5, label=label)

    # Start/end points
    sx, sy = cx + r * math.cos(math.radians(start_deg)), cy + r * math.sin(math.radians(start_deg))
    ex, ey = cx + r * math.cos(math.radians(end_deg % 360)), cy + r * math.sin(math.radians(end_deg % 360))
    ax.plot(sx, sy, 'o', color=color, markersize=8)
    ax.plot(ex, ey, 's', color=color, markersize=8)

    # Compute bbox
    i_off = cx - sx
    j_off = cy - sy
    bb = GCodeStateBBox()
    bb.compute_arc(make_state(sx, sy), make_state(ex, ey), i_off, j_off, clockwise=clockwise)

    # Draw bbox
    rect = mpatches.Rectangle((bb.min_x, bb.min_y), bb.max_x - bb.min_x, bb.max_y - bb.min_y,
                                linewidth=1.5, edgecolor=color, facecolor=color, alpha=0.1, linestyle='--')
    ax.add_patch(rect)

    # Draw what endpoint-only bbox would be (wrong)
    wrong_min_x = min(sx, ex) - 0.1
    wrong_max_x = max(sx, ex) + 0.1
    wrong_min_y = min(sy, ey) - 0.1
    wrong_max_y = max(sy, ey) + 0.1
    rect2 = mpatches.Rectangle((wrong_min_x, wrong_min_y),
                                 wrong_max_x - wrong_min_x, wrong_max_y - wrong_min_y,
                                 linewidth=1, edgecolor='red', facecolor='none', linestyle=':')
    ax.add_patch(rect2)


test_cases = [
    {"title": "Quarter CCW (0°→90°)", "cx": 0, "cy": 0, "r": 10, "start": 0, "end": 90, "cw": False},
    {"title": "Semicircle CCW (0°→180°)", "cx": 0, "cy": 0, "r": 10, "start": 0, "end": 180, "cw": False},
    {"title": "Semicircle CW (0°→180°)", "cx": 0, "cy": 0, "r": 10, "start": 0, "end": 180, "cw": True},
    {"title": "270° CCW (0°→270°)", "cx": 0, "cy": 0, "r": 10, "start": 0, "end": 270, "cw": False},
    {"title": "Arc crossing 90° (45°→135°)", "cx": 0, "cy": 0, "r": 10, "start": 45, "end": 135, "cw": False},
    {"title": "Offset center (50,50) r=10", "cx": 50, "cy": 50, "r": 10, "start": 0, "end": 90, "cw": False},
]

fig, axes = plt.subplots(2, 3, figsize=(16, 11))
colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#E91E63', '#00BCD4']

for ax, tc, color in zip(axes.flat, test_cases, colors):
    draw_arc(ax, tc["cx"], tc["cy"], tc["r"], tc["start"], tc["end"], tc["cw"], color, tc["title"])
    ax.set_title(tc["title"], fontsize=11, fontweight='bold')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=tc["cy"], color='gray', linewidth=0.5)
    ax.axvline(x=tc["cx"], color='gray', linewidth=0.5)
    # Add padding
    pad = tc["r"] * 0.3
    ax.set_xlim(tc["cx"] - tc["r"] - pad, tc["cx"] + tc["r"] + pad)
    ax.set_ylim(tc["cy"] - tc["r"] - pad, tc["cy"] + tc["r"] + pad)

fig.suptitle("compute_arc() Bounding Box Validation\n"
             "Colored dashed + shaded = computed bbox (correct)  |  Red dotted = endpoint-only bbox (wrong)",
             fontsize=13, fontweight='bold')
plt.tight_layout()

out_path = os.path.join(os.path.dirname(__file__), "arc_bbox_visual.png")
plt.savefig(out_path, dpi=150, bbox_inches='tight')
print(f"Saved: {out_path}")
