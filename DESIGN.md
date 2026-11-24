---
version: alpha
name: Awwwards
description: "Light monochrome interface measured from awwwards.com: Inter Tight type, tonal surfaces and 72px corners."
colors:
  background: "#E9E9E9"
  surface: "#E9E9E9"
  on-surface: "#222222"
  on-background: "#222222"
  surface-container-low: "#EDEDED"
  surface-container: "#F8F8F8"
  surface-container-high: "#FFFFFF"
  outline: "#A7A7A7"
  outline-variant: "#FFF083"
  primary: "#222222"
  on-primary: "#FFFFFF"
typography:
  headline-display:
    fontFamily: Inter Tight
    fontSize: 127px
    fontWeight: 600
    lineHeight: 1
  headline-lg:
    fontFamily: Inter Tight
    fontSize: 111px
    fontWeight: 600
    lineHeight: 1
  headline-md:
    fontFamily: Inter Tight
    fontSize: 42px
    fontWeight: 600
    lineHeight: 1.2
  headline-sm:
    fontFamily: Inter Tight
    fontSize: 20.5px
    fontWeight: 600
    lineHeight: 1.36
  body-md:
    fontFamily: Inter Tight
    fontSize: 14px
    fontWeight: 300
    lineHeight: 2
  body-lg:
    fontFamily: Inter Tight
    fontSize: 18px
    fontWeight: 300
    lineHeight: 1.56
  body-sm:
    fontFamily: Inter Tight
    fontSize: 13px
    fontWeight: 300
    lineHeight: 2.15
  label-md:
    fontFamily: Inter Tight
    fontSize: 14px
    fontWeight: 400
    lineHeight: 2
  headline-display-mobile:
    fontFamily: Inter Tight
    fontSize: 42px
    fontWeight: 600
    lineHeight: 1
  headline-sm-mobile:
    fontFamily: Inter Tight
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.56
rounded:
  sm: 4px
  md: 8px
  lg: 72px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 24px
  xl: 37.3px
  gutter: 8px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 0px 20px
    height: 42px
  button-primary-hover:
    backgroundColor: "#383838"
  button-outline:
    backgroundColor: "{colors.outline-variant}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 0px 15.6px
    height: 60px
  button-ghost:
    textColor: "#DEDEDE"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 0px 12px
    height: 48px
  input-field:
    textColor: "{colors.on-surface}"
    typography: "{typography.body-sm}"
    rounded: 0px
    padding: 0px 0px 0px 38px
  link:
    textColor: "{colors.primary}"
---

# Awwwards Design System

## Overview

Awwwards describes itself as: “A high-performance platform for F1 driver Lando Norris, capturing his energy and racing passion through dynamic interactions, bold visuals, and a digital...” The interface is light, built on **Mist (#E9E9E9)** with **Charcoal (#222222)** text and almost no color: actions are carried by contrast, not hue.

Type is set in **Inter Tight**. Headlines run large; body text is 14px. The surface language is flat. Corners are mostly 72px.

Measured from [awwwards.com](https://www.awwwards.com/sites/lando-norris) on November 24, 2026 at 1440×900 and 390×844 from 347 rendered elements. Values are computed styles from the live page, not the original source files.

## Colors

The palette has 9 roles.

- **Mist (#E9E9E9):** Page background, seen 1 time. Token `background`, CSS `--ch-bg`.
- **Charcoal (#222222):** Primary text and headings, seen 142 times. Token `on-surface`, CSS `--border-table`.
- **Mist (#EDEDED):** Raised areas one step from the page, seen 6 times. Token `surface-container-low`, CSS `--border-gray`.
- **Snow (#F8F8F8):** Cards and panels, seen 5 times. Token `surface-container`, CSS `--bg-primary`.
- **White (#FFFFFF):** Hover and pressed fills, seen 2 times. Token `surface-container-high`, CSS `--check-toggle-color-ball`.
- **Gray (#A7A7A7):** Borders and dividers, seen 10 times. Token `outline`.
- **Light Yellow (#FFF083):** Secondary dividers, seen 1 time. Token `outline-variant`, CSS `--color-learn`.
- **Charcoal (#222222):** Primary buttons and calls to action, seen 212 times. Token `primary`, CSS `--border-table`.
- **White (#FFFFFF):** Text and icons on primary. Token `on-primary`.

## Typography

**Inter Tight** carries the whole interface. Fallback stack: `Inter Tight`.

- **headline-display:** Inter Tight 127px at weight 600, line height 1, uppercase (42px on mobile). Page title (h1).
- **headline-lg:** Inter Tight 111px at weight 600, line height 1. Section headings (h2).
- **headline-md:** Inter Tight 42px at weight 600, line height 1.2. Sub-section headings.
- **headline-sm:** Inter Tight 20.5px at weight 600, line height 1.36 (18px on mobile). Card and feature titles.
- **body-md:** Inter Tight 14px at weight 300, line height 2. Body text.
- **body-lg:** Inter Tight 18px at weight 300, line height 1.56. Lead paragraphs.
- **body-sm:** Inter Tight 13px at weight 300, line height 2.15. Secondary and small text.
- **label-md:** Inter Tight 14px at weight 400, line height 2. Buttons, navigation and labels.

## Layout

Spacing is mostly on a 4px grid (77% of measured values), with some off-grid steps. Match the measured scale rather than rounding everything.

- **Scale:** xs 4px, sm 8px, md 12px, lg 24px, xl 37.3px.
- **Gaps:** 8px is the most common gap in flex and grid layouts.
- **Breakpoints:** 576px, 700px, 768px, 1000px, 1024px, 1100px, 1168px, 1184px, 1270px, 1280px, 1360px, 1490px, 1556px, 1578px, 1600px, 1780px, 2291px.

## Elevation & Depth

The design is flat: no shadows were measured. Hierarchy comes from tonal surface steps (#EDEDED → #F8F8F8 → #FFFFFF) and #A7A7A7 borders.

## Shapes

Most elements use 72px corners. Measured radii, most used first:

- **lg (72px):** 40 elements.
- **md (8px):** 32 elements.
- **sm (4px):** 4 elements.

## Components

Measured from the rendered page. Token values reference the tokens above.

- **button-primary (“Be Pro”):** #222222 fill, #FFFFFF text, 14px/500, 8px radius, padding 0px 20px.
- **button-primary-hover:** background #383838, text #FFFFFF on hover.
- **button-outline (“Visit Site”):** #FFF083 fill, #222222 text, 13px/600, 8px radius, padding 0px 15.6px.
- **button-ghost (“Font & Color”):** transparent fill, #DEDEDE text, 13px/400, 8px radius, padding 0px 12px, border 1px solid #4E4E4E.
- **input-field (“Search by Inspiration”):** transparent fill, #222222 text, 13.3px/400, padding 0px 0px 0px 38px.
- **link:** transparent fill, #222222 text, padding 0px.

## Do's and Don'ts

- Do use #E9E9E9 for the page and lift surfaces in small steps: #EDEDED, #F8F8F8, #FFFFFF.
- Do let contrast carry emphasis; primary actions use #222222 on #E9E9E9.
- Do reuse the measured spacing steps (8px, 12px, 24px).
- Do use 72px corners on most elements; larger surfaces also use 8px and 4px.
- Don't add drop shadows for depth; use tonal surfaces.
- Don't introduce new font families beyond Inter Tight.
- Don't add saturated accent colors; the measured palette is almost entirely neutral.
- Don't make interface transitions slower than 0.3s.

## Motion

Interface transitions are quick: 0.3s.

- **Easing:** `ease`, `ease-in-out`.
