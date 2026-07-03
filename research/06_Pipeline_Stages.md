# Pipeline Stages — Max Gym (Panamá)

**Source:** `06_Pipeline_Stage_Map.html` (artifacts/)
**Pipeline:** Membership / Subscription Services

---

## Pipeline Visual

```
New Lead → Tour/Visit Scheduled → Prospect → Member Signed → Active Member
                                    ↘                      ↗
                                    Lost/Disqualified
```

## Stages

### Stage 1 — New Lead
- **Probability:** —
- **Entry Criteria:** Inbound DM (WhatsApp, IG), Meta Ad click, Google Business, referral, walk-in
- **Exit Criteria:** Tour booked (calendar event created) → moves to Tour / Visit Scheduled
- **Bot Mapping:** Phase 0 — Intelligent Greeting
- **Tags Added:** `new-lead`, `ia-qualifying`, `source-*`
- **Fields Set:** objetivo_principal, situacion_actual, cuando_empezar, presupuesto, objecion_sucursal, ubicacion_referencia

### Stage 2 — Tour / Visit Scheduled
- **Probability:** 25%
- **Entry Criteria:** Lead completes all qualification steps → accepts tour → calendar booking confirmed
- **Exit Criteria:** Visit completed, lead expresses interest → moves to Prospect
- **Bot Mapping:** Phase 1–5 → STOPBOT_VISITA
- **Tags Added:** `ia-qualified`, `meeting-scheduled`
- **Tags Removed:** `ia-qualifying`
- **Fields Set:** visita_agendada (date), tour_type = "Tour"

### Stage 3 — Prospect
- **Probability:** —
- **Entry Criteria:** Tour / visit completed, lead is interested (human confirmed)
- **Exit Criteria:** Signs agreement + payment → moves to Member Signed
- **Bot Mapping:** Human takes over
- **Tags Added:** `human-handover`
- **Notes:** Sales rep follows up post-visit, presents plans, closes deal

### Stage 4 — Member Signed
- **Probability:** 100% Won
- **Entry Criteria:** Contract signed + first payment received
- **Bot Mapping:** WF 6 triggers celebration + pixel event

### Stage 5 — Active Member
- **Probability:** —
- **Entry Criteria:** Member active for 30+ days
- **Retention Workflows:** WF 11, WF 12, WF 13

### Hidden Stages
| Stage | Tag | Trigger |
|-------|-----|---------|
| Disqualified | `ia-disqualified`, `dq-*` | Bot DQ (TIPO A–F) |
| Lost | `lost` | Human marks as lost |
| Won | `won` | Human marks as won |
