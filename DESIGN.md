# Webency Design System Specification (`DESIGN.md`)
**Version**: 3.0.0 — Webency Creative Agency Visual Direction  
**Status**: Active Production Standard  

---

## 1. Executive Summary & Aesthetic DNA

This specification codifies the visual direction inspired entirely by **Webency** (`https://webency.themejunction.net/`): a vibrant, high-energy, world-class creative and tech agency aesthetic.

### Core Visual Pillars:
1. **Dynamic Color Spectrum**: Signature electric violet (`#5f39ff`) paired with luminous mint teal (`#20d9a1`), supported by neon magenta (`#fd31bc`) and radiant amber (`#fbb500`).
2. **Dual-Soul Typography**: Bold, technical sans-serif (`'Ubuntu'`) combined with elegant cursive script accents (`'Bilbo Swash Caps'`) for section eyebrows and creative badges.
3. **Pill-Shaped Fluid Buttons**: 150px border-radius buttons with animated multi-stop gradient fills (`linear-gradient(to right, #20d9a1 0%, #5f39ff 51%, #20d9a1 100%)`) and gradient-bordered glass pill buttons.
4. **Atmospheric Dark Surfaces & Luminous Orbs**: Deep charcoal/obsidian hero (`#13131a`) and footer (`#16161c`) backgrounds infused with soft blurred radial lighting (`filter: blur(150px)`) and organic topographic contour line art.
5. **Sculptural Geometry & Micro-Animations**: Arch/stadium framed visual compositions, rotating circular SVG badges (`Creative Minds ✦ Award Winning`), floating stat cards, and subtle organic keyframe animations (`pulse`, `shake-y`, `floatSlow`).

---

## 2. Color Palette & Gradients

```css
:root {
  /* ── Brand Colors ── */
  --tj-color-theme-primary:   #5f39ff;  /* Vibrant Royal Purple */
  --tj-color-theme-secondary: #20d9a1;  /* Luminous Mint Teal */
  --tj-color-theme-accent:    #fd31bc;  /* Neon Magenta */
  --tj-color-theme-gold:      #fbb500;  /* Radiant Amber / Gold */

  /* ── Canvas & Surface ── */
  --tj-color-dark-bg:         #13131a;  /* Hero & Dark Canvas */
  --tj-color-dark-surface:    #1a1a24;  /* Dark Elevated Cards */
  --tj-color-dark-footer:     #16161c;  /* Deep Footer Background */
  --tj-color-light-bg:        #ffffff;  /* Light Section Foundation */
  --tj-color-light-surface:   #f8f7ff;  /* Soft Lilac Tinted Cards */
  --tj-color-light-surface-2: #f2f0ff;  /* Light Highlight Background */

  /* ── Typography & Ink ── */
  --tj-color-heading-primary: #1e1e24;  /* High-Contrast Charcoal Heading */
  --tj-color-heading-white:   #ffffff;  /* White Heading on Dark Canvas */
  --tj-color-text-body:       #66667a;  /* Crisp Body Copy */
  --tj-color-text-muted:      #9999a8;  /* Subtle Metadata */
  --tj-color-text-light:      #e2e2ec;  /* Light Copy on Dark Canvas */

  /* ── Borders & Dividers ── */
  --tj-color-border-light:    #eeecff;  /* Delicate Lilac Card Border */
  --tj-color-border-dark:     #282836;  /* Subtle Dark Section Border */
  --tj-color-border-accent:   #5f39ff;  /* Interactive Focus */

  /* ── Signature Gradients ── */
  --tj-gradient-primary:      linear-gradient(90deg, #20d9a1 0%, #5f39ff 100%);
  --tj-gradient-primary-rev:  linear-gradient(90deg, #5f39ff 0%, #20d9a1 100%);
  --tj-gradient-button:       linear-gradient(to right, #20d9a1 0%, #5f39ff 51%, #20d9a1 100%);
  --tj-gradient-badge:        linear-gradient(90deg, #20d9a1 0%, #5f39ff 100%);
  --tj-gradient-card:         linear-gradient(180deg, rgba(95, 57, 255, 0.04) 0%, rgba(32, 217, 161, 0.02) 100%);
}
```

---

## 3. Typographic System

### 3.1 Typeface Pair
- **Primary Interface, Headings & Body**: `'Ubuntu'`, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif.
- **Signature Accent & Subtitles**: `'Bilbo Swash Caps'`, cursive (fallback: `'Caveat'`, cursive).
- **Labels, Indices, Badges & Tags**: `'Ubuntu'`, sans-serif (consistent sitewide typography without monospaced fonts).

### 3.2 Typography Scale & Roles
- **Hero Display Title**: `70px` (Desktop) / `38px` (Mobile), Weight `700`, Line-height `1.2`. Includes gradient text highlight span (`linear-gradient(90deg, #5f39ff, #20d9a1)`).
- **Primary Section Title (`h2`)**: `48px`–`50px`, Weight `700`, Line-height `1.3`, Color `#1e1e24` or `#ffffff`.
- **Card Title (`h3`/`h4`)**: `22px`–`26px`, Weight `700`.
- **Script Subtitles / Eyebrows (`.sub-title`)**: `35px`, `'Bilbo Swash Caps'`, cursive, letter-spacing `3.5px`, gradient text clip (`linear-gradient(90deg, #20d9a1, #5f39ff)`).
- **Body Copy**: `16px`, Line-height `1.65`, Weight `400`, Color `#66667a`.

---

## 4. Component Architecture

### 4.1 Webency Primary Button (`.tj-primary-btn`)
- Pill shape (`border-radius: 150px`)
- Multi-stop gradient: `linear-gradient(to right, #20d9a1 0%, #5f39ff 51%, #20d9a1 100%)`
- `background-size: 200% auto;`
- Hover: Slides background position to `-100%`, elevates `-2px` with a rich violet glow (`box-shadow: 0 10px 25px rgba(95, 57, 255, 0.35)`).

### 4.2 Webency Secondary Border Button (`.tj-secondary-btn.btn-border`)
- Pill shape (`border-radius: 150px`)
- `padding: 1px;` outer background gradient (`linear-gradient(90deg, #20d9a1, #5f39ff)`)
- Inside `span`: `border-radius: 58px; padding: 16px 34px;` in white or dark obsidian.
- Hover: Inner span becomes transparent gradient, text transitions to pure white.

### 4.3 Hero Composition
- Asymmetric layout:
  - **Left**: Script eyebrow, bold headline with gradient highlight, descriptive copy, primary & secondary action buttons, direct trust notes.
  - **Right**: Sculptural arch / stadium image mask (`border-radius: 200px 200px 0 0` or rounded organic container) with floating statistics card, glowing accent spheres (`blur(150px)`), and subtle geometric line art.

### 4.4 Counter / Metric Bar
- Full-width dark strip (`#1a1a20`) with clean vertical dividers.
- Odometer / counter numbers in bold `56px` display font with teal gradient plus sign.
- Uppercase or title-case label in clean white.

### 4.5 Service Cards (`.tj-service-item`)
- Rounded corners (`border-radius: 20px`), soft lilac surface (`#f8f7ff`).
- Circular floating icon box with gradient or dark violet background.
- Clean heading, informative copy, and hover transformation with elevation and subtle gradient border.

### 4.6 Portfolio Showcase (`.tj_portfolios`)
- Deep dark canvas (`#141419`).
- Category filter pills with active gradient indicator.
- Rounded masonry / card grid with interactive hover overlay, zoom effect, and project metadata.

### 4.7 Testimonials & FAQ
- Large rounded card surfaces (`border-radius: 30px`), SVG quote marks, golden star ratings.
- Accordion with rounded card items, expandable details, and active state violet border highlight.

### 4.8 Footer (`.tj-footer-area`)
- Deep dark canvas (`#16161c`) with subtle topographic contour wave accents.
- 4-column layout: Brand identity, Services, Recent Work / Insights, Direct Contact info with circular icon badges.
- Social links with circular hover gradient transitions.

---

## 5. Animation Tokens
- `pulse`: Subtle rhythmic breathing (`scale(1.03)`).
- `shake-y`: Gentle vertical hover oscillation (`translateY(-8px)`).
- `spin-slow`: Continuous 360-degree rotation for circular badges (20s linear infinite).
