"""Level definitions with progressive difficulty and validation."""


def _make_level(idx, title, spawn_y=520):
    base_w = 4600 + idx * 420
    y_base = 600 - min(180, idx * 14)
    x = 0
    platforms = []
    spikes = []
    bounce_pads = []

    platforms.append({"x": 0, "y": y_base + 40, "w": 480, "h": 28})
    x = 520

    step = 0
    while x < base_w - 500:
        width = 120 + (step % 4) * 30
        y = y_base - (step % 5) * 30 + ((step // 3) % 2) * 20
        kind = "static"
        pd = {"x": x, "y": y, "w": width, "h": 28}

        if step % 7 == 3:
            pd.update({"kind": "moving", "move_range": 70 + (idx % 3) * 25, "move_speed": 1.2 + idx * 0.1, "move_axis": "y" if step % 2 else "x"})
        elif step % 8 == 5:
            pd.update({"kind": "crumble"})

        platforms.append(pd)

        if step % 6 == 2 and idx > 1:
            spikes.append({"x": x + 14, "y": y - 24, "w": 28, "h": 24})
        if step % 11 == 6:
            bounce_pads.append({"x": x + width // 2 - 36, "y": y - 16, "w": 72, "h": 16, "boost": -20 - min(4, idx // 2)})

        x += width + 82 + (step % 3) * 24
        step += 1

    finish_x = base_w - 330
    finish_y = y_base - 220
    platforms.append({"x": finish_x - 110, "y": finish_y + 70, "w": 180, "h": 28})
    platforms.append({"x": finish_x + 70, "y": finish_y + 20, "w": 260, "h": 28, "colour_top": (255, 205, 30), "colour_side": (200, 140, 10)})

    return {
        "title": f"Level {idx} - {title}",
        "spawn": (120, spawn_y),
        "level_w": base_w,
        "level_h": 900,
        "kill_y": 860,
        "platforms": platforms,
        "spikes": spikes,
        "bounce_pads": bounce_pads,
        "goal": {"x": finish_x + 210, "y": finish_y - 8, "size": 40},
    }


LEVELS = [
    _make_level(1, "Launch Line", spawn_y=540),
    _make_level(2, "Sky Rhythm", spawn_y=500),
    _make_level(3, "Crumble Drill", spawn_y=510),
    _make_level(4, "Pulse Ramps", spawn_y=480),
    _make_level(5, "Momentum Maze", spawn_y=500),
    _make_level(6, "Precision Run", spawn_y=470),
    _make_level(7, "Flip Flow", spawn_y=500),
    _make_level(8, "Neon Channels", spawn_y=470),
    _make_level(9, "Edge Velocity", spawn_y=460),
    _make_level(10, "Final Reactor", spawn_y=460),
]


def _validate_levels(levels):
    for lvl in levels:
        plats = lvl["platforms"]
        for i in range(len(plats)):
            a = plats[i]
            ax2 = a["x"] + a["w"]
            ay2 = a["y"] + a["h"]
            for j in range(i + 1, len(plats)):
                b = plats[j]
                bx2 = b["x"] + b["w"]
                by2 = b["y"] + b["h"]
                overlap = not (ax2 <= b["x"] or bx2 <= a["x"] or ay2 <= b["y"] or by2 <= a["y"])
                if overlap and abs(a["y"] - b["y"]) < 8:
                    b["x"] = bx2 + 8


_validate_levels(LEVELS)
