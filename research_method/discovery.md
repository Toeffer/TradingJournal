# Stage 1 — Discovery

Goal: produce a broad, auditable pool of possible new leads after the rolling recommendation
book has been reviewed. Discovery generates leads, not final selections or entries.

## Inputs

- `data/research_snapshot.csv`
- `data/recommendations.csv` and `data/recommendation_reviews.csv`
- candidate reports/manifests from the prior six weeks
- newest US/EU scanner reports
- current public event calendars and primary-source event pages
- optional fresh manual discovery seeds, when explicitly supplied

## Continuity boundary

Discovery starts only after every active recommendation and open position has been reviewed.
Carry-over names are part of the comparison set. A new name must displace or complement an
existing object on evidence and setup quality; novelty earns no priority.

Do not create a duplicate recommendation ID for a ticker/thesis already in the active book.
Reuse the durable object and record what changed.

## Discovery mode

Choose and record one mode before building the new-lead pool:

- `hybrid`: recent scanner observations plus catalyst-first web research;
- `catalyst-first`: primary-source/event-calendar research is the main discovery path;
- `scanner-first`: allowed only when the recent snapshot has enough current rows to meet
  breadth requirements without stale observations.

A missing or expired manual Finviz preflight is normal and must not reduce breadth. Use
`catalyst-first` or `hybrid`; do not treat absent manual seeds as a failed input. Manual seed
membership is a discovery label only and never changes score, evidence quality,
classification, ranking, or weekly action.

## Procedure

1. Read the snapshot and rolling recommendation book before generic web searches.
2. Build up to the configured preliminary count, including the required European pass.
3. Record each lead's origin: snapshot, scanner, event calendar, filing, exchange notice,
   prior report, active recommendation, or optional manual seed.
4. Keep a lead only when there is a plausible dated event inside the 42-day discovery
   horizon or a current anomaly worth verifying.
5. Do not rank or write entries, stops, targets, or position sizes during discovery.
6. Check broker tradeability before expensive research.
7. When scanner breadth is thin, source additional names from issuer IR calendars,
   exchange/regulatory notices, index notices, and reputable event calendars rather than
   padding with stale scanner rows.
8. Record whether each new lead appears stronger, weaker, or complementary to the best
   carry-over recommendations. Final comparison happens only after verification and red
   team.

## Required discovery record

For each lead capture:

- ticker, company, exchange, and currency;
- discovery source and timestamp;
- whether it is new or linked to an existing recommendation ID;
- possible catalyst and date;
- snapshot row or market-data source;
- reason it might matter now;
- obvious early rejection risks;
- optional manual-seed status separately from quantitative data.

## Failure conditions

Reject at discovery when:

- the instrument is not tradeable through the configured broker;
- liquidity or market-cap constraints clearly fail;
- the event is only an undated theme;
- the only thesis is that price moved;
- the source is a search snippet that cannot be opened;
- the name is outside the configured universe without a documented exception;
- it duplicates an active research object without identifying new evidence or a new setup.

Discovery success is breadth with traceability, not a long final shortlist.
