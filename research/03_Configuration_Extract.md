# Configuration Extract — Max Gym (Panamá)

**Derived from:** Strategy Brief (01) + Conversation Flow v1 (02)
**Target:** GoHighLevel Subaccount Setup

---

## Pipeline Stages

**Pipeline Name:** Membership / Subscription Services

| # | Stage Name | Description | Bot Action |
|---|-----------|-------------|-----------|
| 1 | **New Lead** | Lead inbound via WhatsApp, IG, Meta Ads, Google, or referral | Bot starts: Phase 0 — Intelligent Greeting |
| 2 | **Tour / Visit Scheduled** | Tour booked after qualification | Bot STOPBOT_VISITA → WF 1 |
| 3 | **Prospect** | Visit completed, lead is interested | Human takes over |
| 4 | **Member Signed** | Agreement + first payment completed | WF 6: Celebration + Pixel |
| 5 | **Active Member** | Member active for 30+ days | Retention workflows start |

**Additional hidden/internal stages (tracked via tags + fields):**
| Pseudo-Stage | Tag | When |
|-------------|-----|------|
| Disqualified | `ia-disqualified`, `dq-*` | Bot DQ (TIPO A–F) |
| Cold | `cold` | 14 days inactivity |
| Lost | `lost` | Human marks as lost |
| Won | `won` | Human marks as won |

---

## Custom Fields (19)

### Qualification Fields (from Conversation Flow)

| # | Field Key | Type | Options / Values | Maps to Paso |
|---|-----------|------|-----------------|------------|
| 1 | `objetivo_principal` | Single Select | Ganar músculo / Bajar de peso / Mantenerme activo / Mejorar condición / No estoy seguro | Paso 1 |
| 2 | `situacion_actual` | Single Select | Nunca he ido / Voy actualmente a otro gym / He ido antes pero dejé / Entreno en casa | Paso 2 |
| 3 | `cuando_empezar` | Single Select | Esta semana / La próxima semana / En 2-3 semanas / No estoy seguro | Paso 3 |
| 4 | `presupuesto` | Single Select | Plan Max Rewards B/. 58.85 / Plan Mensual (Max PRO) B/. 69.55 / MAX 360 (B/. 529.65 pago único) / Day Pass $21.40 / No estoy seguro | Paso 4 |
| 5 | `objecion_sucursal` | Text | Free text — single location objection handling | Paso 5 |
| 6 | `ubicacion_referencia` | Text | Free text — zone where lead lives/works | Paso 5 |
| 7 | `visita_agendada` | Date | Date/time of scheduled tour visit | Paso 6 |
| 8 | `tour_type` | Text | "Tour" | Paso 6 |

### System Fields (tracked by bot + workflows)

| # | Field Key | Type | Purpose |
|---|-----------|------|---------|
| 9 | `bot_status` | Text | "Qualifying" / "Meeting Booked" / "Disqualified" / "Deactivated" |
| 10 | `disqualification_reason` | Text | TIPO A–F + description |
| 11 | `disqualification_date` | Date | When DQ occurred |
| 12 | `bot_conversation_summary` | Text Area | Full summary of bot-lead exchange |
| 13 | `bot_actions_summary` | Text Area | Actions bot executed (for debugging) |
| 14 | `loss_reason` | Text | Human-entered loss reason |
| 15 | `pixel_event_sent` | Yes/No | Whether conversion pixel event was sent |

### Revenue Fields

| # | Field Key | Type | Purpose |
|---|-----------|------|---------|
| 16 | `membresia_plan` | Single Select | Plan Mensual (Max PRO) / Max Rewards / MAX 360 (pago único) / Day Pass / Otro |

### Additional Fields

| # | Field Key | Type | Options / Values | Purpose |
|---|-----------|------|-----------------|---------|
| 17 | `edad` | Number | — | Edad del lead — verify ≥ 13 |
| 18 | `tipo_entrenador` | Single Select | Floor trainer (gratis) / Personal trainer (costo extra) / No estoy seguro | — |
| 19 | `tipo_pase` | Single Select | Day Pass $21.40 / Week Pass $32.10 / Single Class $10.70 / Ninguno | — |

---

## Tags (36)

### Source Tags

| Tag | Trigger | Removed By |
|-----|---------|-----------|
| `source-whatsapp` | Lead source | Never |
| `source-instagram` | Lead source | Never |
| `source-facebook-ads` | Lead source | Never |
| `source-google-business` | Lead source | Never |
| `source-referral` | Lead source | Never |
| `source-website` | Lead source | Never |

### Bot Lifecycle Tags

| Tag | When Added | When Removed |
|-----|-----------|-------------|
| `new-lead` | On contact creation | When `ia-qualified` or `ia-disqualified` |
| `ia-qualifying` | Bot starts qualification | When `ia-qualified` or `ia-disqualified` |
| `ia-qualified` | Lead completes all qualification steps | Never |
| `meeting-scheduled` | Tour visit booked (STOPBOT_VISITA) | When `won` |
| `ia-disqualified` | Bot DQ triggered | Never |
| `human-handover` | Bot transfers to human | When `won` or `lost` |
| `stop-bot` | Bot deactivated for contact | Never |

### Profile Tags

| Tag | When Added | Purpose |
|-----|-----------|---------|
| `beginner` | Paso 2 = "Nunca he ido" | Tailored onboarding |
| `currently-member-elsewhere` | Paso 2 = "Voy actualmente a otro gym" | Competitive win-back |
| `lapsed-member` | Paso 2 = "He ido antes pero dejé" | Re-engagement |
| `high-urgency` | Paso 3 = "Esta semana" | Priority follow-up |
| `warm-lead` | Paso 2 = otro gym | Has workout habit |
| `guest-used` | Guest pass used by lead | Track guest visits |
| `les-mills-interest` | Lead expressed interest in Les Mills classes | Targeted outreach |

### Disqualification Tags

| Tag | Condition |
|-----|-----------|
| `dq-budget-too-low` | TIPO A: Presupuesto < $50/mes firmemente |
| `dq-wrong-profile` | TIPO B: Vive/trabaja a >30 min de Costa del Este |
| `dq-no-decision-maker` | TIPO C: Necesita aprobación de pareja y no se da |
| `dq-out-of-range` | TIPO D: Busca algo que Max Gym no ofrece |
| `dq-already-committed` | TIPO E: Ya tiene membresía activa y no quiere cambiar |
| `dq-underage` | TIPO F: Menor de 13 años |

### Disqualification Types (TIPO A–F)

| TIPO | Condition | Bot Message | Tag Applied |
|------|-----------|-------------|-------------|
| A | Presupuesto < $50/mes firmemente | "Entendemos que nuestro precio no se ajusta a tu presupuesto. Si cambias de opinión, estaremos aquí." | `dq-budget-too-low` |
| B | Vive/trabaja a >30 min de Costa del Este | "Actualmente solo tenemos sede en Costa del Este. Si te mudas más cerca, encantados de recibirte." | `dq-wrong-profile` |
| C | Necesita aprobación de pareja y no se da | "Entendemos que es una decisión en pareja. Cuando ambos estén listos, nos encantaría darles un tour." | `dq-no-decision-maker` |
| D | Busca algo que Max Gym no ofrece | "Lamentamos no tener lo que buscas. Te deseamos éxito en tu búsqueda." | `dq-out-of-range` |
| E | Ya tiene membresía activa y no quiere cambiar | "Gracias por tu interés. Si algo cambia, aquí estamos." | `dq-already-committed` |
| F | Under 13 years | "Lo sentimos, la edad mínima para ingresar a Max Gym es 13 años." | `dq-underage` |

### Nurture / Cold Tags

| Tag | When Added | Action |
|-----|-----------|--------|
| `cold` | After 14 days of inactivity (WF 5) | Move to cold stage |
| `nurturing` | Added with `cold` | Start nurture sequence |
| `no-reply` | After 15-day follow-up sequence with no response | Last touch sent |

### Outcome Tags

| Tag | When Added | Action |
|-----|-----------|--------|
| `won` | Stage = Member Signed | WF 6: celebration + pixel |
| `lost` | Stage = Lost (human) | WF 7: handle + nurture |
| `disqualified` | Stage = Lost via DQ | WF 3: secondary DQ handling |

### Retention Tags

| Tag | When Added | Action |
|-----|-----------|--------|
| `onboarding-start` | Member signed | Start onboarding sequence |
| `15-day-checkin` | 15 days after sign-up | WF: check-in message |
| `7-day-no-show` | 7 days without attendance after sign-up | WF: re-engagement |
| `churn-risk` | Flagged by system | Priority human intervention |

---

## Tag-to-Stage Mapping

```
New Lead ─────────────────────────────────────────────────────────────
  Tags: new-lead, ia-qualifying, source-*
  [bot qualification begins]

Tour / Visit Scheduled ───────────────────────────────────────────────
  Tags: ia-qualified, meeting-scheduled
  Tags REMOVED: ia-qualifying
  [bot stops, human takes over after visit]

Prospect ─────────────────────────────────────────────────────────────
  Tags: human-handover
  [human follows up post-visit]

Member Signed ────────────────────────────────────────────────────────
  Tags: won, onboarding-start
  Tags REMOVED: meeting-scheduled, ia-qualified

Active Member ────────────────────────────────────────────────────────
  Tags: 15-day-checkin, 7-day-no-show (as needed)
  [retention workflows]

Lost / Disqualified ──────────────────────────────────────────────────
  Tags: ia-disqualified, dq-*, lost, disqualified
  Tags: stop-bot
```
