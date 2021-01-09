#!/usr/bin/env python3
"""hourglass-habit — log daily study/work hours by subject."""
from __future__ import annotations

import argparse
import csv
import os
from collections import defaultdict
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.environ.get("HOURGLASS_LOG", os.path.join(HERE, "hours.csv"))


def ensure_log() -> None:
    if not os.path.exists(LOG):
        with open(LOG, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["date", "subject", "hours", "note"])


def add(subject: str, hours: float, note: str, day: str | None) -> None:
    ensure_log()
    day = day or date.today().isoformat()
    with open(LOG, "a", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow([day, subject, f"{hours:g}", note])
    print(f"logged {hours:g}h on {subject} ({day})")


def read_rows():
    ensure_log()
    with open(LOG, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def summary() -> None:
    rows = read_rows()
    totals = defaultdict(float)
    for r in rows:
        totals[r["subject"]] += float(r["hours"])
    if not totals:
        print("(no entries)")
        return
    print(f"{'subject':<16} hours")
    for sub, hrs in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"{sub:<16} {hrs:g}")
    print(f"{'TOTAL':<16} {sum(totals.values()):g}")


def today() -> None:
    day = date.today().isoformat()
    rows = [r for r in read_rows() if r["date"] == day]
    if not rows:
        print(f"(nothing logged on {day})")
        return
    total = 0.0
    for r in rows:
        h = float(r["hours"])
        total += h
        note = f" — {r['note']}" if r.get("note") else ""
        print(f"{r['subject']:<16} {h:g}h{note}")
    print(f"{'TOTAL':<16} {total:g}h")


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("subject")
    a.add_argument("hours", type=float)
    a.add_argument("note", nargs="?", default="")
    a.add_argument("--date", dest="day", default=None)
    sub.add_parser("summary")
    sub.add_parser("today")
    args = p.parse_args()
    if args.cmd == "add":
        add(args.subject, args.hours, args.note, args.day)
    elif args.cmd == "summary":
        summary()
    elif args.cmd == "today":
        today()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
