# Foresight — Engineering Handoff
### Company: Review Foresight · Product: PubCast AI · UI Shell: Foresight
**Status: design direction, ready to build against. This is the full design intent as
established through extensive discussion — it is not a locked visual spec (no final
color values, exact pixel measurements, or asset files), but every mechanic, rule, and
behavior described here is a real decision, not a suggestion.**

---

## 0. What This Is, Structurally

Three distinct things share the name "Foresight," and keeping them separate matters:

1. **Review Foresight** — the company.
2. **PubCast AI** — the primary program/product, a production-grade virtual production
   platform for solo creators.
3. **Foresight** — this UI itself. It is not just PubCast's shell. It is designed to
   function as a shared hub / operating-system-like layer that multiple different
   programs can dock into and work inside of over time — PubCast today, other programs
   later. Build accordingly: the tray/Counter/carousel system below should not assume
   PubCast is the only thing that will ever open inside it.

There is also **Foresight the Sprite** — same name, the system's living presence (§6).
Meeting her is meeting Foresight.

**What this document extends:** the existing build, `foresight_ui_v18_-16.html`
("Counter / Morphable Tray Workspace"), already contains early collision/deformation
logic (`deformForCollisions`, `collisionVector`, `shapeDeform`, `overlap`) and fan-out
menu logic (`openFan`/`closeFan`). Extend this code, don't discard it. Also referenced:
`2i_writers_room_v3.html` (a separate, related editor build) and `foresight_ui_v19.html`
(a later Counter iteration) — reconcile against whichever of these is most current
before starting.

**Engineering standard for this project (non-negotiable):** production-quality, fully
functional code only. No placeholders, no stub functions, no simulated/fake data, no
TODOs left in delivered code. The only exception is a clearly labeled, mutually agreed
experiment. This product is going to market soon.

**Target hardware constraint:** the primary dev machine ("Zoidberg") runs a GTX 960M
with 2GB VRAM. This is why the technical direction (§7) stays in plain HTML/SVG/CSS/JS
rather than WebGL for this phase — treat it as a real current constraint, not a
permanent architectural rule; revisit if the dev machine changes.

---

## 1. Visual Language: Neo Art Deco Nouveau

Four pillars, all four required — every visual decision gets checked against this list:

- **Great Gatsby opulence and materials** — brass, lacquer, glass, deep jewel tones.
  Richness as a feature, not a flaw. Elsewhere described with a materials list of
  mahogany, turtle shell, oak, leather, and brass, and surface treatments of
  tortoiseshell (amber with dark mottling), leather, and wood specifically at borders
  and seams. Buttons should feel tactile and slightly three-dimensional. Overall palette
  should skew darker and subdued rather than bright white.
- **Star Trek ergonomics** — every ornamented surface is still a real control someone
  uses under pressure. Opulence never obscures function.
- **"We ran out of money before we finished our dream home"** — deliberate imperfection.
  Not every surface is maxed to the same gloss; some areas lavish, some plain or
  exposed. That contrast is what makes a space read as real and lived-in rather than a
  rendered showroom. Uniform polish everywhere is what makes AI-generated interfaces
  feel fake.
- **Noir lighting** — one strong, consistent, dramatic light source with real shadow
  contrast, applied system-wide. This is not just mood — it's the same rule that makes
  the technical shading system work (§4.4). Implement the light angle as a single
  enforced value (a CSS custom property or equivalent) that every shadow and highlight
  gradient reads from — not a convention someone has to remember per-component, or it
  will drift as more trays get built.

**Neo Art Deco Nouveau** is the explicit fusion of art deco's geometry and art
nouveau's organic flow. In this build, that fusion shows up specifically in the
Counter's shape language (§3): smooth rounded edges, shapes that taper to a point
without ever feeling sharp, forms that flow into one another with an aerodynamic
quality rather than hard angles — nouveau's curvature is the operative reference here,
not deco's harder faceting.

**Scope note:** an earlier draft of a related document mistakenly folded in a separate
"Control Room" concept (a hotkey-driven live-broadcast switcher space). That belongs to
the podcast/broadcast side of the product, not this UI. This document is Counter/UI
scope only.

---

## 2. Top-Level Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  🏮[Lantern] ── [Robotic Arm Fixture] ── [Fan Menu →→→]   [Silver   │
│                        │                                  System    │
│                  [ Chat Slot ]                             Bar:     │
│                  (Foresight's perch)                    File/Edit/…│
│                                                                     │
│                                                                     │
│                       THE COUNTER (workspace)                       │
│                    freely-positioned trays here                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Two top-level control regions, explicitly **not** the same thing:

- **The Silver System Bar** — a bar along the top holding traditional dropdown/rollout
  system menus (File, Edit, etc. — conventional application menu behavior). This is the
  ordinary, dependable layer.
- **The Upper-Left Control Anchor** — everything described in §5 (lantern, robotic arm,
  fan, chat slot). This is the custom, living part of the interface.

**Explicitly rejected:** an earlier direction placed a bottom-center "Command Bar" as
the primary input surface. This was overturned. There is no bottom-center command bar.
The Chat Slot (§5.3) lives in the upper-left, under the robotic arm fixture, and is not
a generic search box — it is specifically the conversation log between the user and
Foresight.

---

## 3. The Counter — Core Metaphor

The workspace is called **the Counter**, deliberately avoiding the standard
row-and-column, div/flexbox grid look of ordinary web UI. Mental model: a table set for
a meal — different pieces suited to different roles, arranged the way that actually
makes sense for what's being served, not snapped into a uniform grid of identical
rectangles.

**Important: this is a metaphor for shape variety, not a literal inventory.** The point
being illustrated is "not everything is a square." A short list of illustrative
examples was given early on (a small round bowl, a flat primary surface, a larger
multi-part vessel, two differently-scaled versions of the same kind of item) purely to
demonstrate that range. This is **not**:
- a closed set of exactly four allowed shapes,
- literal dishware/tableware rendering,
- capped at any specific number of shapes or open trays.

New silhouettes should be added freely as new tool roles need them. Every open program,
file, or tool on the Counter is called a **tray** — never a "window," never a "dish."
Trays are positioned freely on the Counter — real absolute positioning, no grid — and
can be dragged, resized, and rearranged.

**Confirmed build priority:** tray *types* should vary visually from one another (a
manuscript tray should not look like a settings panel), but all tray types run on the
same shared underlying tray logic — one tray engine, many silhouettes, not a separate
system per tray type. This is the single most important scoping decision for the build:
get the shared tray engine right once, and visual variation and additional countertops
(§5.4) become comparatively cheap — largely styling plus a handful of animations, not
new systems.

---

## 4. Tray Anatomy & Visual Rules

### 4.1 The two-layer split (load-bearing)

Every tray has two distinct layers:

1. **The safe rectangle** — the inner region that always reliably displays the actual
   content: text, controls, editors, whatever the tray's job is. Ordinary, legible,
   accessible HTML. Content is never sacrificed for the sake of shape.
2. **The frame** — the outer border, where shape and ornament live. Reshapable into an
   irregular polygon, or (simpler, near-term) one of a growing set of named
   silhouettes, with smooth aerodynamic edges per the Counter's material direction.

**Hard rule:** the frame may only bulge *outward* from the safe rectangle — never
inward. Without this, an oddly-shaped or programmatically-generated frame will
eventually clip real content. Enforce this as a real constraint in the tray component,
not a design guideline.

### 4.2 What "3D" means here

Not a literal 3D engine or scene, and trays are not modeled as physical tableware. What
they have is shading and texture — highlight, gradient, and shadow treatment — giving
the *appearance* of weight and depth, so they read as objects sitting on the Counter
rather than flat rectangles floating on a page.

### 4.3 The shadow primitive

CSS `box-shadow` only works cleanly on rectangles — it's why most web UI reads as
stacked flat cards. `filter: drop-shadow()` follows the actual silhouette of whatever
shape is drawn. Use `drop-shadow()`, not `box-shadow`, for tray shapes and irregular
frames.

### 4.4 The noir lighting rule

One consistent light source across every object on the Counter. Mismatched shadow
direction is the fastest way to break the illusion of real objects on a real surface.
Every highlight gradient (glass streak, ceramic matte falloff, metal reflection band)
and every drop-shadow direction/blur obeys the same light angle, decided once,
system-wide (see §1 on implementing this as a single enforced value).

---

## 5. The Upper-Left Control Anchor

This is the persistent, living control cluster — distinct from the ordinary Silver
System Bar (§2).

### 5.1 The components and their stack order

- **The Lantern** — top of the assembly. Foresight's home (see §6).
- **The Robotic Arm Fixture** — the mechanical hinge point below/near the lantern,
  where the Fan Menu extends from. Also serves as the mechanism for jumping between
  entire programs (distinct from the Fan Menu's job, which is tray/tab management —
  see 5.2).
- **The Fan Menu** — extends rightward from the robotic arm fixture, horizontally
  across the top axis (not a vertical dropdown).
- **The Chat Slot** — positioned below the robotic arm fixture, closer to the edge.

### 5.2 The Fan Menu's actual purpose: tray/tab management

This was clarified mid-discussion and is important — the Fan Menu is **not** a generic
navigation menu. It is the open-tray manager. **Each fan blade represents one open
tray** on the current countertop. Clicking a blade brings that tray to prominence,
opens it, or closes it, per the rules in §5.5.

The existing `openFan`/`closeFan` logic in `foresight_ui_v18` is a starting point for
this mechanism, not a finished implementation of it — it needs to be wired to actual
tray state (labels, selection, z-order) per this spec.

### 5.3 The Chat Slot

Not a search bar, not a "command bar." The Chat Slot is the conversation log between
the user and Foresight — literally the user and the system, embodied by the Sprite.

- Collapsed by default: a slim input slot.
- Expandable into a full IM-style conversation history window.
- This is also Foresight's physical perch — see §6.3.

### 5.4 Multi-countertop carousel

For handling more trays than comfortably fit on one countertop:

- Multiple countertops are mounted on a shared central rotating axle/cylinder.
- **All countertops stay flat and parallel to the ground at all times** — they rotate
  around the axle like a Ferris wheel or a Rolodex, they do **not** tilt or flip.
- Only one countertop is visible/active at a time.
- When a countertop gets crowded, the user rotates to a fresh one rather than
  continuing to pile trays onto the same surface.
- Each countertop has its **own color-coded robotic arm and fan**, all emerging from
  the same central hub anchor point (the same physical location described in §5.1,
  just cycling through which arm/fan is currently forward).

### 5.5 The hub interaction model

**Selecting/previewing a countertop:** rotating the hub cycles through the
color-coded arms, bringing a different one to the front for preview. The forward arm's
fan can be expanded to inspect its trays before committing to a switch.

**The single center hub button — a context-dependent toggle, not three separate
controls:**
- If the **currently active** arm's fan is extended → pressing the button retracts/
  closes it.
- If the currently active arm's fan is retracted → pressing the button extends/opens it.
- If a **different** arm (i.e. a different countertop) has been rotated to the front for
  preview → pressing the button instead engages the carousel and rotates that
  countertop into the active position.

One physical button, three contextual behaviors, no separate UI elements needed for
open/close/switch.

**Selecting a fan blade (an individual tray):**
- If the tray is hidden behind others (collision/overlap allowed, see §4 and the
  existing collision toggle) → selecting its blade pops it to the top of the z-index
  stack.
- If the user can't visually locate the tray → selecting its blade makes the tray
  glow/highlight to indicate its position.
- If the tray is closed/stowed → selecting its blade opens it / brings it to prominence.

### 5.6 Blade lifecycle: the "deck of cards" model

- An extended arm with **no open trays** always shows exactly **one blank blade** —
  like the single visible top card of a held deck. This is a persistent baseline state,
  never fully empty.
- Clicking the blank blade opens a file/program picker. The chosen item's name labels
  the new blade. A fresh blank blade appears behind it, ready for the next addition.
  (Opening items is also available via the Silver System Bar's Open command — both
  paths should converge on the same "spawn a labeled tray" logic.)
- As more items open, the fan articulates outward to hold the growing list of labeled
  blades for that countertop.

### 5.7 Closing behavior — two distinct actions with different safety levels

**Closing an individual tray** (low-stakes, reversible-feeling):
- The tray's fan blade detaches from the arm with a subtle unlatch, then **falls off
  the bottom of the screen** under a card-like gravity motion.
- Motion spec: not a light feather flutter, and not a rigid straight/linear drop.
  Closer to a played card slipping and swaying through the air as it falls — some
  air-resistance-style sway/rotation on the way down, gathering speed, exiting past the
  bottom edge. It does not need to "land" anywhere visible — it simply falls off screen.
- Remaining blades on the arm snap inward afterward to close the gap and restore fan
  spacing.

**Closing an entire countertop** (high-stakes, destructive, needs friction):
- **Cannot** be triggered from the hub button or from any individual blade — this is a
  deliberate safety rule to prevent an accidental click from wiping an entire
  countertop's worth of open work.
- Can only be initiated from the Silver System Bar (e.g. File → Close Countertop /
  equivalent).
- Requires a confirmation dialog that explicitly **lists every open item** that will be
  closed as a result, before the user can confirm.

### 5.8 Saving state

- An individual countertop's tray layout/state can be saved on its own.
- Saving one countertop also updates the saved state of the other countertops in the
  overall workspace (i.e. there is one overall saved-workspace state, and per-countertop
  saves feed into it — not fully independent save files per countertop).

---

## 6. Foresight the Sprite

A small, glowing, iridescent presence tied to the lantern. Mental model: Disney's
Tinker Bell — same functional role (recurring visual/brand signature, "the system's
mouse pointer"), not a literal copy. **Her name is Foresight** — confirmed directly; she
carries the product's own name rather than a separate character name. (Note for the
engineer: some earlier working material uses the placeholder name "Sheila" — that was
explicitly stated as a placeholder at the time it was used and is not the real name.
Use Foresight everywhere in implementation, strings, and asset naming.)

### 6.1 Architecture: presence is a swappable layer

Two separate concerns, deliberately decoupled:

- **The assistant** — intelligence, memory, tools, awareness, initiative, actions. This
  layer is constant regardless of how she's shown or heard.
- **The presence layer** — how that intelligence manifests to the user. A swappable
  skin over the same underlying assistant. Discussed possible implementations: a fuller
  diorama/avatar person, a video-call-style person, an ethereal avatar, the
  floating-light sprite described below, voice-only with no visual, or no presence at
  all. Different surfaces of the product could in principle use different presence
  implementations without touching the assistant underneath.

**The current build target is the voice + light combination below** — not a fuller
avatar/diorama mode, which remains a possible future presentation option (§6.6) rather
than the near-term target.

### 6.2 Voice — the primary presence

Voice is the biggest part of how the user actually experiences Foresight as "an
assistant." It's user-selectable — the person picks the voice, which carries
personality, cadence, warmth, humor, or seriousness as they prefer. The voice is the
thing the user comes to know as Foresight, not audio bolted onto a visual character.

### 6.3 The light — home, perch, and activity states

She lives in **the lantern**, and importantly: she is not a separate object the lantern
illuminates — **she is the lantern's light source.** The light never fully turns off,
it only moves and changes:

| State | Location | Light/motion behavior |
|---|---|---|
| Resting / dismissed | Inside the lantern | Lantern keeps glowing, just dimmer — soft, slow, low-key glow. Doesn't light the surrounding area, only itself. Occasional ambient hints (subtle shifts in direction, color, or intensity) signal she's present even at rest. |
| Waiting / on duty | Perched on the Chat Slot | She flies out, flutters briefly, and settles/perches directly on the Chat Slot — her designated landing spot while waiting for input. |
| Active / working | Flying in the workspace | Tight figure-eight flutter motion with a brief, fast-fading sparkle trail. Flicker speed, intensity, and frequency scale continuously with how active/busy she currently is — this is a continuous readout of activity level, not a small fixed set of discrete icons/states. |

Motion and illumination details:
- **Motion**: tight figure-eight, not a wandering or erratic path.
- **Trail**: short-lived, quickly-fading sparkle trail.
- **Illumination**: lights only the immediate area/object she's referencing — never a
  whole paragraph or panel, just the specific point of focus (avoids reading like boxy
  accessibility-style highlighting).
- **Abstraction**: no face, no body required to function — at simplest she can read as
  closer to "a bit of fluttering light" than a rendered character, the way people
  perceive Tinker Bell from a distance without resolving detail.
- **Visibility is optional**: she can hold at a target while the voice explains it, can
  trace a path through steps, or can disappear entirely so the user hears only the
  voice. She does not need to be visually present to be present.
- **Scale**: mouse-pointer size, possibly smaller, deliberately — at normal viewing
  distance she should read as a point of light, not an inspectable character. This
  keeps her from becoming a persistent widget sitting on the interface; she inhabits it
  instead.
- **Adaptive color**: not a fixed color — her emitted light/color should adapt to the
  active theme/background to stay legible without clashing or visually dominating (e.g.
  darker backgrounds warrant a softer/deeper glow; pale backgrounds warrant less raw
  emitted brightness but more saturated color and a halo so she doesn't wash out). The
  hard constraint: always visually legible, never visually dominant.

### 6.4 Functional behavior — the light has real jobs, it isn't decorative

- **Reading cursor (Read Aloud / text-to-speech)**: on trigger, she becomes the
  physical representation of the reading position — flutters word to word at the pace
  of the voice, illuminating only the current word. When reading reaches the bottom of
  the visible area, she leads the viewport downward (text scrolls just enough to keep
  her and the current words in view), then continues. Triggering Read Aloud again makes
  her disappear.
- **Pointing/guidance**: flies to and holds at a UI target (button, menu item,
  document) while the voice explains it — a live "look here" indicator.
- **Path-tracing**: can trace a path through a menu or sequence of steps.
- **Visual audit trail**: when she acts on the user's behalf (e.g. retrieving
  something, navigating somewhere), she visibly travels there rather than returning a
  black-box result — the user can see where she's going before/as it happens. This is a
  trust mechanism, not only a cute touch.

### 6.5 First-run sequence

**Design principle: Foresight becomes a presence before the workspace does.** She
appears during installation itself, not only after setup completes.

```
Download → Unpack → Initialize → ✨ First Glimmer (Sprite)
   → Lantern / Sprite Introduction → Installation / Setup
   → Foresight Logo → Introduction → ✨ Sprite / Foresight
   → First Conversation → Foresight
```

The technical machinery underneath stays completely ordinary (files unpacking,
components initializing, dependencies checking). What changes is what the user sees
layered on top:

- Initially just a tiny glow — a shimmer, a flicker.
- She emerges from the lantern.
- She can unobtrusively accompany the install ("We're getting everything ready."),
  point toward progress, react to major stage completions — without narrating every
  technical operation.
- Installation finishes, interface settles, intro animation and logo play.
- Rather than being introduced as a bolted-on feature afterward, she's already there.
- First spoken line, after light/flutter/settle: **"Hi."** — nothing more. The user has
  already learned, by watching her behave, that light means presence, movement means
  activity, and the lantern means home. Explanation of what she is comes after, not
  before.

### 6.6 Presentation modes beyond the near-term light (future option, not current scope)

If a fuller avatar/diorama presence is ever used for a given surface (per the
presence-layer split in §6.1), a cinematic camera grammar was established so that
presentation reads as staged television blocking, not a UI viewport snapping between
states:

- Camera **tracks** her while she's traveling.
- Camera **locks** when something significant happens (e.g. reaching a door).
- **Framing changes** with state: working = static composition, discovery = camera
  moves in, searching = camera follows her, waiting = ambient shot, return = tracking
  shot back.
- The environment only needs to render the portion the camera can currently perceive —
  an apparently large, detailed world can exist with very little actual geometry,
  because the audience fills in what isn't shown.

Not the current build target. Documented here so it isn't lost, and so the presence
layer (§6.1) is built with this as a plausible future skin rather than something that
would require re-architecting the assistant underneath.

---

## 7. Technical Direction (current thinking, not locked)

Given that "3D" here means shading/weight rather than a literal engine, stay in
**plain HTML/SVG/CSS/JS** for this phase:

- Tray shapes as SVG / `clip-path` geometry.
- `filter: drop-shadow()` for real shape-following shadows (§4.3).
- Layered gradients per material (glass, ceramic, metal, brass, lacquer) under the
  single fixed light source (§1, §4.4).
- Free absolute positioning for the Counter surface, extending the existing
  drag/resize code already in `foresight_ui_v18`.
- Single global light-angle value driving every shadow/highlight calculation (§1).

This keeps the product inside its stated identity — "a studio in a browser" — with no
native build, no C++, and a much lighter GPU footprint than a full WebGL scene. This is
a *current* constraint tied to the primary dev machine's hardware today (Zoidberg,
GTX 960M, 2GB VRAM), not a permanent architectural rule — revisit if the dev machine
changes.

**Held in reserve, not needed now:** true WebGL/Three.js (with `CSS3DRenderer` to keep
real HTML content inside 3D-positioned frames) remains the answer if and when the
product wants actual perspective depth. Separate, additive phase — do not build toward
this preemptively.

---

## 8. Suggested Build Order

Per the confirmed priority in §3: the tray engine is the load-bearing piece. Everything
else is comparatively cheap once it's right.

1. **Tray core** — the two-layer safe-rectangle/frame model (§4.1), outward-only frame
   constraint, `drop-shadow()`-based shading under the single light source, blade
   lifecycle states (blank → labeled → selected → detaching, §5.6/5.7), pop-to-top and
   glow-to-locate selection behavior (§5.5).
2. **Opening programs/files into trays** — a picker (triggered by the blank blade or
   the Silver System Bar's Open command) that feeds into the same "spawn a labeled
   tray" flow, whether the target is a PubCast panel, a manuscript, or a future
   program docking into the Foresight hub (§0).
3. **Everything else is a variant of #1/#2**: a second countertop is another instance
   of the same tray system with its own color-coded arm/fan (§5.4); the carousel
   rotation is one animation; the card-fall close animation (§5.7) is a second; the
   collision/deform toggle (already partially present in `foresight_ui_v18`) is
   optional polish layered on top, not a dependency for the core system to work.
4. **The Sprite (§6)** can be developed in parallel once the Chat Slot and lantern
   anchor points exist spatially — her simplest state (glow, flutter, perch, "Hi.") is
   a reasonable first milestone; the reading-cursor and pointing/guidance behaviors
   (§6.4) can follow once she has somewhere to travel to.

---

## 9. Open Questions (genuinely unresolved — do not treat as decided)

- **Browser vs. native**: currently leaning browser-based; not formally decided against
  a native build.
- **Exact silhouette library**: a fixed but growing named-silhouette system vs. fully
  freeform irregular polygons per tray — current lean is named silhouettes as the
  simpler near-term path, with no fixed cap on how many exist (§3).
- **Fan blade capacity/overflow**: how many labeled blades a single arm's fan can
  hold before needing pagination, scrolling, or sub-grouping is undecided.
- **Tray grouping/stacking**: briefly discussed as a way to manage many trays on one
  countertop (nested/stacked trays with a "peek" of what's underneath) but not
  designed in detail or confirmed — treat as a possible future refinement, not a spec.
- **Corner indent / exact anchor dimensions**: no pixel-level spec yet for how far the
  Upper-Left Control Anchor sits from the bezel, or how it behaves at different
  viewport sizes.
- **Sprite color-adaptation algorithm**: the *principle* (legible, never dominant,
  adapts per theme) is settled; the exact hue/saturation/halo mapping per theme is not.
- **Performance validation**: no benchmarking has been done yet for how multiple
  layered `drop-shadow()`/gradient trays perform during Sprite flight animation on the
  target low-VRAM hardware — recommend an early throwaway stress test before committing
  to a full shading approach.
