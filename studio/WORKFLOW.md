# Agent Coordination System

A lightweight coordinator pattern for multiple AI agents building software.

## Phases

1. Brief — define what to build, success criteria, references
2. Plan — ADRs, file map, first tasks
3. Slice — create self-contained task cards with ownership and file scope
4. Swarm — agents claim tasks, lock files, work, heartbeat, complete
5. Integrate — resolve branches or manifests, validate coherence
6. Ship — version, tag, release notes

## Slots

- Project = standalone repo or subproject with its own git root
- Studio = workspace that owns multiple projects and shared coordination tools
- Personal System = user’s local artifacts: LM Studio endpoint, key configs, preferred CLIs, shell profile settings

## Rules

- One active flow per project at a time.
- Default to manifest mode unless clean history is requested.
