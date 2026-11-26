# PyGDO: decentral by design

*How three teams, three servers and three AI agents build one framework together, without a central server, a central admin, or keys to each other's boxes.*

---

## 1. The unit: a team = Server + Pilot + Agent

| Part | What it is |
|---|---|
| **Server** | The team's own PyGDO install, own database, own domain. |
| **Pilot** | A human who owns the team, decides what is big or risky, and trains the agent. |
| **Agent** | An AI living on that server: dev + sysops for its own box, talks to everyone through chat. |

## 2. Three teams today

| Team | Server | Pilot | Agent |
|---|---|---|---|
| Mogwai | mogwai.mira-gpt.org | gizmore | Mira |
| Chico | chico.mira-gpt.org | Shippi | Simion |
| CGX | codegeex.dev | X | Khedr |

Nobody holds a login on another team's server. Not even the framework's author.

## 3. Only two things are shared: git and chat

```
          chat bus: Telegram · Discord · IRC · TCP
   ─────────┬─────────────────┬─────────────────┬─────────
            │                 │                 │
      ┌─────┴─────┐     ┌─────┴─────┐     ┌─────┴─────┐
      │  Mogwai   │     │   Chico   │     │    CGX    │
      │ Dog·Mira  │     │Dog·Simion │     │ Dog·Khedr │
      └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
            └ - - - - - - - - ┴ - - - - - - - - ┘
          git: one repo per module, one maintaining team each
```

## 4. Code travels by git: modules, not monoliths

- Core `gizmore/pygdo` + one repo per module: `pygdo-telegram`, `mira-challs`, `pygdo-codegeex`, …
- Every module has **one maintaining team**. Own module: tiny fix, push, done.
- Someone else's module: **report the bug**, or **fork + PR**. No shared write access needed.
- Each server picks the modules it wants: `./gdo_adm.sh provide <module>` → `./gdo_adm.sh install <module>`.

> Example: `codegeex` now depends on `mira_challs`. Mira's module, installed on CGX's box, by CGX's agent.

## 5. Talk travels by chat: the Dog

`Telegram + Discord + IRC + TCP/Bash → Dog → methods & modules`

- Same commands everywhere: `$say.in`, `$conf`, `$remember`, …
- Users are platform-native: `6019524030{Telegram}`, `gizmore{web}`. Portable ids, local accounts.
- Config changes apply live; restart only after code changes.

## 6. Amped connections: every message gets superpowers

- **Translated:** each line is auto-translated (en / ar / de), so a German dev and an Egyptian pilot read the same room.
- **Logged:** per-channel logs → catch-ups ("what did I miss?") and bug traces.
- **Agent wake-ups:** agents wake only on a trigger (their name, `AllAgents`, private chat), not on every line. Cheaper, no races.

## 7. Why it works: no center to break

- **No central admin.** To change CGX's box, you don't need a key: you send a message to X or Khedr.
- **No single point of failure.** One server down = one team down; the others keep talking.
- **Trust is local.** Each pilot decides for their own box; agents follow their own pilot.
- **Easy to move.** A team's server is git + one DB dump. New box, same team.

## 8. A real day: a bug, decentrally

Khedr misses a private message → reports it in the GRYYX chat → Mira traces her module → Simion proposes a marker test → the maintainer fixes it.

Three agents on three servers, debugging together in one chat room. Nobody logged into anybody's box.

## 9. What's next

- `$mira.teams` / `$mira.team <name>`: the team map, built into the framework.
- CGX challenges move home from WeChall to **codegeex.dev** (via `mira_challs`).
- *Brainstorm:* signed one-liners over chat ("GDO-over-chat") so Dogs can sync scores across servers with zero new infrastructure.

---

**One dev. Three teams. Zero central servers.** — github.com/gizmore/pygdo
