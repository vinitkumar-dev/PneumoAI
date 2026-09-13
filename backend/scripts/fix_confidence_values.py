"""
One-off maintenance script: normalizes any historical `predictions.confidence`
(and accuracy/precision/recall/f1_score) values that are outside the valid
0-100 percentage range.

Why this is needed
-------------------
An earlier version of the backend multiplied an already-percentage-scaled
confidence value by 100 a second time (see the fixed comment in
response_builder.py), producing rows with confidence values like 9889
instead of 98.89. Averaging several such corrupted rows together with
normal rows is what produced nonsensical dashboard numbers such as
"Mean Confidence Interval: 1639.36%".

The current code clamps every value at write time (see
src/services/prediction_service.py -> clamp_confidence), so this bug can no
longer occur going forward. This script fixes rows that were already
written to the database before that fix existed.

Usage
-----
    cd backend
    python -m scripts.fix_confidence_values          # dry run (reports only)
    python -m scripts.fix_confidence_values --apply   # writes the fix
"""

import sys
import argparse

from app import create_app
from database.db import db
from models.prediction import Prediction

FIELDS = ["confidence", "accuracy", "precision", "recall", "f1_score"]


def normalize(value):
    """
    Best-effort repair for an out-of-range percentage value:
      - If it's > 100 and dividing by 100 lands it back in [0, 100],
        assume it was double-scaled and undo that.
      - Otherwise, just clamp into [0, 100].
    """
    if value is None:
        return value

    value = float(value)

    if value > 100:
        candidate = value / 100
        if 0 <= candidate <= 100:
            return round(candidate, 2)

    return max(0.0, min(100.0, round(value, 2)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write the fixed values (default is a dry run).",
    )
    args = parser.parse_args()

    app = create_app()

    with app.app_context():
        rows = Prediction.query.all()

        fixed_count = 0

        for row in rows:
            changed = False

            for field in FIELDS:
                current = getattr(row, field)
                if current is None:
                    continue

                fixed = normalize(current)

                if fixed != current:
                    print(
                        f"Prediction #{row.id}: {field} "
                        f"{current} -> {fixed}"
                    )
                    if args.apply:
                        setattr(row, field, fixed)
                    changed = True

            if changed:
                fixed_count += 1

        if args.apply:
            db.session.commit()
            print(f"\nFixed {fixed_count} row(s). Changes committed.")
        else:
            print(
                f"\n{fixed_count} row(s) would be fixed. "
                f"Re-run with --apply to write changes."
            )


if __name__ == "__main__":
    sys.exit(main())
