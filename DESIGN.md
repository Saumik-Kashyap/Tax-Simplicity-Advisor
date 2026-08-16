---
name: Heritage Modern
colors:
  surface: '#f7f9ff'
  surface-dim: '#d5dae2'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4fc'
  surface-container: '#e9eef6'
  surface-container-high: '#e3e8f0'
  surface-container-highest: '#dee3eb'
  on-surface: '#171c22'
  on-surface-variant: '#44474d'
  inverse-surface: '#2b3137'
  inverse-on-surface: '#ecf1f9'
  outline: '#75777e'
  outline-variant: '#c4c6ce'
  surface-tint: '#4d5f7d'
  primary: '#000615'
  on-primary: '#ffffff'
  primary-container: '#0b1f3a'
  on-primary-container: '#7587a7'
  inverse-primary: '#b5c7ea'
  secondary: '#006b58'
  on-secondary: '#ffffff'
  secondary-container: '#99f4da'
  on-secondary-container: '#00725e'
  tertiary: '#755b00'
  on-tertiary: '#ffffff'
  tertiary-container: '#cea72c'
  on-tertiary-container: '#503d00'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d6e3ff'
  primary-fixed-dim: '#b5c7ea'
  on-primary-fixed: '#071c36'
  on-primary-fixed-variant: '#364764'
  secondary-fixed: '#99f4da'
  secondary-fixed-dim: '#7dd7be'
  on-secondary-fixed: '#002019'
  on-secondary-fixed-variant: '#005142'
  tertiary-fixed: '#ffe08e'
  tertiary-fixed-dim: '#ecc246'
  on-tertiary-fixed: '#241a00'
  on-tertiary-fixed-variant: '#584400'
  background: '#f7f9ff'
  on-background: '#171c22'
  surface-variant: '#dee3eb'
typography:
  display-lg:
    fontFamily: Fraunces
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Fraunces
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-lg:
    fontFamily: Fraunces
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Fraunces
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  section-gap-lg: 64px
  section-gap-md: 32px
  container-padding: 24px
  gutter: 16px
---

## Brand & Style

The design system is engineered for small business owners who require a balance of institutional trust and modern agility. The aesthetic blends **Corporate Modern** reliability with **Minimalist** clarity, ensuring that complex financial data feels approachable rather than overwhelming.

The emotional response should be one of "calm confidence." By utilizing high-quality serif typography against a structured, spacious layout, the UI evokes the feeling of a premium boutique bank. The design avoids "fintech-bro" neon trends in favor of a timeless, stable, and prestigious visual language that respects the gravity of capital management.

## Colors

The palette is anchored by **Deep Navy**, representing stability and depth. **Teal** is used for primary actions and positive financial trends (growth, credit, success), while **Muted Gold** is reserved for high-value highlights, premium features, or "Golden Path" notifications.

- **Primary (Navy):** Used for headers, primary text, and grounding elements.
- **Accent (Teal):** Used for "Commit" actions and interactive states.
- **Highlight (Gold):** Used sparingly for rewards, alerts, or signifying "Premium" status.
- **Surface Strategy:** Layers are built using White surfaces over an Off-white background to create a clear physical hierarchy.

## Typography

This system uses a "Hybrid-Serif" strategy. **Fraunces** provides an authoritative, editorial feel for headings, suggesting a legacy of financial expertise. **Inter** handles all functional and data-heavy content to ensure maximum legibility at small sizes, particularly for transaction ledgers and dashboards.

- **Headlines:** Use tighter letter spacing and lower line heights for a compact, professional look.
- **Numerical Data:** Use Inter with tabular lining figures (if available) to ensure columns of numbers align perfectly in financial tables.
- **Hierarchy:** Ensure a clear contrast between the serif headlines and sans-serif body to guide the user's eye from summary to detail.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy on desktop (max-width 1280px) to maintain a sense of structured stability. On mobile, it transitions to a fluid 4-column system.

- **Generous Breathing Room:** Sections are separated by large vertical gaps (32px to 64px) to prevent "data fatigue" for business owners reviewing their finances.
- **Rhythm:** All margins and paddings must be multiples of 8px.
- **Card Padding:** Standardize internal card padding at 24px (Desktop) and 16px (Mobile) to maintain consistency across the dashboard.

## Elevation & Depth

Hierarchy is established through **Ambient Shadows** and **Tonal Layers**. Instead of harsh borders, we use depth to separate global navigation from the workspace.

- **Shadow Profile:** Use a singular, highly-diffused shadow for floating elements: `0 4px 20px rgba(11, 31, 58, 0.06)`. The navy tint in the shadow prevents it from looking "dirty" on the off-white background.
- **Surface Elevation:** 
  - Level 0: Soft Off-white Background (`#F7F9FC`).
  - Level 1: White Cards (`#FFFFFF`) with 1px border (`#E3E8F0`).
  - Level 2: Active Modals or Pop-overs with the signature ambient shadow.

## Shapes

The shape language is "Stable-Rounded." We use a 14px radius (defined as `rounded-lg` in this system) for primary containers. This specific radius is soft enough to feel modern and accessible, but structured enough to feel more professional than "playful" circular designs.

- **Standard Elements:** Buttons and Input fields use the base 14px radius.
- **Small Elements:** Tooltips and tags use a reduced 6px radius.
- **Consistency:** Never mix sharp corners with rounded corners within the same component family.

## Components

### Buttons
- **Primary:** Deep Navy background with White text. 14px radius. High emphasis.
- **Secondary:** Teal border and text with White background. Used for secondary calls to action.
- **Ghost:** Transparent background with Navy text. Used for navigation or low-priority actions.

### Input Fields
- White background with a 1px border (`#E3E8F0`).
- On Focus: Border changes to Teal (`#167D68`) with a 2px outer glow.
- Labels are always positioned above the field in `label-md` (Inter, Bold).

### Cards
- The foundational unit of the UI.
- 14px border radius, White background, 1px Light Grey border.
- Cards should have a "Header" section for titles in `headline-md` (Fraunces).

### Chips & Status Tags
- Used for transaction statuses (e.g., Pending, Completed).
- Use low-saturation background tints of the status color with high-saturation text to maintain accessibility.

### Data Tables
- Row-based layout with subtle 1px horizontal dividers.
- Header row uses `label-sm` (Inter, Uppercase) for clear categorization.
- Hover state: Change row background to `#F7F9FC` for better focus.

### Icons
- 24px grid, 1.5pt stroke weight. 
- Avoid filled icons unless used for active navigation states. Icons should be Navy or Teal.