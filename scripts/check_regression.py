#!/usr/bin/env python3
"""Detect performance regressions in Mochi benchmark CSV data.

Compares the latest date's results against historical data using Z-score
and IQR methods. Exits 0 if no regressions, 1 if any are detected.
"""

import argparse
import csv
import math
import sys
from collections import defaultdict


def parse_args():
    p = argparse.ArgumentParser(
        description="Check benchmark CSVs for performance regressions."
    )
    p.add_argument("files", metavar="CSV_FILE", nargs="+", help="CSV files to check")
    p.add_argument(
        "--z-threshold",
        type=float,
        default=3.0,
        help="Z-score threshold for anomaly detection (default: 3.0)",
    )
    p.add_argument(
        "--window",
        type=int,
        default=0,
        help="Use only the last N historical dates (default: all)",
    )
    p.add_argument(
        "--metrics",
        nargs="+",
        default=None,
        help="Override which columns to check",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Require BOTH methods to agree before flagging",
    )
    p.add_argument(
        "--quiet", action="store_true", help="Only print anomalies and summary"
    )
    return p.parse_args()


def read_csv(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def detect_mode(headers):
    """Auto-detect CSV type from headers.

    Returns (metrics, direction, group_cols) where direction is
    'lower' (lower is better, e.g. latency) or 'higher' (higher is better).
    """
    if "med" in headers and "avg" in headers:
        metrics = ["med", "avg"]
        direction = "lower"
        group_cols = [h for h in headers if h not in {
            "date", "iterations", "warmup_iterations", "size",
            "min", "q1", "med", "avg", "q3", "max",
        }]
    elif "MiB/s" in headers:
        metrics = ["MiB/s"]
        direction = "higher"
        group_cols = [h for h in headers if h not in {
            "date", "warmup_seconds", "threads", "total_bytes",
            "seconds", "MiB/s", "align_buffer",
        }]
    else:
        print(f"  WARNING: Cannot auto-detect CSV type from headers: {headers}")
        return None, None, None
    return metrics, direction, group_cols


def group_key(row, group_cols):
    return tuple(row[c] for c in group_cols)


def group_label(group_cols, key):
    return ", ".join(f"{c}={v}" for c, v in zip(group_cols, key))


def mean(values):
    return sum(values) / len(values)


def stdev(values, mu):
    if len(values) < 2:
        return 0.0
    return math.sqrt(sum((v - mu) ** 2 for v in values) / (len(values) - 1))


def quartiles(values):
    """Return (Q1, median, Q3) using the linear interpolation method."""
    s = sorted(values)
    n = len(s)

    def percentile(p):
        k = (n - 1) * p
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return s[f]
        return s[f] * (c - k) + s[c] * (k - f)

    return percentile(0.25), percentile(0.5), percentile(0.75)


def check_file(path, args):
    """Check one CSV file for regressions. Returns number of anomalies."""
    rows = read_csv(path)
    if not rows:
        print(f"Checking: {path}")
        print("  WARNING: Empty CSV file, skipping")
        return 0

    headers = list(rows[0].keys())
    metrics, direction, group_cols = detect_mode(headers)
    if metrics is None:
        return 0

    if args.metrics:
        metrics = args.metrics

    # Separate latest date from historical data
    dates = sorted(set(r["date"] for r in rows))
    if len(dates) < 2:
        print(f"Checking: {path}")
        print("  WARNING: Only one date in file, nothing to compare against")
        return 0

    latest_date = dates[-1]
    historical_dates = set(dates[:-1])

    if args.window and args.window > 0:
        windowed = sorted(historical_dates)[-args.window:]
        historical_dates = set(windowed)

    print(f"Checking: {path} (latest date: {latest_date})")

    # Group rows
    hist_groups = defaultdict(list)
    latest_groups = defaultdict(list)

    for row in rows:
        key = group_key(row, group_cols)
        if row["date"] == latest_date:
            latest_groups[key].append(row)
        elif row["date"] in historical_dates:
            hist_groups[key].append(row)

    # Check for groups present in history but missing in latest
    for key in hist_groups:
        if key not in latest_groups:
            label = group_label(group_cols, key)
            print(f"  WARNING: Group [{label}] present in history but missing on {latest_date}")

    anomalies = 0
    checks = 0

    for key in sorted(latest_groups):
        label = group_label(group_cols, key)
        if not args.quiet:
            print(f"  Group: {label}")

        hist_rows = hist_groups.get(key, [])

        for metric in metrics:
            checks += 1

            # Parse metric values
            try:
                latest_vals = [float(r[metric]) for r in latest_groups[key]]
            except (ValueError, KeyError):
                print(f"    WARNING: Cannot parse metric '{metric}' for group [{label}]")
                continue

            latest_val = mean(latest_vals)

            try:
                hist_vals = [float(r[metric]) for r in hist_rows]
            except (ValueError, KeyError):
                print(f"    WARNING: Cannot parse historical metric '{metric}' for group [{label}]")
                continue

            # Check minimum data points
            n_dates = len(set(r["date"] for r in hist_rows))
            if n_dates < 10:
                if not args.quiet:
                    print(
                        f"    {metric}: {latest_val:.3e} | "
                        f"only {n_dates} historical dates, skipping (need >= 10)"
                    )
                checks -= 1  # don't count this as a check
                continue

            # Compute statistics
            mu = mean(hist_vals)
            sd = stdev(hist_vals, mu)
            q1, med, q3 = quartiles(hist_vals)
            iqr = q3 - q1

            # Z-score check
            z_flag = False
            z_val = None
            if sd > 0:
                z_val = (latest_val - mu) / sd
                if direction == "lower" and z_val > args.z_threshold:
                    z_flag = True
                elif direction == "higher" and z_val < -args.z_threshold:
                    z_flag = True

            # IQR check
            iqr_flag = False
            if iqr > 0:
                iqr_lower = q1 - 1.5 * iqr
                iqr_upper = q3 + 1.5 * iqr
            else:
                # Zero IQR: use ±50% of median as bounds
                iqr_lower = med * 0.5
                iqr_upper = med * 1.5

            if direction == "lower" and latest_val > iqr_upper:
                iqr_flag = True
            elif direction == "higher" and latest_val < iqr_lower:
                iqr_flag = True

            # Determine if this is an anomaly
            if args.strict:
                is_anomaly = z_flag and iqr_flag
            else:
                is_anomaly = z_flag or iqr_flag

            # Build status string
            z_str = f"z={z_val:+.2f}" if z_val is not None else "z=N/A(std=0)"
            status = "REGRESSION" if is_anomaly else "OK"

            if is_anomaly or not args.quiet:
                if is_anomaly:
                    anomalies += 1
                    prefix = "    *** "
                    suffix = " ***"
                else:
                    prefix = "    "
                    suffix = ""
                print(
                    f"{prefix}{metric}: {latest_val:.3e} | "
                    f"mean={mu:.3e} std={sd:.3e} {z_str} "
                    f"IQR=[{iqr_lower:.3e}, {iqr_upper:.3e}] "
                    f"-- {status}{suffix}"
                )
            elif is_anomaly:
                anomalies += 1
                print(
                    f"    *** {metric}: {latest_val:.3e} | "
                    f"mean={mu:.3e} std={sd:.3e} {z_str} "
                    f"IQR=[{iqr_lower:.3e}, {iqr_upper:.3e}] "
                    f"-- REGRESSION ***"
                )

    return anomalies, checks


def main():
    args = parse_args()
    total_anomalies = 0
    total_checks = 0

    for path in args.files:
        result = check_file(path, args)
        if isinstance(result, tuple):
            a, c = result
        else:
            a, c = result, 0
        total_anomalies += a
        total_checks += c
        print()

    if total_anomalies > 0:
        print(f"FAIL: {total_anomalies} anomalies detected across {total_checks} checks")
        sys.exit(1)
    else:
        print(f"PASS: 0 anomalies detected across {total_checks} checks")
        sys.exit(0)


if __name__ == "__main__":
    main()
