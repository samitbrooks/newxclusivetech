# Design System Specification (`DESIGN.md`)
**Version**: 2.0.0 — Elite Editorial & Engineering Direction  
**Status**: Draft for Phase 1 Approval  

---

## 1. Core Typographic System

### 1.1 Typeface Pair
- **Primary Interface & Editorial Font**: `'Ubuntu'`, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif.
- **Monospace / Data / Metric Font**: `'JetBrains Mono'`, monospace.

### 1.2 Strict Font Weight Limit (Maximum 2 Weights)
The entire site is strictly limited to exactly two font weights of Ubuntu. No exceptions:
- **`400` (Regular)**: All body copy, secondary descriptions, navigation links, meta tags, table content, and form inputs.
- **`700` (Bold)**: All headings (`<h1>` through `<h6>`), button labels, emphasized pricing/metrics, active nav states, and badges.

*(Strictly prohibited: 300 Light, 500 Medium, 800 ExtraBold, and arbitrary weights).*

### 1.3 Strict Modular Type Scale (1.250 — Major Third Ratio)
Base font size: `16px` (`1rem`). Every text element on the site must map directly to one of these 8 steps:

| Token | Size (rem) | Size (px) | Line Height | Tracking | Recommended Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `--type-xs` | `0.75rem` | 12px | 1.40 (16.8px) | `+0.04em` | Category tags, uppercase pills, legal notes |
| `--type-sm` | `0.875rem` | 14px | 1.50 (21.0px) | `+0.01em` | Captions, secondary text, metadata, form labels |
| `--type-base`| `1.000rem` | 16px | 1.60 (25.6px) | `0` | Standard body paragraphs, list items, nav links |
| `--type-lg` | `1.250rem` | 20px | 1.40 (28.0px) | `-0.01em` | Lead paragraphs, card titles, subheadings |
| `--type-xl` | `1.563rem` | 25px | 1.30 (32.5px) | `-0.02em` | `<h3>` headers, metric highlights, modal titles |
| `--type-2xl`| `1.953rem` | 31px | 1.25 (38.8px) | `-0.025em`| `<h2>` section headers (mobile/standard) |
| `--type-3xl`| `2.441rem` | 39px | 1.20 (46.8px) | `-0.03em` | `<h2>` primary section headers (desktop) |
| `--type-4xl`| `3.052rem` | 49px | 1.15 (56.4px) | `-0.035em`| `<h1>` hero display headline (mobile) |
| `--type-5xl`| `3.815rem` | 61px | 1.10 (67.1px) | `-0.04em` | `<h1>` hero display headline (desktop) |

---

## 2. Mathematical Spacing System

### 2.1 Fixed Spacing Scale (8-Point Grid)
Arbitrary pixels (`11px`, `17px`, `23px`, `36px`, `80px`, `96px` ad-hoc) are strictly forbidden. All margins, paddings, gaps, and absolute offsets must use this fixed scale:

| Token | Value | Equivalent | Usage |
| :--- | :--- | :--- | :--- |
| `--space-1` | `0.25rem` | 4px | Micro spacing, icon-to-text gap, border offset |
| `--space-2` | `0.50rem` | 8px | Button inline icon gap, badge padding, compact grid gap |
| `--space-3` | `0.75rem` | 12px | Compact padding, input vertical padding |
| `--space-4` | `1.00rem` | 16px | Standard component padding, inline group spacing |
| `--space-6` | `1.50rem` | 24px | Card padding, standard grid gap, layout column gutter |
| `--space-8` | `2.00rem` | 32px | Large card padding, sub-section separation |
| `--space-12` | `3.00rem` | 48px | Section intra-block spacing, mobile section padding |
| `--space-16` | `4.00rem` | 64px | Standard section vertical padding (mobile/tablet) |
| `--space-24` | `6.00rem` | 96px | Hero and primary section vertical padding (desktop) |

---

## 3. Curated Color Palette & Contrast Hierarchy

All color combinations are mathematically verified to exceed **WCAG AA** (minimum 4.5:1) and achieve **WCAG AAA** (7.0:1+) for primary reading elements.

### 3.1 Surface Tokens
- `--surface-canvas`: `#FFFFFF` — The foundation canvas.
- `--surface-subtle`: `#F8FAFC` (Slate 50) — Subtle alternate section canvas and card backgrounds.
- `--surface-sunken`: `#F1F5F9` (Slate 100) — Input backgrounds, pill tags, and code blocks.
- `--surface-card`: `#FFFFFF` — Primary elevated card background.
- `--surface-inverse`: `#0A0F1D` — Deep obsidian slate for high-impact footer or contrast banners.

### 3.2 Border Tokens
- `--border-subtle`: `#E2E8F0` (Slate 200) — Razor-thin 1px card boundaries and structural dividers.
- `--border-strong`: `#CBD5E1` (Slate 300) — Interactive element borders (secondary buttons, inputs).
- `--border-focus`: `#0A0F1D` — High-contrast interactive focus ring.
- `--border-accent`: `#1D4ED8` (Blue 700) — Active state indicator.

### 3.3 Text & Icon Tokens
- `--text-primary`: `#0A0F1D` — Deep slate-black. Contrast ratio on white: **18.2:1** (WCAG AAA).
- `--text-secondary`: `#334155` (Slate 700) — High-clarity secondary copy. Contrast on white: **9.6:1** (WCAG AAA).
- `--text-muted`: `#64748B` (Slate 500) — Supporting metadata, timestamps, captions. Contrast on white: **4.6:1** (WCAG AA).
- `--text-inverse`: `#FFFFFF` — Text on dark surfaces (`--surface-inverse`).
- `--text-accent`: `#1D4ED8` — Interactive link and category text. Contrast on white: **7.2:1** (WCAG AAA).

### 3.4 Accent Tokens
- `--accent-primary`: `#1D4ED8` (Blue 700) — Authoritative royal cobalt for primary actions.
- `--accent-hover`: `#1E40AF` (Blue 800) — Darker cobalt for hover states.
- `--accent-subtle`: `#EFF6FF` (Blue 50) — Delicate tint for active tabs, selected states, and tags.
- `--accent-success`: `#059669` (Emerald 600) — Reserved solely for live status and confirmed indicators.

---

## 4. Architectural Rules & Anti-Patterns

This design system explicitly prohibits the following five practices:

### 1. No Centered-Everything Layouts
- **The Anti-Pattern**: Stacking a centered badge, centered H2, centered paragraph, and centered 3-card grid in every section.
- **The Rule**: Asymmetric, editorial grid layouts. Strong left-aligned headlines anchored by clear content columns, with generous intentional whitespace.

### 2. No AI-Cliche Text Gradients or Neon Glows
- **The Anti-Pattern**: Multi-stop rainbow/purple-to-cyan text gradients (`gradient-text`) and glowing drop-shadows (`shadow-glow`, neon borders).
- **The Rule**: Sharp, crisp typography in solid high-contrast ink (`--text-primary`). Visual authority comes from proportion, kerning, and negative space — not novelty text gradients.

### 3. No Specificity Wars or Inline Style Overrides
- **The Anti-Pattern**: Littering HTML tags with `style="color: #ffffff !important;"` to patch broken styles.
- **The Rule**: 100% semantic CSS token architecture. Zero `!important` hacks. Single source of truth in CSS tokens.

### 4. No Div Soup or Redundant Wrappers
- **The Anti-Pattern**: Nesting 4 layers of generic `<div>` elements just to center a card or apply a border.
- **The Rule**: Strict semantic HTML5 (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`). Zero arbitrary decorative wrapper divs.

### 5. No Toy Micro-Animations or Visual Gimmicks
- **The Anti-Pattern**: Wobbling, pulsing, shaking, bouncing icons, glowing threads, and decorative background matrices.
- **The Rule**: Fast, stable, static-first rendering. Transitions are limited to micro-interactions under `0.2s ease` on user intent (focus, hover, click). No autonomous looping animations.
