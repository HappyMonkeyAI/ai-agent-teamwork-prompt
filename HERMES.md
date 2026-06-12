# HERMES.md — agent guide for ai-agent-teamwork

## Role

This repo is a coordination layer, not an app. Treat docs and protocols as first-class artifacts.

## Operating rules

- Follow the manifest protocol when the user asks for swarm speed.
- Follow the branch protocol when the user asks for clean merges and reviewable commits.
- Summarize current locks before starting any file work: `status.py`.
- If a merge conflict occurs during branch mode, stop and report; do not silently resolve.

## Expectations

- Doc updates should land in the same change as the protocol or workflow change they reflect.
- ADRs go in `docs/adr/` and should be short and decision-focused.

## Research behavior

- Research notes belong in `research/`, not in `docs/`.
- When reviewing external projects, capture: URL, license, stack, why it matters, what to cherry-pick or avoid.
