# Source Governance Matrix

| Tier | Source | Best use | Standalone auto update allowed | Access policy |
|---|---|---|---|---|
| A | CMS NPPES files and NPI Registry | NPI identity, taxonomy, deactivation, other names, non primary locations | No | Public CMS data and API only |
| A | State medical boards | License and professional standing | No | Official board pages or approved APIs only |
| B | Official practice websites | Address, phone, roster, accepting status, website | Only with corroboration for low risk fields | Respect robots, terms, rate limits, and cache snapshots |
| B | Health system directories | Roster, affiliation, location, phone | Only with corroboration for low risk fields | Public pages or approved feeds only |
| B | NUCC taxonomy | Specialty normalization | No | Reference vocabulary only |
| C | Reputable business listings | Discovery hint for phone or address | No | Use as weak evidence only |
| D | Credential gated, blocked, unsupported, or terms incompatible sites | None | Never | Excluded from source registry |

CMS note: NPI issuance does not validate licensure or credentialing. Source: https://download.cms.gov/nppes/NPI_Files.html

NUCC note: taxonomy codes are self selected and do not define scope of licensure. Source: https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40
