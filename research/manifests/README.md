# Candidate evidence manifests

Each weekly candidate report must have a matching JSON manifest:

```text
research/candidates-YYYY-MM-DD.md
research/manifests/candidates-YYYY-MM-DD.json
```

The manifest is the auditable evidence layer. Markdown is the human-readable analysis.
Run `python scripts/validate_candidate_manifest.py <manifest>` before committing.
