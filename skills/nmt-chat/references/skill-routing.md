# Skill routing

`nmt-chat` is the model-invoked router. Use it when the user has a product,
strategy, or methodology question but the next Skill is not yet clear. It
should route by the user's Job and situation, not by a Consumer-project rule
injection.

| Situation | Skill |
| --- | --- |
| New idea, market, segment, or pivot | `nmt-market-research` |
| Live product, metric change, risks, or growth points | `nmt-diagnose` |
| Existing interview material | `nmt-analyze-interviews` |
| Value proposition or differentiation | `nmt-craft-value-proposition` |
| Build-ready requirements | `nmt-product-requirements` |
| Landing page, ads, or GTM communication | `nmt-craft-go-to-market` |
| Legacy project-local refresh | `nmt-upgrade` |

The producer flow is:

```text
nmt-market-research → nmt-craft-value-proposition
                    → nmt-product-requirements
                    → nmt-craft-go-to-market
```

The Client may add a namespace or invocation marker to a direct Skill name.
The shared source uses the portable Skill name; the Client adapter registry is
the only place for proven invocation differences.
