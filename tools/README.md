# Planned Tools

Tools will be added as bounded components, each with an allowlist, input/output contract, logs, tests, and an explicit runtime status.

Planned order:

1. laptop-first model router;
2. notes/RAG search;
3. shell-in-container MCP;
4. pcap/tshark analysis;
5. Ghidra headless integration;
6. CTFd client;
7. GDB/pwndbg wrapper.

Prefer a fixed pipeline such as `pcap → tshark facts → candidate streams → model summary → human decision` over an agent with unrestricted shell access.

