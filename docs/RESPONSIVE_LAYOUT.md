# Kitchen Roots Responsive Layout Guide

## Purpose

The existing mobile mockups are the source of truth for the app's content,
visual hierarchy, and core navigation. Larger layouts should expand that
design without changing the user flow.

## Breakpoints

- Mobile: 760px and below
- Tablet: 761px through 1023px
- Desktop: 1024px and wider

## Recipe Collection

- Mobile: display recipe cards in one column.
- Tablet: display recipe cards in two columns when space permits.
- Desktop: display recipe cards in up to three columns.
- Keep each entire recipe card easy to select.

## Recipe Detail

- Mobile: stack ingredients, steps, and notes in one column.
- Tablet and desktop: place ingredients beside steps.
- Give the steps section more width than the ingredients section.
- Display notes in one column on mobile and two columns on larger screens.

## Navigation

- Mobile: show the Kitchen Roots brand and hide secondary header text.
- Desktop: show the brand and supporting header text.
- Navigation must remain consistent between collection and detail pages.

## Add Recipe Form

- Mobile: stack all form fields in one column.
- Desktop: keep the form centered with a readable maximum width.
- Ingredient and step controls must remain large enough to select easily.

## Validation

Tested the recipe collection and recipe detail pages in Safari Responsive
Design Mode.

- At 390px, content uses a readable one-column mobile layout.
- At 760px, content continues to use the mobile layout.
- At 1200px, the collection uses a multi-column layout and recipe details use the standard desktop layout.
- Navigation, recipe links, ingredients, steps, tags, and notes remain readable and usable at both phone and desktop widths.
