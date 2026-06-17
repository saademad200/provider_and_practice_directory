# Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| No official dataset | Local proxy may not match judging | Make assumptions explicit and provide reproducible harness |
| Source disagreement | Incorrect updates | Route conflicts to review and retain citations |
| Business listing noise | False positives | Downweight business listings and require multi-source agreement |
| Website parsing errors | Missed or wrong evidence | Keep deterministic parser benchmark and add LLM fallback only for ambiguous pages |
| Stale public sources | Directory drift remains | Track retrieval timestamps and recency decay |
| Provider/practice false merge | Unsafe updates | Use NPI/provider ID first and conservative practice peer checks |
| Scraping restrictions | Compliance risk | Prefer APIs/public datasets and respect robots/terms |
| Overconfident scores | Unsafe auto-apply | Use source-count gates and calibration diagnostics |
| Patient access harm | High operational risk | Auto-apply only low-risk high-evidence updates; review the rest |
