# Claude ↔ Codex divergence matrix

Дата аудита: 2026-08-14

## Scope and source of truth

Аудит выполнен только по локальному checkout и покрывает:

- восемь пар SKILL.md: nmt-analyze-interviews, nmt-chat, nmt-craft-go-to-market, nmt-craft-value-proposition, nmt-diagnose, nmt-market-research, nmt-product-requirements, nmt-upgrade;
- PRODUCER-CONTRACT.md и READABILITY-CONTRACT.md;
- все локальные references/glossary.md (четыре пары).

Remote canon, web search и содержимое consumer-проектов для классификации не использовались. Git-операции не выполнялись.

Метод проверки: побайтное сравнение соответствующих файлов, затем построчный diff с проверкой каждого блока и поиск всех client/tool/path pointers. Всего: 14 файлов в каждой ветке (Skills/claude и Skills/codex), 28 файлов в сравнении.

## Classification legend

- **capability incompatibility** — различие в доступном клиентском инструменте, интерактивном протоколе, execution model или install root;
- **invocation spelling** — одна и та же команда/skill с клиентским написанием /nmt-* против $nmt-*;
- **instruction-source pointer** — ссылка на consumer-facing rules source: CLAUDE.md против AGENTS.md;
- **formatting-only drift** — перенос строк YAML, пунктуация, порядок двух эквивалентных пунктов или эквивалентная формулировка без изменения поведения;
- **unintended semantic drift** — потерянное обещание, триггер, критерий, ограничение, маршрут или изменённое правило, которое не требуется клиентской несовместимостью.

## Executive matrix

| Pair | capability incompatibility | invocation spelling | instruction-source pointer | formatting-only drift | unintended semantic drift |
|---|---|---|---|---|---|
| nmt-analyze-interviews | tool names (AskUserQuestion, Agent) and Claude/Codex execution wording | all cross-skill and update-check invocations | CLAUDE.md → AGENTS.md | folded frontmatter and minor prose reflow | frontmatter drops input coverage, success-criteria/priority-order clustering, per-interview feedback, mode details and several triggers |
| nmt-chat | Claude-specific model wording → active model | /nmt-* and /nmt-upgrade references | CLAUDE.md → AGENTS.md | folded frontmatter | frontmatter drops the producer pipeline and “plain language first / methodology terms in parentheses” promise |
| nmt-craft-go-to-market | Claude/Codex execution wording; AskUserQuestion → request_user_input; agent runtime wording | all cross-skill and update-check invocations | CLAUDE.md → AGENTS.md | folded frontmatter, punctuation and equivalent wording | frontmatter weakens/removes timing, web/subagent mode detail and “features as proof, not message” nuance |
| nmt-craft-value-proposition | AskUserQuestion → request_user_input; intake batching and human-gate protocol; Agent runtime wording | all cross-skill and update-check invocations | CLAUDE.md → AGENTS.md | folded frontmatter and equivalent prose | frontmatter drops “distinct from generic Christensen JTBD”, cost-to-build specificity, Deep competitor-mining detail and plain-language promise |
| nmt-diagnose | none beyond client invocation | all routing and update-check invocations | CLAUDE.md → AGENTS.md | frontmatter reflow | frontmatter drops the explicit growth/RAT inventory and route list; Core Job gloss adds “end to end” |
| nmt-market-research | Claude/Codex execution wording; intake batching and AskUserQuestion → request_user_input | all cross-skill and update-check invocations | CLAUDE.md → AGENTS.md | folded frontmatter and removed blank/batching prose | frontmatter drops language adaptation and Quick/Deep detail; Codex intake policy changes batching semantics |
| nmt-product-requirements | Claude/Codex execution wording; AskUserQuestion → request_user_input | all routing and update-check invocations, plus one broken mixed pointer | CLAUDE.md → AGENTS.md | folded frontmatter | frontmatter drops the ~90% edge-case promise and Deep parity detail; S0 retains /craft-value- instead of $nmt-craft-value- |
| nmt-upgrade | Codex copy narrows project-root discovery to .agents/skills/ | user-facing /nmt-* → $nmt-* examples | none in body; CLAUDE.md / AGENTS.md order only | reordered client bullets and rule-block paths | .claude/skills/ is omitted from the locate-root instruction |

The matrix is not a claim that every changed line is equally risky. A changed invocation token is expected adapter work; frontmatter omissions and the mixed PRD pointer are semantic defects.

## Pair-by-pair audit

### 1. nmt-analyze-interviews

Sources: Skills/claude/nmt-analyze-interviews/SKILL.md:3-25, :35-49, :94-126, :158-191, :337-393; Skills/codex/nmt-analyze-interviews/SKILL.md:3-24, :28-49, :83-115, :147-180, :326-382.

- **capability incompatibility:** Claude’s Agent/subagent_type/background fan-out is replaced by “Codex’s available execution”, with a sequential fallback. AskUserQuestion becomes request_user_input, including language-choice and business-task calls. “One Claude synthesizes” becomes “one Codex agent synthesizes.”
- **invocation spelling:** routing, hand-off, “what this skill does not do”, and the end-of-run updater use $nmt-* in Codex where Claude uses /nmt-*.
- **instruction-source pointer:** output-file and methodology references use AGENTS.md in Codex where Claude points to CLAUDE.md.
- **formatting-only drift:** the long one-line YAML description is rewritten as a folded block; remaining equivalent prose is rewrapped.
- **unintended semantic drift:** the Codex frontmatter no longer states that clustering uses similar success criteria and priority order, that confidence is computed from supporting interviews, or that per-interview feedback/data quality is delivered. It also removes several accepted input types and trigger phrases, plus the explicit Quick/Deep web distinction. The body still contains much of this behavior, so the defect is primarily in discoverability/skill metadata, not a total loss of implementation.

### 2. nmt-chat

Sources: Skills/claude/nmt-chat/SKILL.md:3-13, :27-57, :74-165, :267-300; Skills/codex/nmt-chat/SKILL.md:3-13, :37-57, :84-165, :277-300.

- **capability incompatibility:** “Claude’s general knowledge” is generalized to “the active model’s general knowledge”; this removes a client-specific assumption without changing source hierarchy.
- **invocation spelling:** the empty invocation, proactive hand-off example, producer names, and updater use $nmt-* in Codex.
- **instruction-source pointer:** terminology, links, audience, saved-artifact and disclaimer references switch from CLAUDE.md to AGENTS.md.
- **formatting-only drift:** the frontmatter description is folded into YAML and prose is reflowed.
- **unintended semantic drift:** the Codex frontmatter drops the explicit producer pipeline (market-research → value-proposition → PRD / GTM) and the promise “Plain language first, methodology terms in parentheses.” The body still contains routing and reader-language rules, so this is a metadata-level semantic loss that can affect discovery and expectations.

### 3. nmt-craft-go-to-market

Sources: Skills/claude/nmt-craft-go-to-market/SKILL.md:3-20, :23-95, :115-178, :419-480; Skills/codex/nmt-craft-go-to-market/SKILL.md:3-20, :34-95, :127-178, :431-491.

- **capability incompatibility:** AskUserQuestion is replaced by request_user_input for intake and direction confirmation. Claude’s Agent/background runtime is replaced by Codex’s available execution with a sequential fallback. “One Claude” becomes “one Codex agent.”
- **invocation spelling:** the pipeline, quick-map, intake paths, hand-offs, “does not do” routes, and updater switch from /nmt-* to $nmt-*.
- **instruction-source pointer:** producer-contract, output-file, methodology and quality-check references use AGENTS.md instead of CLAUDE.md.
- **formatting-only drift:** YAML is folded; cross-sell / upsell / retention is re-punctuated as cross-sell/upsell/retention; equivalent route prose is rewrapped.
- **unintended semantic drift:** the Codex frontmatter omits Quick duration, no-internet/Deep web-review detail, and the explicit “features as proof not message” distinction (it retains only “features as proof”). The full body retains the core delivery model, but the public description no longer exposes all promised operating modes and the message constraint.

### 4. nmt-craft-value-proposition

Sources: Skills/claude/nmt-craft-value-proposition/SKILL.md:3-18, :21-68, :87-142, :176-239, :270-431, :604-773; Skills/codex/nmt-craft-value-proposition/SKILL.md:3-19, :21-68, :98-141, :187-239, :280-431, :614-773.

- **capability incompatibility:** Claude’s AskUserQuestion calls become request_user_input or direct chat. Codex adds a client-specific intake sequence: at most three structured questions per call, at most three choices, free text in chat, and direct-chat fallback. The top-two human gate is similarly adapted. Claude’s Agent/background runtime becomes Codex’s available execution with sequential fallback.
- **invocation spelling:** all map, input-path, hand-off, implementation-spec, “next” and updater references use $nmt-* instead of /nmt-*.
- **instruction-source pointer:** CLAUDE.md rule pointers become AGENTS.md pointers in methodology and output checks.
- **formatting-only drift:** folded YAML and small equivalent prose rewrites preserve the stated flow; request_user_input wording itself is counted above as capability adaptation.
- **unintended semantic drift:** the Codex frontmatter removes “distinct from generic Christensen JTBD”, changes cost-to-build to the broader cost, removes explicit Deep “subagents + web competitor mining”, and drops “Plain language.” These omissions alter the public contract even though the detailed body still carries most mechanics and RAT workflow.

### 5. nmt-diagnose

Sources: Skills/claude/nmt-diagnose/SKILL.md:3-20, :26-44, :111-227, :260-264; Skills/codex/nmt-diagnose/SKILL.md:3-20, :26-38, :105-221, :254-258.

- **capability incompatibility:** no execution or interactive API substitution occurs beyond the client invocation token; this pair is otherwise the closest structurally.
- **invocation spelling:** routing table, stage guidance, all hand-offs and updater use $nmt-* in Codex.
- **instruction-source pointer:** CLAUDE.md becomes AGENTS.md in terminology and audience pointers.
- **formatting-only drift:** the Codex frontmatter is folded and rephrased line-wise.
- **unintended semantic drift:** the Codex frontmatter removes the explicit inventory of weak profit-chain nodes, growth moves (Previous/Next Job, level climb, adjacent Small Jobs, kill-a-Job and chain repair), RAT risks, and exact downstream skill list. Those capabilities still appear in the body, so the observed risk is metadata discoverability. Separately, the Core Job gloss adds “end to end” (Skills/codex/nmt-diagnose/SKILL.md:220 versus Skills/claude/nmt-diagnose/SKILL.md:226); that is a stronger criterion, not a client requirement.

### 6. nmt-market-research

Sources: Skills/claude/nmt-market-research/SKILL.md:3-13, :25-85, :112-188, :231-246, :487-738; Skills/codex/nmt-market-research/SKILL.md:3-13, :35-95, :123-188, :240-255, :497-747.

- **capability incompatibility:** “one Claude”/“one Codex” and agent execution wording are adapted. AskUserQuestion becomes request_user_input. Codex adds an intake-compatibility paragraph (Skills/codex/nmt-market-research/SKILL.md:129) that limits structured calls to 1–3 questions and 2–3 choices, routes free text to chat, and allows sequential calls across logical questions.
- **invocation spelling:** all quick-map, hand-off, value-proposition route and updater references use $nmt-* in Codex.
- **instruction-source pointer:** output, source-link and methodology references switch CLAUDE.md to AGENTS.md.
- **formatting-only drift:** folded frontmatter and removal of the old blank/batching line are partly reflow; equivalent “multi-batch intake” wording is otherwise retained.
- **unintended semantic drift:** the Codex frontmatter no longer promises language adaptation, nor describes Quick as fast/no-internet and Deep as subagents plus web research. More materially, the intake contract is no longer “two batched AskUserQuestion calls, max four each”: Codex permits multiple calls with max three questions/choices. This is an intended tool-capability adaptation, but changes observable batching and must be treated as an adapter contract, not silent source drift. The explicit Step 5 “I don’t have this info” option remains while the new general rule forbids explicit “Other”; this is compatible only if the former is treated as a real answer choice, not generic Other.

### 7. nmt-product-requirements

Sources: Skills/claude/nmt-product-requirements/SKILL.md:3-12, :17-108, :144-227, :251-351, :455-641; Skills/codex/nmt-product-requirements/SKILL.md:3-22, :29-108, :156-231, :263-351, :467-641.

- **capability incompatibility:** AskUserQuestion becomes request_user_input; Claude’s Agent/background runtime becomes Codex’s available execution with sequential fallback. Language, direction-confirmation and batched-intake wording adapt to the Codex interaction contract.
- **invocation spelling:** routing, path choices, hand-off, “does not do” routes and updater use $nmt-* in Codex.
- **instruction-source pointer:** all rule/output/citation pointers switch from CLAUDE.md to AGENTS.md.
- **formatting-only drift:** folded YAML and route/table reflow are formatting-only where text is otherwise equivalent.
- **unintended semantic drift:** the Codex frontmatter drops the ~90% of use cases edge-case promise, explicit “if a better way wins, write the PRD for that” wording, Deep subagent/web parity-check detail, and plain-language promise. More importantly, the flow diagram has a mixed client pointer at Skills/codex/nmt-product-requirements/SKILL.md:190: “to $nmt-market-research → /craft-value-”. The second hop is neither Claude spelling (/nmt-craft-value-proposition) nor Codex spelling ($nmt-craft-value-proposition), so this is a real invocation defect, not harmless reformatting.

### 8. nmt-upgrade

Sources: Skills/claude/nmt-upgrade/SKILL.md:7-58; Skills/codex/nmt-upgrade/SKILL.md:7-58.

- **capability incompatibility:** the Codex copy’s project-root locator says Next-Move-Theory-Canon/ and/or .agents/skills/ (Skills/codex/nmt-upgrade/SKILL.md:39), while Claude’s says .claude/skills/ (Skills/claude/nmt-upgrade/SKILL.md:39). This is an install-root adapter only if the updater is deliberately client-local; it is a semantic defect if the goal is one updater that discovers either installed client.
- **invocation spelling:** trigger and completion examples use $nmt-upgrade, $nmt-diagnose and $nmt-chat in Codex; Claude uses slash invocations.
- **instruction-source pointer:** no client-source substitution occurs in the Codex body. CLAUDE.md / AGENTS.md order is only reordered.
- **formatting-only drift:** .agents/skills and .claude/skills bullets are reordered, as are the rule-block path pair and unrelated-skills pair.
- **unintended semantic drift:** because the Codex locator omits .claude/skills/, a Codex invocation cannot start from a consumer project containing only the Claude installation. The frontmatter also says it refreshes both client trees, so the narrowed locator is internally inconsistent unless the adapter contract explicitly says the active client root is the only valid discovery root.

## Shared contracts

### PRODUCER-CONTRACT.md

Skills/claude/PRODUCER-CONTRACT.md and Skills/codex/PRODUCER-CONTRACT.md share the same base contract. The Codex copy adds Skills/codex/PRODUCER-CONTRACT.md:11-23:

- **capability incompatibility:** request_user_input constraints (1–3 questions, 2–3 choices, recommended-first), direct-chat free-text fallback, no explicit Other, split only across logical questions, fallback when the tool is unavailable, root-agent-only interaction, and equivalent mappings for Read, WebFetch, WebSearch, Write and Agent.
- **instruction-source pointer:** the new section identifies Skills/codex/.agents/skills versus Skills/claude/.claude/skills.
- **invocation spelling:** hand-off examples at Skills/codex/PRODUCER-CONTRACT.md:107,121 use $nmt-* instead of /nmt-*.
- **formatting-only drift:** the orientation sentence changes only the named interaction call from AskUserQuestion to request_user_input (line 35).
- **unintended semantic drift:** none in the added contract if the adapter is intentional. However, it creates a second source of intake truth; it must remain generated/validated against the shared producer contract or future changes can drift.

### READABILITY-CONTRACT.md

Skills/claude/READABILITY-CONTRACT.md and Skills/codex/READABILITY-CONTRACT.md are byte-identical. No divergence to classify.

## References and glossaries

The four existing glossary pairs are byte-identical. Each Claude/Codex pair has SHA-256 414df7118480c0c976ef79f37891ac96e1ad90827e9dbe1f3a2c0c42dd12a2dc:

- nmt-craft-go-to-market/references/glossary.md;
- nmt-craft-value-proposition/references/glossary.md;
- nmt-market-research/references/glossary.md;
- nmt-product-requirements/references/glossary.md.

The other four Skill pairs have no references/glossary.md in either client tree. There are no reference-only differences hidden outside these paths.

## Shared defects surfaced by the local audit

These are not Claude↔Codex divergences because the same defect is present in both copies, but they are directly relevant to frontier issue #5:

1. Both trees contain the same dangling provenance pointer Next-Move-Theory-Canon/Next-Move-Theory/mechanics-catalog.md in nmt-analyze-interviews (Skills/claude/...:172, Skills/codex/...:161). The local replacement-shaped file Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/value-creation-mechanics.md exists.
2. Both trees contain numbered CLAUDE.md/AGENTS.md Rule references, while the shipped local AGENTS.md and installed-rule contract do not expose that numbered rule set. The pointer spelling is client-adapted, but the missing source is shared; changing only one client copy would not fix the underlying defect.

## Conclusion and implementation implication

The current layout is not a safe “two spellings of one source” situation:

- intended adapters are concentrated in invocation spelling, rules-file pointers, interactive tool names, subagent execution wording, Codex intake limits and client install roots;
- the eight frontmatter descriptions also contain independent semantic loss, and nmt-product-requirements contains a concrete mixed invocation typo;
- PRODUCER-CONTRACT.md has a real Codex capability adapter, while READABILITY-CONTRACT.md and all glossaries are already shared-content candidates;
- the two shared dangling-reference defects should be fixed once in the canonical source, not patched independently in Claude and Codex copies.

For migration, the canonical editable source should retain full behavior and metadata. Client adapters should be generated only for the proven items above, with a drift check that fails on any other residual difference—especially frontmatter omissions, altered Job criteria, route changes or mixed / and $ invocations.
