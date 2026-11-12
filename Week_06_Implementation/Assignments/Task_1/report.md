# Task 1 – Cloning Report

**Agent:** Claude Code (VS Code extension)

## How it was done
The agent doesn't have a built-in "clone" feature. It used its **Bash tool**, which runs shell commands on the local machine through the user's installed `git` and the machine's network access:

```bash
cd Week_06_Implementation/Assignments/Task_1
git clone https://github.com/Neltharion59/AI4SE_Playground.git
rm -rf AI4SE_Playground/.git
```

## Mechanism
- **Tool use:** the model decides which command to run, and Claude Code runs it in a shell and returns the output so the agent can check the result.
- **Permissions:** shell commands are subject to Claude Code's permission system. The user approves them, or allows them automatically in auto mode.
- **Removing the inner `.git`:** this turns the clone into ordinary files. Without it, Git would record the folder as an embedded repo (gitlink), and GitHub would show it as an empty folder. The outer repo's `.git` and its `origin` remote were not touched, so pushing still works.
