## Hooks

git runs a hook at a moment of its own, for example before a commit or before a push.

---

## A check before each commit

The hook runs `just check`. If it fails, git refuses the commit.

---

## Install it

Hooks are not cloned. `just install-hook` points git at `hooks/`.

---

## Tests in the hook

A failing test is as good a reason as a broken file.
