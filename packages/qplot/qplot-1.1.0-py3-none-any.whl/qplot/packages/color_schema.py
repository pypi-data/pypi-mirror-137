def Comp_Style(line_size_default,size_default,small):
    custom = {
        "BorderPoints": {"color": "m", "marker": "o", "size": 20},
        "Compressors": {"color": "r", "marker": "o", "size": 20},
        "Compressors_Lines": {
            "color": "r",
            "marker": "u",
            "size": 4 * line_size_default,
        },
        "SeaMarkers": {"color": "m", "marker": "u", "size": 2 * line_size_default},
        "Markers": {"color": "y", "marker": "P", "size": size_default},
        "ConnectionPoints": {"color": "g", "marker": "+", "size": size_default},
        "Consumers": {"color": "y", "marker": "P", "size": size_default},
        "EntryPoints": {"color": "y", "marker": "d", "size": 45},
        "InterConnectionPoints": {"color": "w", "marker": "o", "size": 25},
        "LNGs": {"color": "b", "marker": "v", "size": 38},
        "Nodes": {"color": "k", "marker": ".", "size": 20},  # used to be a value of 10
        "PipeLines": {"color": "steelblue", "marker": "u", "size": line_size_default},
        "PipeLines2": {"color": "g", "marker": "u", "size": line_size_default},
        "PipeLines3": {"color": "b", "marker": "u", "size": line_size_default},
        "PipePoints": {"color": "c", "marker": "P", "size": line_size_default},
        "PipeSegments": {
            "color": "steelblue",
            "marker": "D",
            "size": line_size_default,
        },
        "Processes": {"color": "k", "marker": "s", "size": size_default},
        "PowerPlants": {"color": "w", "marker": "^", "size": size_default},
        "Productions": {"color": "w", "marker": "*", "size": size_default},
        "Storages": {"color": "g", "marker": "^", "size": small},
    }

    return custom
