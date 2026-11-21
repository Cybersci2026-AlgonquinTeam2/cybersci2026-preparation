# CyberSci 2026 competition day

Download the [offline field guide](../practice-resources/field-guide/README.md) ahead of time. Check with organizers whether prepared references, including AI-authored notes, are permitted at the event.

Team working area for the November 21, 2026 regional event. Start with the [competition runbook](../operations/competition-day-runbook.md) and [CTF method](../curriculum/modules/01-ctf-method-and-competition-day.md).

## Before the event

- Confirm the venue, arrival time, current rules, target scope, permitted references, internet access and publication restrictions with your school/organizers.
- Assign a coordinator/submission owner and primary/backup coverage for web, network, forensics, crypto and reverse engineering. Fill in [team roles](team-roles.md).
- Rehearse with the network disconnected; verify the laptop, VM, tools, notes and scripts work locally.
- Follow the repository's recorded organizer instruction: no AI tools at CyberSci. Do not include local models, AI agents, MCP services or AI retrieval systems in the competition environment.
- Prepare student ID, power supplies, adapters, water and resumes for interviews.

## During the event

1. Record the organizer-provided scope and rules in a private team location.
2. Triage challenges and assign an owner. Use [the board template](challenge-board.csv) in a private copy.
3. Keep a timestamped hypothesis/evidence log; use [the challenge template](templates/challenge.md).
4. Time-box attempts to 30 minutes, then hand off with the evidence and next test.
5. The submission owner checks the flag format and records the result privately.
6. Stop interacting with targets when the organizers close the event.

## Storage and sharing

This repository is public. Do not commit active-event challenge files, flags, credentials, private target details or team contact information here. The `private/` directory below is ignored for local working copies; Git ignore is an accident-prevention aid, not access control. Use the [private competition repository](https://github.com/Cybersci2026-AlgonquinTeam2/competition-day-2026) for shared live-event work and check organizer publication rules before releasing writeups.

## Official sources

Checked November 15, 2026:

- [CyberSci home](https://cybersci.ca/): regional event date, November 21, 2026.
- [Program](https://cybersci.ca/the-program/): regional CTF and hiring event context.
- [Students](https://cybersci.ca/students/): preparation skills and school-based registration. Some page content is marked October 2024; current organizer instructions take precedence.

The AI restriction comes from the existing repository's recorded organizer reply dated October 15, 2026, not from a newly verified public rules page. Exact venue times and a complete current rulebook remain to be confirmed.
