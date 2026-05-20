"""Arctic level definitions: 9 stages + final boss."""


BIOMES = [
    "Tundra Dawn",
    "Snow Drift",
    "Frozen Bridges",
    "Blizzard Lane",
    "Ice Cavern",
    "Glacial Teeth",
    "Aurora Shelf",
    "Iceberg Rush",
    "Polar Citadel",
]


def _make_level(idx, title, spawn_y=520):
    base_w = 4600 + idx * 430
    y_base = 610 - min(180, idx * 14)
    x = 0
    platforms = []
    spikes = []
    bounce_pads = []

    platforms.append({"x": 0, "y": y_base + 40, "w": 520, "h": 28})
    x = 560
    step = 0
    while x < base_w - 620:
        width = 120 + (step % 4) * 28
        y = y_base - (step % 5) * 30 + ((step // 3) % 2) * 18
        pd = {"x": x, "y": y, "w": width, "h": 28}

        if step % 7 == 3:
            pd.update({"kind": "moving", "move_range": 70 + (idx % 3) * 24, "move_speed": 1.1 + idx * 0.08, "move_axis": "y" if step % 2 else "x"})
        elif step % 8 == 5:
            pd.update({"kind": "crumble"})

        platforms.append(pd)

        if step % 6 == 2 and idx > 1:
            spikes.append({"x": x + 14, "y": y - 24, "w": 28, "h": 24})
        if step % 11 == 6:
            bounce_pads.append({"x": x + width // 2 - 36, "y": y - 16, "w": 72, "h": 16, "boost": -20 - min(4, idx // 2)})

        x += width + 84 + (step % 3) * 24
        step += 1

    finish_x = base_w - 350
    finish_y = y_base - 210
    platforms.append({"x": finish_x - 130, "y": finish_y + 70, "w": 200, "h": 28})
    platforms.append({"x": finish_x + 60, "y": finish_y + 20, "w": 280, "h": 28, "colour_top": (215, 245, 255), "colour_side": (95, 150, 190)})

    return {
        "title": f"Level {idx} - {title}",
        "biome": title,
        "spawn": (120, spawn_y),
        "level_w": base_w,
        "level_h": 900,
        "kill_y": 860,
        "platforms": platforms,
        "spikes": spikes,
        "bounce_pads": bounce_pads,
        "goal": {"x": finish_x + 220, "y": finish_y - 8, "size": 40},
    }


LEVELS = [
    _make_level(1, BIOMES[0], 540),
    _make_level(2, BIOMES[1], 500),
    _make_level(3, BIOMES[2], 510),
    _make_level(4, BIOMES[3], 480),
    _make_level(5, BIOMES[4], 500),
    _make_level(6, BIOMES[5], 470),
    _make_level(7, BIOMES[6], 500),
    _make_level(8, BIOMES[7], 470),
    _make_level(9, BIOMES[8], 460),
    {
        "title": "Level 10 - Frost Guardian",
        "biome": "Boss Arena",
        "spawn": (180, 520),
        "level_w": 3600,
        "level_h": 900,
        "kill_y": 860,
        "platforms": [
            {"x": 0, "y": 640, "w": 900, "h": 28},
            {"x": 980, "y": 590, "w": 180, "h": 28},
            {"x": 1240, "y": 560, "w": 190, "h": 28},
            {"x": 1520, "y": 535, "w": 190, "h": 28},
            {"x": 1800, "y": 510, "w": 220, "h": 28},
            {"x": 2120, "y": 510, "w": 260, "h": 28, "kind": "moving", "move_range": 100, "move_speed": 1.4, "move_axis": "x"},
            {"x": 2480, "y": 510, "w": 220, "h": 28},
            {"x": 2780, "y": 510, "w": 480, "h": 28, "colour_top": (215, 245, 255), "colour_side": (95, 150, 190)},
        ],
        "spikes": [{"x": 1000, "y": 566, "w": 28, "h": 24}, {"x": 1030, "y": 566, "w": 28, "h": 24}],
        "bounce_pads": [{"x": 1860, "y": 494, "w": 72, "h": 16, "boost": -24}],
        "goal": {"x": 3300, "y": 490, "size": 42},
        "boss": {"x": 2900, "y": 500},
    },
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
