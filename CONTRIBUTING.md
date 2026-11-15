# Contributing

## Get the resources

In PowerShell, Git Bash or a terminal with Git installed:

```sh
git clone https://github.com/Cybersci2026-AlgonquinTeam2/cybersci2026.git
cd cybersci2026
```

If you cloned the repository before its transfer, update the remote from inside that checkout:

```sh
git remote set-url origin https://github.com/Cybersci2026-AlgonquinTeam2/cybersci2026.git
git remote -v
```

The remote is the GitHub address used for fetches and pushes. Updating it does not change your local files.

## Make a change

1. Start with a clean working tree (`git status`); commit or safely store your own changes before pulling.
2. Run `git switch main` and `git pull --ff-only` to get the latest work without creating an accidental merge.
3. Create a descriptive branch, for example `git switch -c practice/pcap-notes`.
4. Make one coherent change. Link existing curriculum instead of duplicating it.
5. Check relative links, factual claims, attribution and `git diff --check`.
6. Stage only intended files, commit, and push your branch with `git push -u origin practice/pcap-notes`.
7. Open a pull request explaining the change and how you checked it; request a teammate review when practical.

Branch review is a team convention; this guide does not imply GitHub enforces it.

## Practice and evidence

Use issue templates to assign a practice objective or propose a resource correction. Record independent versus assisted attempts honestly. Follow [practice resources](practice-resources/README.md) and existing [run conventions](runs/README.md).

## Publication and event work

This repository is public. Keep active-event files, flags, credentials, private target information and personal contact details in the private competition repository or approved local storage. Confirm organizer publication rules before sharing writeups. Respect external licenses and platforms' solution-sharing policies.

The repository records an organizer reply banning AI at CyberSci. Keep AI-assisted study outside competition and no-AI rehearsals.
