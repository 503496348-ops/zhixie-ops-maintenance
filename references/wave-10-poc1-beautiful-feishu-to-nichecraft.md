# Wave-10 POC-1 预检：beautiful-feishu-whiteboard -> nichecraft

生成时间：2026-07-16T14:49:05

外部候选模板: 35 个，nichecraft 模板: 20 个。
重叠数: 16，独占可补齐: 19。

候选独占样式前3（POC-1）：
- apricot-arc
- berry-pop
- bold-poster

复核结果（每项）：

### apricot-arc
- 候选仓存在: True
- nichecraft 中重复: False
- 设计元数据样例:
---
version: 1.0
name: Apricot Arc
renderer: feishu-svg-whiteboard
description: >
  A warm mid-century geometric design system for Feishu SVG whiteboards. Soft cream canvas, no borders and no shadows — depth comes purely from flat apricot-and-salmon color-blocking and a signature half-circle (arc) motif laid out on a tight checkerboard rhythm. Rounded, friendly, two-hue palette with a deep terracotta ink reserved for text inside light panels. Calm and retro rather than loud. Built for explanatory diagrams that benefit from a soft, rhythmic, optimistic register: stages, comparisons, system maps, timelines, and step pipelines.

# ── COLOR ────────────────────────────────────────────────────
colors:
  cream: "#FFF8EE" # universal canvas background — warm soft ivory, never pure white
  paper: "#FFFFFF" # optional clean panel fill (highest-contrast card)
  orange: "#F69834" # primary accent — warm apricot orange; alternates with salmon to create rhythm, not collision
  salmon: "#F9C2BD" # secondary accent — soft salmon pink (pairs with orange); never put light text on salmon
  terracotta: "#C7561E" # ink only — text, big numerals, occasional 3px rule; a deep burnt tone from the orange family so the system never goes cold or black; not a fill block
  ink-2: "#7A4A33" # softer brown for secondary text on light panels
  # Use the 2-hue core (orange + salmon) per scene — that pairing IS the identity; terracotta is for ink only, not a fill block.
  # Dark (terracotta) text on light fills always. No black — the system stays warm.
  # Opacity is ignored: get a lighter shade by choosing a lighter solid (cream over salmon over orange), never by fading.

# ── DEPTH ────────────────────────────────────────────────────
# FLAT system — NO shadows of any kind (no blur, no duplicate-offset trick).
# Depth and hierarchy come from flat color blocks, the arc motif, panel role-swaps, and scale.
# The reference is borderless: prefer abutting flat shapes over outlined cards.


### berry-pop
- 候选仓存在: True
- nichecraft 中重复: False
- 设计元数据样例:
---
version: 1.0
name: Berry Pop
renderer: feishu-svg-whiteboard
description: >
  A fresh, fruity brand palette: a clean white page with two pop accents, a deep raspberry-wine and a
  pale periwinkle. The raspberry is the loud hero (bold fills, headers, big blocks) and a darker wine
  doubles as the readable ink; the periwinkle is the soft cool counter, used for light panels and for
  text on a berry fill. Confident and playful, like a juice-bar or club logo. Flat color only, no
  gradients; hard offset shadows are fine.

# ── COLOR ────────────────────────────────────────────────────
colors:
  white: "#FFFFFF" # universal canvas: clean bright white
  berry: "#9E2B50" # PRIMARY accent: deep raspberry-wine. Hero fills, headers, key blocks
  berry-deep: "#6E1E3A" # darker wine: body/structural text on white, borders, hard shadows (the in-family "ink")
  peri: "#C7D2F0" # SECONDARY accent: pale periwinkle. Soft panels/fills, and large text on a berry fill
  peri-deep: "#9DB0E8" # stronger periwinkle: small accents, rules, dots where the pale tone is too faint
  # White page + two accent families. Berry leads, periwinkle supports; both share a scene. Berry-deep
  # is the text color on white. Keep two accents per scene; let the white breathe.

# ── TEXT COLOR ───────────────────────────────────────────────
text-rules:
  rule: "Text is berry-deep on the white page (a deep wine that reads like ink). On a berry fill, use large bold white or pale periwinkle. Keep periwinkle out of small text on white (too pale)."

### bold-poster
- 候选仓存在: True
- nichecraft 中重复: False
- 设计元数据样例:
---
version: 1.0
name: Bold Poster
renderer: feishu-svg-whiteboard
description: >
  A populist editorial-poster palette of uncompromising restraint: a white canvas, a deep brown-black
  ink, a single saturated tomato red, and a warm off-white for alternating panels. No secondary brand
  colors, no tints, no semantic state colors. Red is reserved for emphasis moments only (numerals,
  active rules, calls to action, full-bleed statement panels), never body text or an empty fill. Loud,
  confident, and unmistakably print-poster. The only depth is a single hard offset shadow behind red
  display text.

# ── COLOR ────────────────────────────────────────────────────
colors:
  bg: "#FFFFFF" # pure white canvas: the default ground for most surfaces, reads as fresh newsprint
  dark: "#1C1410" # deep brown-black with a warm bias (not pure black — warmth sets it apart from a generic editorial black): ALL body text, borders, small labels, and full-bleed dark panel grounds
  red: "#D8000F" # saturated tomato red: the single accent, emphasis moments only — numerals, section eyebrows, the active emphasis rule, bullet glyphs, the progress bar, calls to action, full-bleed statement panels
  light: "#F5F2EF" # warm off-white: stripe alternating panels and small chrome backgrounds; subtly warmer than bg so a surface differentiates without breaking the printed-paper register
  # Two-color identity: brown-black ink on white, with red as the sole accent. Red is never body
  # text, never a tint, never a card fill without overlaid text.

# ── SHADOW ───────────────────────────────────────────────────
shadow:
  recipe: "redraw the shape or word once in dark behind the real red display text, offset on x and y"

结论：3 个样式均为 `candidate-only`，可进入字段映射与规则复用试点。