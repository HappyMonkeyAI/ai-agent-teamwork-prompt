# Prompt Log — ai-agent-teamwork session

Collected user prompts and directions from the multi-agent coordination + voice-page-builder session. Intended as bootstrap material for ADRs, CONTEXT.md, and project docs in another project.

## 1. Swarm / Coordination Problem Statement

- "I was thinking just now after working on various projects today that something which I don't do at the moment is have multiple sub agents working on the same project..."
- "what would be more efficient would be the swarm method of building things using different sub agents to leverage bandwidth and capacity to do so at pace"
- "if I was to launch multiple agents with different tasks on a project in the same code base and files locally on my development computer here they would no doubt wind up tripping over each other"
- "perhaps what would be good... is the ability for them to lock files that they are working on and some kind of manifest that could be created in order for them to orchestrate between each other what they are doing"
- "Such a structured approach to it would then mean that even without one of these a fancy orchestration layers... we could still point multiple different AI agents at a directory and have them build features together without them trashing it"

## 2. Test Shape — slice 1, voice-page-builder

- "proceed with testing slice 1 (repo scaffold and editor shell) for voice-page-builder using multiple subagent CLI tools"
- "validate end-to-end workflow and assess build speed vs token usage tradeoffs, with explicit preference for faster build times even if token consumption is higher"
- "ok sounds like a logical test"
- "Let's tighten up those issues then" (after false-completion issue identified)
- "ok so ready to try a bigger build at rapid pace with multiple different cli's acting as agents to build together? (1 task 1 agent tho)?"
- "shouldn't there only have been 1 codex agent 1 task tho? that was the plan not hand 8 tasks to codex"
- "The idea was to have the swarm working together to build at pace, not sequential execution by one agent"

## 3. Preferred Tooling / Models

- "I should use the ones that are most appropriate for the individual tasks that I'm handing off to them but also try to lean towards the ones that are free to use first which is going to be the local model in LM Studio, open code cli, and gemini cli"
- "I think the test here is going to be to have them orchestrate those workers as some agents using our coordination manifest to work together towards the goal of building the project"
- "Lets do it!"
- "Perhaps we could call agent cordination system, sounds better than Rube flow tbh"

## 4. Architecture / Workflow Direction

- "perhaps though we are hitting a missing piece of the puzzle too, if there was a central task list for agents to choose from to work on then there would be no need to orchastrate them at all"
- "everyone could work until they are all done, marking them off, or adding any new tasks as required, or noting blockers etc on them if they are unable to do so"
- "I think you'd likely have to create it from the brief I gave you" (referring to phases, slots, Rube flow / Agent Coordination System)
- "ok so we will stop here for the day then, what I am thinking is one of two things, either we go down the route of no orchastrator, the tasks and manifest rules are created by I open each sub agent and instruct them perhaps via a bootstrap prompt to take a task and begin work working in sequence to build? that or we use mcp servers, I am favouring the first tbh"

## 5. Local Environment / Tooling Known

- LM Studio endpoint: http://192.168.5.232:1234
- Models referenced: qwen3.5-2b-kimi-and-opus-distillation-i1 2B, qwen3.5-9b-deepseek-v4-flash
- CLI tools: opencode, gemini, agy, codex
- Local repos: /home/stephen/Documents/www/php-ai-page-gen/ai-site-builder-v2, /home/stephen/Documents/www/happymonkeyWP

## 6. Project Setup Directives

- "New feature projects placed in /home/stephen/projects/ai-agent-teamwork/projects/<project-name>/"
- "Branch-based coordination preferred for feature work to maintain clean commit history, per ADR-002; manifest mode retained for rapid prototyping"
- Page builder UI: 2-panel (right: voice assistant + toolbox, left: live preview), top control strip (save/publish, versioning, page hierarchy navigation), support for detached floating windows
- WordPress + WP CLI + MCP + docker compose under evaluation as underlying stack

## 7. Explicit Preferences

- Prioritize build speed over token efficiency for coordination validation builds
- Decentralized file-based coordination over centralized orchestration
- Prefer concise, explicit, project-specific docs
- Learns by shipping real end-to-end systems

---

*Generated from session prompts only. No assistant narration included.*
