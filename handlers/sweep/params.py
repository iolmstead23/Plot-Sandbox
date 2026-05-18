"""Sweep configuration — edit FIXED and GRID here to control the run matrix."""

# Fixed — applied to every run, never swept.
FIXED: dict[str, str] = {
    "--node-count":  "100",
    "--seed":        "42",
    "--max-ticks":   "10000",
    "--output-dir":  ".output/grid",
}

# Grid — cartesian product of all parameter value lists is the run matrix.
# Comment out any row to hold that parameter at its config.json default.
GRID: dict[str, list | dict] = {
    "--gravity-ratio": {"start": 0.0001, "stop": 0.02,  "steps": 4, "scale": "log"},
    "--repel-ratio":   {"start": 0.0005, "stop": 0.03,  "steps": 4, "scale": "log"},
    "--max-degree":    {"start": 2,      "stop": 16,    "steps": 4, "scale": "linear", "dtype": "int"},
    "--weight-max":    [10, 50, 200],
    "--k-edge":        {"start": 0.05,   "stop": 2.0,   "steps": 3, "scale": "log"},
}
