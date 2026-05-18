"""Results reporting subhandler — prints the summary table, saves CSV, and lists failures."""

import csv
import pathlib
from typing import Any


def _print_table(rows: list[dict], param_names: list[str]) -> None:
    if not rows:
        return

    short = [p.lstrip("-").replace("-", "_") for p in param_names]
    param_widths = [max(len(s), 7) for s in short]

    fixed_cols = [
        ("run",    5),
        ("edges",  6),
        ("ticks",  7),
        ("conv",   4),
        ("final_T",9),
        ("spread", 8),
        ("deg",    5),
    ]

    header = "  ".join(
        f"{s:<{w}}" for s, w in zip(short, param_widths)
    ) + "  " + "  ".join(
        f"{name:>{w}}" for name, w in fixed_cols
    )
    sep = "-" * len(header)

    print(sep)
    print(header)
    print(sep)
    for r in rows:
        s = r["stats"]
        param_part = "  ".join(
            f"{r['params'][p]:<{w}}" for p, w in zip(param_names, param_widths)
        )
        fixed_part = "  ".join([
            f"{r['run_id']:>{fixed_cols[0][1]}}",
            f"{s['edges']:>{fixed_cols[1][1]}}",
            f"{s['ticks']:>{fixed_cols[2][1]}}",
            f"{'Y' if s['converged'] else 'N':>{fixed_cols[3][1]}}",
            f"{s['final_T']:>{fixed_cols[4][1]}.6f}",
            f"{s['spread_mean']:>{fixed_cols[5][1]}.3f}",
            f"{s['deg_mean']:>{fixed_cols[6][1]}.2f}",
        ])
        print(f"{param_part}  {fixed_part}")
    print(sep)


def _save_csv(
    rows: list[dict],
    param_names: list[str],
    out_dir: pathlib.Path,
) -> pathlib.Path:
    csv_path = out_dir / "grid_summary.csv"
    stat_fields = [
        "nodes", "dims", "edges", "ticks", "converged", "final_T",
        "w_min", "w_max", "w_mean", "spread_mean", "spread_max",
        "deg_mean", "deg_max", "elapsed_s",
    ]
    fieldnames = ["run_id", "npz_path"] + param_names + stat_fields

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            row: dict[str, Any] = {
                "run_id":   r["run_id"],
                "npz_path": str(r["npz_path"]),
                "elapsed_s": f"{r['elapsed_s']:.2f}",
            }
            row.update(r["params"])
            row.update(r["stats"])
            writer.writerow(row)
    return csv_path


def report(
    results: list[dict],
    failed: list[int],
    param_names: list[str],
    out_base: pathlib.Path,
    total: int,
    elapsed: float,
) -> None:
    """Print completion summary, result table (capped at 40 rows), CSV path, and failure list."""
    m, s = divmod(int(elapsed), 60)
    print(f"\nCompleted {len(results)}/{total} runs in {m}:{s:02d}")

    if results:
        print()
        display = results if len(results) <= 40 else results[:40]
        _print_table(display, param_names)
        if len(results) > 40:
            print(f"  ... {len(results) - 40} more rows in CSV")

        csv_path = _save_csv(results, param_names, out_base)
        print(f"\nCSV saved: {csv_path}  ({len(results)} rows)")

    if failed:
        print(f"\nFailed run indices: {failed}")

    print()
