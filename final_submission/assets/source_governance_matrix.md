# Source Governance Matrix

| Tier | Source | Best use | Can auto-update from this alone? | Operating note |
|---|---|---|---|---|
| A | CMS NPPES monthly/weekly downloadable files and deactivation data | NPI identity, provider names, taxonomy, practice locations, deactivation signals | No, except low-risk confirmation with corroboration | NPI issuance does not validate licensure or credentialing. |
| A | State medical boards | License status, disciplinary signals, professional standing | No for status changes; review first | State board evidence is the appropriate authority for licensure-sensitive decisions. |
| B | NUCC provider taxonomy | Specialty normalization vocabulary | No | Taxonomy codes are self-selected and do not establish licensure scope. |
| B | Practice and health-system websites | Phone, address, roster, affiliation, website | Only for low-risk fields with corroboration and freshness checks | Useful for current operational details, but roster/affiliation changes remain review-first. |
| B | USPS Publication 28 or conforming address software | Address standardization | Not a source of truth by itself | Improves address quality; does not prove a provider currently practices there. |
| C | Reputable business listings | Phone/address hints only | Never alone | Weak support source; can help prioritize review. |
| D | Blocked, gated, unsupported, or terms-incompatible scraping | None | Never | Excluded from production connectors. |
