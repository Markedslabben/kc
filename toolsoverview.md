# Claude Code Tools Overview
## Agents & Skills Quick Reference

**Version**: January 2026 | **Format**: A3 Poster | **Author**: Klaus

---

```
+-----------------------------------------------------------------------------------+
|                              QUICK COMMAND SYNTAX                                  |
+-----------------------------------------------------------------------------------+
|  SKILL:   /namespace:skill-name        Example: /ui:design, /kc:parallel          |
|  AGENT:   Task tool → subagent_type    Example: subagent_type="code-reviewer"     |
+-----------------------------------------------------------------------------------+
```

---

# 1. UI & FRONTEND DESIGN

## Skills (`/ui:*`)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/ui:design` | **Full UI assistant** - all modules | Any frontend work |
| `/ui:colors` | Color palette expert | New projects, theming, accessibility |
| `/ui:responsive` | Responsive layout guidance | Mobile-first, breakpoints |
| `/ui:shadows` | Shadow and depth system | Adding polish, elevation |
| `/ui:shadcn` | shadcn/ui component workflow | React + Tailwind projects |
| `/ui:charts` | Charting library selection | Data visualization needs |

## Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `frontend-architect` | Accessible, performant UIs | Complex frontend architecture |
| `frontend-design:frontend-design` | Production-grade interfaces | High-quality UI generation |

---

# 2. CODE DEVELOPMENT

## Skills (`/sc:*` - SuperClaude)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sc:implement` | Feature implementation | Start any new feature |
| `/sc:design` | System/API design | Architecture planning |
| `/sc:build` | Build and package | Compile, bundle projects |
| `/sc:improve` | Systematic improvements | Code quality, performance |
| `/sc:cleanup` | Dead code removal | Technical debt reduction |
| `/sc:refactor` | Code refactoring | Clean code, reduce debt |
| `/sc:explain` | Code explanation | Learning, documentation |

## Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `python-expert` | Production-ready Python | SOLID, security, performance |
| `backend-architect` | Reliable backend systems | Data integrity, fault tolerance |
| `refactoring-expert` | Systematic refactoring | Clean code principles |
| `learning-guide` | Teach programming | Progressive learning |
| `socratic-mentor` | Socratic method teaching | Discovery-based learning |

---

# 3. CODE ANALYSIS & REVIEW

## Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sc:analyze` | Comprehensive analysis | Security, performance, quality |
| `/code-review:code-review` | Review a PR | Before merging |
| `/pr-review-toolkit:review-pr` | Multi-agent PR review | Thorough PR analysis |

## Agents (`pr-review-toolkit:*`)

| Agent | Purpose | Auto-triggers |
|-------|---------|---------------|
| `code-reviewer` | Style & best practices | After code changes |
| `code-simplifier` | Reduce complexity | Overly complex code |
| `comment-analyzer` | Comment accuracy | Documentation changes |
| `type-design-analyzer` | Type design quality | New types added |
| `silent-failure-hunter` | Find silent failures | Error handling changes |
| `pr-test-analyzer` | Test coverage gaps | PR with new features |

## Feature Development Agents (`feature-dev:*`)

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `code-architect` | Design feature architecture | New feature planning |
| `code-explorer` | Analyze existing features | Understanding codebase |
| `code-reviewer` | Review for bugs/security | Quality assurance |

---

# 4. DEBUGGING & TESTING

## Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sc:test` | Run tests with coverage | Quality reporting |
| `/sc:troubleshoot` | Diagnose issues | Build, deploy, runtime |
| `/test-browser` | Chrome DevTools testing | Visual validation, E2E |
| `/tdd:test-first` | TDD workflow enforcer | Test-driven development |

## Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `kc:parallel-debugger` | **Full debug pipeline** | Complex bugs, hypothesis testing |
| `kc:parallel-tester` | Parallel hypothesis testing | Multiple bug theories |
| `parallel-debugger` | Bug → verified fix | Systematic debugging |
| `parallel-tester` | Test hypotheses in worktrees | Eliminate false theories |
| `quality-engineer` | Comprehensive testing | Edge case detection |
| `root-cause-analyst` | Evidence-based analysis | Complex problem investigation |

---

# 5. DOCUMENTATION

## Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sc:document` | Generate focused docs | APIs, components, features |
| `/sc:index` | Project documentation | Knowledge base generation |
| `/kc:md2docx` | Markdown to Word | Export professional docs |
| `/nivametoden` | Pyramid Principle docs | MECE, SCQA, BLUF reports |
| `/kc-docs` | Python project docs | UML, architecture diagrams |

## Document Skills (`document-skills:*`)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `docx` | Word document generation | Professional documents |
| `pdf` | PDF operations | Merge, analyze PDFs |
| `canvas-design` | Visual design/posters | Artwork, static graphics |
| `brand-guidelines` | Anthropic brand colors | Branded content |
| `algorithmic-art` | Generative art (p5.js) | Creative coding |
| `doc-coauthoring` | Co-authoring workflow | Specs, proposals, decisions |

## Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `technical-writer` | Technical documentation | Audience-focused docs |
| `nivametoden` | Pyramid Principle reports | Hierarchical documents |

---

# 6. DEVOPS & INFRASTRUCTURE

## Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `devops-architect` | Infrastructure automation | Reliability, observability |
| `security-engineer` | Security vulnerabilities | Compliance, best practices |
| `performance-engineer` | Performance optimization | Bottleneck analysis |

## Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/git:deploy-staging` | Deploy to staging | Pre-production testing |

---

# 7. GIT & VERSION CONTROL

## Skills (`git:*` and `commit-commands:*`)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sc:git` | Smart git operations | General git workflow |
| `/git:quick-commit` | Fast commit generation | Quick commits |
| `/git:fix-github-issue` | Fix GitHub issue | Automated issue workflow |
| `/git:setup-worktree` | Setup git worktree | Parallel development |
| `/commit-commands:commit` | Create git commit | Standard commits |
| `/commit-commands:commit-push-pr` | Commit + push + PR | Full PR workflow |
| `/commit-commands:clean_gone` | Clean deleted branches | Branch cleanup |

---

# 8. PLANNING & ARCHITECTURE

## Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sc:brainstorm` | Requirements discovery | Socratic exploration |
| `/sc:estimate` | Development estimates | Task/feature sizing |
| `/sc:workflow` | Implementation workflows | PRD to plan |
| `/sc:task` | Complex task management | Intelligent delegation |
| `/sc:spawn` | Task orchestration | Breakdown and delegate |
| `/sc:reflect` | Task reflection | Validation with Serena |
| `/kc:architecture` | Architecture review | DHH + ParkOptimizer review |

## Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `system-architect` | Scalable architecture | Long-term decisions |
| `requirements-analyst` | Requirements discovery | Ambiguous projects |
| `Plan` | Implementation planning | Step-by-step plans |
| `Explore` | Codebase exploration | Quick file/code search |

---

# 9. PARALLEL EXECUTION

## Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sc:parallel` | Validated parallel execution | Multi-task work |
| `/kc:parallel` | Manual parallel orchestration | Git worktree parallelization |
| `/kc:parallel-orchestrator` | Overhead-aware splitting | >3 files, multi-phase |
| `/parallel` | Analyze for parallel execution | Task splitting |

## Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `kc:parallel-orchestrator` | Git worktree parallelization | Large multi-file work |
| `kc:parallel-debugger` | Full debug pipeline | Complex debugging |

---

# 10. AI & AUTOMATION

## Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/analyze-prompt` | Prompt optimization | Auto-suggests improvements |
| `/kc:analyze-prompt` | Anthropic best practices | Prompt engineering |
| `/kc:chatgpt-proxy` | ChatGPT capabilities | OpenAI model tasks |
| `/kc:gemini-proxy` | Google Gemini | Multimodal tasks |
| `/kc:ai-proxy` | Multiple AI models | Flexible model selection |
| `/kc:ai-proxy-browser` | AI via web interfaces | Browser automation |

## Agent SDK (`agent-sdk-dev:*`)

| Skill/Agent | Purpose | When to Use |
|-------------|---------|-------------|
| `/agent-sdk-dev:new-sdk-app` | Create SDK application | New agent app |
| `agent-sdk-verifier-py` | Verify Python SDK app | After creating/modifying |
| `agent-sdk-verifier-ts` | Verify TypeScript SDK app | After creating/modifying |

---

# 11. SESSION MANAGEMENT

## Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sc:load` | Load session context | Start of session |
| `/sc:save` | Save session context | End of session |
| `/sc:overnight` | Overnight autonomous mode | Long-running tasks |

---

# 12. NORWEGIAN GRANTS

## Skills (`soknad:*`)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/soknad:soknad` | Master grant router | Any Norwegian grant |
| `/soknad:innovasjon` | Innovasjon Norge | Innovation grants |
| `/soknad:skattefunn` | Skattefunn | R&D tax deductions |
| `/soknad:enova` | ENOVA energy | Energy efficiency |
| `/soknad:enova_varmesentral` | ENOVA heat pump | Heat pump support |
| `/soknad:budget` | Budget calculation | Support amounts |
| `/soknad:validate` | Validate application | Check criteria |
| `/soknad:firmaprofil` | Company profiles | Manage profiles |
| `/soknad:status` | Status and deadlines | Track applications |

---

# 13. PLUGIN DEVELOPMENT

## Skills (`plugin-dev:*`)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/plugin-dev:create-plugin` | End-to-end plugin creation | New plugin workflow |
| `/plugin-dev:plugin-structure` | Plugin architecture | Directory layout |
| `/plugin-dev:agent-development` | Create agents | Subagent design |
| `/plugin-dev:command-development` | Create commands | Slash commands |
| `/plugin-dev:skill-development` | Create skills | Skill structure |
| `/plugin-dev:hook-development` | Create hooks | Event-driven automation |
| `/plugin-dev:mcp-integration` | MCP server integration | External services |
| `/plugin-dev:plugin-settings` | Plugin configuration | User settings |

## Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `agent-creator` | Create plugin agents | New agent needed |
| `plugin-validator` | Validate plugin | Before release |
| `skill-reviewer` | Review skills | Quality check |

---

# 14. MISCELLANEOUS

## Hookify (`hookify:*`)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/hookify:hookify` | Create prevention hooks | From conversation analysis |
| `/hookify:configure` | Enable/disable rules | Configure hookify |
| `/hookify:list` | List configured rules | View rules |
| `/hookify:writing-rules` | Rule syntax guidance | Write hook rules |

## Other Skills

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/screenshot` | Get Windows screenshots | Screenshot analysis |
| `/view-mermaid` | View Mermaid diagrams | Diagram visualization |
| `/ralph-wiggum:ralph-loop` | Ralph Wiggum loop | Iterative refinement |
| `/kc:task-velocity-estimator` | Time estimates | Data-driven estimation |
| `/kc:financial-analyst` | Financial analysis | Budgeting, forecasting |

---

# MCP TOOLS QUICK REFERENCE

## Firecrawl (Web Scraping)

| Tool | Purpose |
|------|---------|
| `firecrawl_scrape` | Single page extraction |
| `firecrawl_search` | Web search with extraction |
| `firecrawl_map` | Discover site URLs |
| `firecrawl_crawl` | Multi-page extraction |
| `firecrawl_extract` | Structured data extraction |
| `firecrawl_agent` | Autonomous data gathering |

## Chrome DevTools (Browser)

| Tool | Purpose |
|------|---------|
| `take_snapshot` | Page text snapshot (a11y tree) |
| `take_screenshot` | Visual screenshot |
| `click` / `fill` / `hover` | User interactions |
| `navigate_page` | URL navigation |
| `list_console_messages` | Debug console |
| `list_network_requests` | Network analysis |
| `performance_start_trace` | Performance profiling |

## Memory (Knowledge Graph)

| Tool | Purpose |
|------|---------|
| `create_entities` | Add to knowledge graph |
| `create_relations` | Link entities |
| `search_nodes` | Query knowledge |
| `read_graph` | Full graph view |

## Ref (Documentation)

| Tool | Purpose |
|------|---------|
| `ref_search_documentation` | Search docs |
| `ref_read_url` | Read doc content |

---

# FLAGS QUICK REFERENCE

## Analysis Depth
| Flag | Tokens | Use Case |
|------|--------|----------|
| `--think` | ~4K | Standard analysis |
| `--think-hard` | ~10K | Deep architectural |
| `--ultrathink` | ~32K | Maximum depth |

## Execution Control
| Flag | Purpose |
|------|---------|
| `--parallel` | Enable parallel execution |
| `--parallel --force` | Skip safety checks |
| `--safe-mode` | Maximum validation |
| `--validate` | Pre-execution checks |

## MCP Servers
| Flag | Server |
|------|--------|
| `--ref` | Documentation search |
| `--seq` | Sequential reasoning |
| `--magic` | UI generation |
| `--morph` | Bulk code transforms |
| `--play` | Browser automation |
| `--all-mcp` | Enable all servers |
| `--no-mcp` | Disable all servers |

---

```
+-----------------------------------------------------------------------------------+
|                                 DAILY WORKFLOW                                     |
+-----------------------------------------------------------------------------------+
|  START:     /sc:load                    Load session context                      |
|  FRONTEND:  /ui:design                  Full UI assistant                         |
|  IMPLEMENT: /sc:implement               Feature implementation                    |
|  DEBUG:     /kc:parallel-debugger       Complex bug fixing                        |
|  REVIEW:    /pr-review-toolkit:review-pr  Code review                             |
|  COMMIT:    /git:quick-commit           Fast commits                              |
|  END:       /sc:save                    Save session context                      |
+-----------------------------------------------------------------------------------+
```

---

**File**: `/home/klaus/klauspython/kc/toolsoverview.md`
**Print**: A3 Landscape for best readability
**Update**: Run `/sc:cleanup` periodically to keep current
