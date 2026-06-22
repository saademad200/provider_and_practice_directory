# Cost Model Per 1,000 Records

Assumptions:

- public/bulk source snapshots are cached where possible;
- deterministic parsing runs before LLM fallback;
- manual review is estimated at 2 minutes per reviewed item and `$30/hour` loaded cost;
- cloud services are cloud-agnostic, with AWS services used only as reference examples.

| Scenario | Evidence retrieval | Cloud compute/storage/monitoring | LLM fallback | Manual review | Review items | Total / 1,000 |
|---|---:|---:|---:|---:|---:|---:|
| Low-risk periodic refresh | `$4.50` | `$3.00` | `$1.00` | `$50.00` | `50` | `$58.50` |
| Base production run | `$9.00` | `$6.00` | `$5.00` | `$150.00` | `150` | `$170.00` |
| High-risk backlog cleanup | `$18.00` | `$10.00` | `$15.00` | `$350.00` | `350` | `$393.00` |

The main cost lever is reviewer volume. The system lowers operating cost by avoiding unnecessary paid APIs, unnecessary LLM calls, and unnecessary human review.
