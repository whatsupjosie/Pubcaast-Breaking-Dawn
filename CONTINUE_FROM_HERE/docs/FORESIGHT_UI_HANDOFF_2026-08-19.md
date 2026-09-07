# Foresight UI & Sprite — Design Handoff
### Style: Neo Art Deco Nouveau
**Status: design direction, not yet built. This document is the plan, not a spec of finished work.**

Supplement to the existing `foresight_ui_v18_-16.html` build (titled "Counter / Morphable
Tray Workspace"), which already contains early collision/deform logic
(`deformForCollisions`, `collisionVector`, `shapeDeform`, `overlap`) that this plan extends
rather than replaces.

---

## 1. The Style: Neo Art Deco Nouveau

Four pillars, all four required — this is the language everything else in this document
gets checked against:

- **Great Gatsby opulence and materials** — brass, lacquer, glass, deep jewel tones.
  Richness as a feature, not a flaw.
- **Star Trek ergonomics** — every ornamented surface is still a real control someone
  uses under pressure. Opulence never gets to obscure function. This is what keeps the
  richness from becoming decoration for its own sake.
- **"We ran out of money before we finished our dream home"** — deliberate imperfection.
  Not every surface is maxed out to the same gloss. Some rooms lavish, some plain or
  exposed. That contrast is what makes a space read as real and lived-in rather than a
  rendered showroom — uniform polish everywhere is what makes AI-generated interfaces
  feel fake.
- **Noir lighting** — one strong, consistent, dramatic light source with real shadow
  contrast. This is not just mood — it's the same rule that makes the technical shading
  system work (§4). The aesthetic and the engineering constraint are the same rule.

**Neo Art Deco Nouveau** is the explicit fusion of art deco's geometry and art nouveau's
organic flow — not two competing references, but two expressions of one language,
deployed differently depending on which room you're in (§2).

---

## 2. Two Rooms, One Language

The product has two distinct spaces. They share the Neo Art Deco Nouveau style, the
single-light-source rule, and Foresight the Sprite as the constant anchor — but they are
built and used differently, on purpose:

### The Control Room
The gamified, walk-around space — literally walking into a virtual studio control room
to stand at a mixer, a real video switcher, and push the buttons. This is where the
harder-edged, more geometric deco reference (faceted glass, ornate mixer panels) belongs.
It is immersive and spectacular by design.

**Practical constraint that overrides aesthetics here:** live broadcast switching must be
operable primarily by **hotkeys**, not point-and-click. Mouse and touch are both
acknowledged as too slow and too awkward for real-time, live use — a director can't hunt
for a target with a cursor mid-cut. The ornate visual is the immersive layer; hotkeys are
the actual operating layer underneath it, always.

### The Counter
The everyday workspace — softer, nouveau-leaning: cold granite countertop feel, plates
and flatware with solid texture and striking design, smooth rounded edges, shapes that
taper to a point without ever feeling sharp, forms that flow into one another with an
aerodynamic quality rather than hard angles. This is the primary daily-driver space and
is covered in detail below.

---

## 3. The Counter: Core Metaphor

The workspace is called **the Counter** specifically to get away from the standard
row-and-column, div-and-flexbox look of ordinary web UI. The mental model is a kitchen
counter or table set with different dishware — finger bowls, a dinner plate, serving
dishes, a chafing dish, a salad fork, a soup spoon, a bread plate, a wine glass versus a
water glass — all laid out freely in front of you, arranged the way that actually makes
sense for the meal, not snapped into a grid.

Translated to UI: every open "tray" (a program, file, or tool) is one instance from a
small **vessel library** — a defined set of shapes, each suited to a role:

- **Finger bowl** — small, round, a minor utility panel
- **Dinner plate** — the primary content surface
- **Chafing dish** — large, multi-part, a complex tool with several regions
- **Wine glass vs. water glass** — two visual tiers of the same category (e.g. a
  status indicator vs. a full panel of the same kind)

Trays are positioned freely on the Counter — real absolute positioning, no grid — and can
be dragged, resized, and rearranged the way you'd actually arrange place settings.

---

## 4. Tray Anatomy & Visual Rules

Every tray has two distinct layers, and this split is the load-bearing idea of the whole
system:

1. **The safe rectangle** — the inner region that always reliably displays the actual
   content: text, controls, editors, whatever the tray's job is. This stays ordinary,
   legible, accessible HTML. Content does not get sacrificed for the sake of shape.
2. **The frame** — the outer border, where shape and ornament live. Reshapable into an
   irregular polygon, or (simpler, near-term) one of the fixed vessel silhouettes above,
   with smooth aerodynamic edges per the Counter's material direction.

**Standing rule:** the frame may only bulge *outward* from the safe rectangle — never
inward. Hard constraint. Without it, an oddly-shaped or AI-generated frame will
eventually clip real content.

**"3D" clarified:** not a literal 3D engine or scene. Depth, shading, and a sense of
real-life weight — objects that look like they have mass and are actually sitting on the
Counter, not flat rectangles floating on a page.

**The technical unlock for shaped shadows:** CSS `box-shadow` only works cleanly on
rectangles — it's why most web UI reads as stacked flat cards. `filter: drop-shadow()`
follows the actual silhouette of whatever shape is drawn. This is the correct primitive
for vessel shapes and irregular frames alike.

**Non-negotiable lighting rule (the noir rule):** one consistent light source across
every object on the Counter and in the Control Room alike. Mismatched shadow direction
is the fastest way to break the illusion of real objects on a real surface. Every
highlight gradient (glass streak, ceramic matte falloff, metal reflection band) and every
drop-shadow direction/blur obeys the same light angle, decided once, system-wide.

---

## 5. Interaction

- **Drag** — trays move freely on the Counter surface.
- **Resize** — standard resize, already present in the existing build.
- **Telescope** — trays can grow/shrink with a sense of depth (moving closer/farther),
  not just a flat scale transform.
- **Collision/deformation** — trays can be set to deform against each other when they
  collide, matching the existing physics-style logic already in `foresight_ui_v18`. This
  behavior is a **toggle**, on or off, not forced.
- **Control Room hotkeys** — the primary operating layer for live/real-time work; see §2.

---

## 6. Technical Direction (current thinking, not locked)

Given that "3D" here means shading and weight rather than a literal engine, the current
recommendation is to **stay in plain HTML/SVG/CSS/JS** for this phase:

- Vessel shapes as SVG/`clip-path` geometry
- `filter: drop-shadow()` for real shape-following shadows
- Layered gradients per material (glass, ceramic, metal, brass, lacquer) under the single
  fixed light source
- Free absolute positioning for the Counter surface itself, extending the existing
  drag/resize code already in `foresight_ui_v18`

This keeps the product inside its stated identity — "a studio in a browser" — with no
native build, no C++, and a much lighter GPU footprint than a full WebGL scene (relevant
given the primary dev machine, Zoidberg, runs a GTX 960M with 2GB VRAM).

**Held in reserve, not needed now:** true WebGL/Three.js (with `CSS3DRenderer` to keep
real HTML content inside 3D-positioned frames) remains the answer *if and when* the
product wants actual perspective depth. Separate, additive phase.

---

## 7. Foresight the Sprite

A small, glowing, iridescent presence tied to a lantern — the system's recurring visual
and brand signature, described in discussion as "the system's mouse pointer." Mental
model: Disney's Tinkerbell — same functional role, not a literal copy. Her name is
**Foresight** — she is a sprite, and she carries the product's name itself, not a
separate character name. Meeting her *is* meeting Foresight.

### Design principle
**Foresight becomes a presence before it becomes a workspace.** She appears during
installation itself — not only after setup completes.

### Proposed first-run sequence

```
Download
   ↓
Unpack
   ↓
Initialize
   ↓
✨ First Glimmer (Sprite)
   ↓
Lantern / Sprite Introduction
   ↓
Installation / Setup
   ↓
Foresight Logo
   ↓
Introduction
   ↓
✨ Sprite / Foresight
   ↓
First Conversation
   ↓
Foresight
```

The technical machinery underneath stays completely ordinary — files unpacking,
components initializing, dependencies checking. What changes is what the user sees
layered on top of it:

- Initially just a tiny glow — a shimmer, a flicker.
- She emerges from the lantern.
- She can unobtrusively accompany the install ("We're getting everything ready."), point
  toward progress, react to major stage completions — without narrating every technical
  operation.
- Installation finishes, the interface settles, the intro animation and Foresight logo
  play.
- Rather than introducing an assistant as a bolted-on feature afterward, she's already
  there.
- First spoken line, after light/flutter/settle: **"Hi."** The user has already learned,
  by watching her behave, that light means presence, movement means activity, and the
  lantern means home. Explanation of what she actually is comes after, not before.

### Brand role
The same Sprite embodiment may eventually extend to a Pub Partner as well, making the
tiny shimmer-and-flutter as recognizable across the product line as the logo itself.

### Doctrine structure implication
This reframes what was going to be Chapter 1 ("Installation, Initialization & First Run")
into establishing the philosophical transition — presence before workspace — with
Chapter 2 formally explaining what that presence is.

---

## 8. Creative Exploration — proposals, not decisions

Ideas for how the four style pillars (§1) could extend into the Sprite, the trays, and
the menus. Marked separately from the rest of this document because none of this has
been agreed to yet — it's offered for you to keep, reject, or reshape.

**The lantern as a dock, not just an icon.** If she lives in the lantern, the lantern
itself is a persistent anchor point, visible in both the Counter and the Control Room —
the one constant that ties the two rooms together as one product. At rest she recedes
into it and the lantern glows like a low ember (Gatsby warmth). Under real work, the
glow could shift cooler — a "computer is thinking" cue in the Star Trek sense — and a
brief dim or flicker could stand in for an alert or error, in keeping with noir's
instinct for meaning through light rather than icons. That would make her genuinely
functional as a status signal, not only a mascot — living up to "she's the system's
mouse pointer."

**The lantern's glass, imperfect on purpose.** Brass-and-glass, faceted like the deco
reference — but one pane very slightly mismatched from the rest, a small hand-made flaw.
A literal, physical rendering of the "ran out of money before we finished the dream
home" pillar, rather than that idea only living in the countertop material.

**Trays: ornament frames the control, never hides it.** A brass or dark lacquered bevel
where a tray's frame meets the Counter — a real rim, not just a shadow — echoing the
flatware language already established. And in the same spirit as the lantern's flawed
pane: one tray type could carry a deliberately unfinished edge — a hairline where the
lacquer doesn't quite reach a corner — so the richness never reads as sterile or
templated.

**Menus as objects, not dropdowns.** The existing fan-out menu logic already in
`foresight_ui_v18` (`openFan`/`closeFan`) is most of the way to something better than a
dropdown already — reskinned as an actual folding fan or a hand of cards spreading on a
brass hinge, it becomes a Gatsby-era object rather than a generic UI pattern, without
needing to be rebuilt from scratch.

---

## 9. Open Decisions

- **Browser vs. native** — currently leaning browser-based (matches "a studio in a
  browser"), not yet formally decided against a native C++ build.
- **Frame shape system** — fixed vessel-silhouette library vs. fully freeform irregular
  polygons per tray; current lean is the vessel library as the near-term, simpler path.
- **WebGL phase** — not started, held for a later phase if true perspective/telescoping
  depth is wanted beyond shading/shadow.

---

## 10. What This Extends

- `foresight_ui_v18_-16.html` — existing Counter/Morphable Tray Workspace build with
  early collision/deform code to extend rather than discard.
- Reference material: art deco/nouveau stained-glass images (project uploads), Gemini
  surface/lighting studio notes (`gemini_surfaces.txt`).
