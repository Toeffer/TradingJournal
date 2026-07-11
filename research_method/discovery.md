# Stage 1 — Discovery

Goal: produce a broad, auditable pool of possible candidates. Discovery generates
**leads**, not final selections.

## Inputs

- `data/research_snapshot.csv`
- newest US/EU scanner reports
- prior candidate report for continuity
- current public event calendars and primary-source event pages

## Procedure

1. Read the snapshot before using model memory or generic web searches.
2. Build up to the configured preliminary count, including the required European pass.
3. Record the origin of every lead: snapshot, scanner, event calendar, company filing,
   exchange notice, or prior report.
4. Keep a candidate only when there is a plausible dated event within the 42-day
   discovery horizon or a current price/volume anomaly worth verifying.
5. Do not rank candidates yet. Do not write entries, stops, targets, or position sizes.
6. Check broker tradeability before expensive research, especially for IPOs and
   special situations.

## Required discovery record

For each lead capture:

- ticker, company, exchange, currency
- discovery source and timestamp
- possible catalyst and possible date
- snapshot row or market-data source
- reason it might matter now
- obvious early rejection risks

## Failure conditions

Reject at discovery when:

- the instrument is not tradeable through the configured broker;
- liquidity or market-cap constraints clearly fail;
- the event is only an undated theme;
- the only thesis is that price moved;
- the source is a search snippet that cannot be opened;
- the name is outside the configured universe without a documented exception.

Discovery success is breadth with traceability—not a long final shortlist.
