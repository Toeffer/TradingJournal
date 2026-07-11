# Stage 2 — Verification

Verification is a hard gate. A final candidate may not rely on a model's recollection,
a search-result snippet, or a source another agent merely summarized.

## Source hierarchy

1. Company investor relations, regulatory filings, exchange notices, prospectuses,
   official index/event calendars, and regulator announcements.
2. Reputable financial news for context and expectations.
3. Structured market-data providers for price, volume, market cap, and history.
4. Blogs, analyst commentary, forums, and social media for leads only.

## Required checks

For every possible Actionable or Early Watch name:

- Open the primary source personally in the synthesizing pass.
- Verify the exact catalyst date and event mechanics.
- Record the source URL, source type, publication date, and access timestamp.
- Verify that the event has not already occurred, moved, or been cancelled.
- Verify price/liquidity data with a dated structured source or the repository snapshot.
- Check intervening earnings, financing, offerings, lockup waivers, and other events.
- For non-US names, verify exchange, currency, local listing versus ADR, and hours.

## Date status

Use exactly one value:

- `verified`: opened primary source states the date or binding window.
- `secondary_only`: reputable secondary source, but no opened primary source.
- `derived`: calculated from terms rather than explicitly stated.
- `unverified`: not sufficiently supported.

Only `verified` may enter the Actionable shortlist or Early Watch list. The other
statuses are Reject until verified.

## Lockups and derived dates

Do not accept “IPO date + N days.” Open the prospectus or underwriting terms and check:

- exact lockup duration and start condition;
- early-release price triggers;
- underwriter waiver rights;
- earnings-related release clauses;
- secondary offerings or registrations that already released shares.

## Evidence manifest

Every material factual claim must map to an entry in the JSON manifest's `evidence`
array. At minimum, each non-rejected candidate needs:

- one primary catalyst source;
- one structured market-data source;
- one source or explicit statement supporting the expectations/priced-in assessment.

When evidence is missing, downgrade the candidate. Do not hide the gap in a long
compliance appendix.
