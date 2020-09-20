#!/usr/bin/env python3
"""upsc-daily-log — track study hours by subject (UPSC prep)."""

from __future__ import print_function
import json, os, sys
from datetime import date

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "study_log.json")


def load():
    if not os.path.isfile(LOG):
        return []
    with open(LOG, "r") as f:
        return json.load(f)


def save(rows):
    with open(LOG, "w") as f:
        json.dump(rows, f, indent=2)


def add(subject, hours, note=""):
    rows = load()
    rows.append({
        "date": date.today().isoformat(),
        "subject": subject.lower(),
        "hours": float(hours),
        "note": note,
    })
    save(rows)
    print("logged %.1fh of %s" % (float(hours), subject))


def summary():
    rows = load()
    if not rows:
        print("no data — the void stares back")
        return
    totals = {}
    for r in rows:
        totals[r["subject"]] = totals.get(r["subject"], 0.0) + r["hours"]
    print("=== lifetime hours ===")
    for k in sorted(totals, key=totals.get, reverse=True):
        print("  %-12s %5.1f" % (k, totals[k]))
    print("  total        %5.1f" % sum(totals.values()))


def today():
    rows = [r for r in load() if r["date"] == date.today().isoformat()]
    if not rows:
        print("nothing logged today. suspicious.")
        return
    s = sum(r["hours"] for r in rows)
    print("today: %.1fh across %d entries" % (s, len(rows)))
    for r in rows:
        print("  - %s %.1fh %s" % (r["subject"], r["hours"], r.get("note") or ""))


def main(argv):
    if not argv:
        print("usage: add SUBJECT HOURS [note...] | summary | today")
        return 1
    if argv[0] == "add" and len(argv) >= 3:
        add(argv[1], argv[2], " ".join(argv[3:]))
    elif argv[0] == "summary":
        summary()
    elif argv[0] == "today":
        today()
    else:
        print("unknown command")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
