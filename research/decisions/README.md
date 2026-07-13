# Weekly decision archives

Each `decisions-YYYY-MM-DD.csv` file is an immutable copy of the recommendation reviews
recorded for one research run. A repeated same-day run uses an `-HHMM` suffix. The matching
`.meta.json` records the row count and SHA-256.

Create an archive only after updating and validating:

```bash
python scripts/validate_recommendations.py
python scripts/archive_recommendation_reviews.py --date YYYY-MM-DD
```

Never edit an archived row to make a past recommendation look better. Corrections and
changed opinions belong in a new row in `data/recommendation_reviews.csv`, linked through
`recommendation_id` and the prior/new status fields.
