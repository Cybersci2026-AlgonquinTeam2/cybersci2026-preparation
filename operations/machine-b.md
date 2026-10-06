# Machine B: Training Capacity Box

Machine B is not part of the guaranteed competition-day path.

## Intended uses

- Hashcat on the GTX 1660 Ti.
- Overnight RAG indexing and bulk parsing.
- A slower/stronger model endpoint for training.
- Long-running vulnerable labs in VMware.

## Constraints

- Six GB GPU memory and weekday credential-factory contention from 08:30–16:30.
- Intermittent reachability over Tailscale.
- Windows Server 2022; Linux-only tools belong in a Linux VM unless verified otherwise.
- Docker and WSL2 are not assumed available.

## Security boundary

- Bind services to the Tailscale interface only.
- Require an authentication token and rotate it outside the repository.
- Run shell-capable components in an isolated VM/container with no credential-factory mounts.
- Log every request, command, model, fallback, and result status.
- Treat a shell-enabled agent as untrusted code with the ability to damage its execution environment.

## Required tests before use

1. Verify address and authenticated reachability from the laptop.
2. Stop Machine B and confirm the laptop still functions.
3. Confirm no factory paths are visible to the service.
4. Confirm one-model-at-a-time behavior under GPU contention.
5. Confirm logs preserve remote/fallback provenance.

