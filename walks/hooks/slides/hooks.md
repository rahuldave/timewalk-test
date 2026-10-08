## Hooks

git runs a hook at a moment of its own: before a commit, before a push.

---

## A check before each commit

The hook runs `just check`. If it fails, git refuses the commit.

---

## Install it

Hooks are not cloned. `just setup` points git at `hooks/`.

---

## Tests in the hook

A failing test is as good a reason as a broken file.
