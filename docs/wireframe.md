# AgentDNA — Product Wireframe

## Global shell

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ AgentDNA                         COMMAND CENTER / OVERVIEW  Syncing locally AS │
├───────────────┬──────────────────────────────────────────────────────────────┤
│ ◈ AgentDNA    │                                                              │
│ PERSONAL AI   │                                                              │
│ SWARM         │                                                              │
│               │                                                              │
│ ● EVOLUTION   │                                                              │
│   ONLINE      │                                                              │
│               │                                                              │
│ COMMAND       │                                                              │
│ CENTER        │                                                              │
│ ⌂ Overview    │                                                              │
│ ◈ Population  │                                                              │
│ ⌁ Patterns    │                    MAIN CONTENT                              │
│ ◎ Lineage     │                                                              │
│               │                                                              │
│ CONTROL ROOM  │                                                              │
│ ♢ Privacy     │                                                              │
│ ⚙ Settings    │                                                              │
│               │                                                              │
│ ✓ Data local  │                                                              │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

## Overview

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ GOOD MORNING, ALEX                                      [PAUSE MONITORING]   │
│ Your swarm is getting smarter.                                             │
│ 12 agents are adapting to the way you work.                                │
├─────────────┬─────────────┬─────────────┬────────────────────────────────────┤
│ ACTIVE      │ AVG FITNESS │ TIME RETURN │ GENERATION                          │
│ 12 +3       │ 74 / 100    │ 4.2 hrs     │ 08                                  │
├───────────────────────────────────────┬──────────────────────────────────────┤
│ EVOLUTION TRAJECTORY                  │ EVOLUTION LOG                         │
│ [fitness line chart]                  │ ● Scout-7 graduated                   │
│                                       │ ● New agent spawned                   │
├───────────────────────────────────────┼──────────────────────────────────────┤
│ TOP PERFORMERS                        │ RIGHT NOW                             │
│ Scout-7       92 fitness   ACTIVE     │ Deep work · 42 min                    │
│ Muse-12       84 fitness   ACTIVE     │ VS Code → Chrome · coding mode       │
│ Link-4        78 fitness   ACTIVE     │ [context confidence bar]             │
└───────────────────────────────────────┴──────────────────────────────────────┘
```

## Agent population

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ THE POPULATION                                                               │
│ Every agent earns its place.                                                  │
│ [ALL STATES] [SORT: FITNESS] [SEARCH]                                       │
├────────────────┬────────────────┬─────────────────────────────────────────────┤
│ ◈ Scout-7      │ ◒ Muse-12      │ ↗ Link-4                                   │
│ Shortcut       │ Focus          │ Research                                   │
│ ACTIVE         │ ACTIVE         │ ACTIVE                                     │
│ 92 / 100       │ 84 / 100       │ 78 / 100                                  │
│ [fitness bar]  │ [fitness bar]  │ [fitness bar]                             │
├────────────────┼────────────────┼─────────────────────────────────────────────┤
│ ◷ Nudge-19     │ ✦ Scribe-3     │ ◇ Atlas-2                                 │
│ Nursery        │ Template       │ Workflow                                   │
│ 61 / 100       │ 73 / 100       │ 48 / 100                                  │
└────────────────┴────────────────┴─────────────────────────────────────────────┘
```

## Privacy control room

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ PRIVACY & PERMISSIONS                                                        │
│ ✓ Privacy guard is active                                                    │
│ App names, window titles and timing only.                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│ OBSERVATION CONTROLS                                      [KILL SWITCH READY] │
│ Monitoring enabled                                      [ ON ]               │
│ Clipboard metadata                                      [ OFF ]              │
│ Private mode detection                                  [ ON ]               │
│ Keep activity history                                   [ ON ]               │
├──────────────────────────────────────────────────────────────────────────────┤
│ ALLOWED APPLICATIONS                                      [+ ADD APPLICATION] │
│ Visual Studio Code · Window title + timing                    ALLOWED        │
│ Google Chrome · Window title + timing                          ALLOWED        │
│ Slack · Window title + timing                                  ALLOWED        │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Core user flows

### First run

```text
Welcome → explain data boundary → choose apps → OS permission prompt
        → test observation → set quiet hours → finish
```

### New agent

```text
Pattern discovered → show evidence → user reviews proposal
                   → nursery shadow mode → graduate or retire
```

### Suggestion feedback

```text
Suggestion → Accept / Helpful / Dismiss / Snooze / Stop / Never
           → record response time → update fitness → show rationale
```

### Automation approval

```text
Agent proposes action → show trigger + action + permission level
                      → user approves once / always / never
                      → execute only within declared scope
                      → provide undo
```
