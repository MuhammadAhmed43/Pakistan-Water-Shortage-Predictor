# Stitch Prompt — Pakistan Water Shortage Predictor

Paste the body below into Stitch (https://stitch.withgoogle.com) as a single
prompt. The structure is intentional: it leads with tone so Stitch absorbs the
mood, then specifies design tokens, then walks page by page through the exact
functionality currently implemented in the Streamlit application. Nothing here
asks Stitch to invent new product surface area.

---

## Prompt

I am designing the interface for the **Pakistan Water Shortage Predictor**, a
machine-learning dashboard that forecasts agricultural water shortage at the
district level across Punjab, Pakistan. It is used by farmers, agricultural
extension officers, researchers and policymakers. The subject matter is
serious — water security, crop survival, livelihoods — and the interface must
feel that way.

The goal is a dashboard that looks like it was commissioned by a national
research institute, not a generic SaaS product. Think editorial restraint, the
visual weight of a quarterly report from the World Bank or FAO, the calm of a
museum exhibit, the precision of a meteorological service. Confident, quiet,
data-first. No cartoonish illustrations, no emoji, no neon gradients, no
playful mascots, no Web 3.0 glass-morphism. Every visual decision should make
the data feel trustworthy.

### Brand foundation

- **Name:** Pakistan Water Shortage Predictor.
- **Tagline:** "Decision-grade water intelligence for Pakistan's agriculture."
- **Voice:** measured, technical, plainspoken. Sentences favour clarity over
  flourish. Headlines are noun phrases, not slogans.

### Visual language

- **Mood:** majestic but reserved. Editorial. Cinematic in scale, restrained in
  ornament. Generous negative space. Sparse but deliberate accents.
- **Inspiration references** (for Stitch to draw on tonally):
  - The Pudding's long-form data essays.
  - The Economist's interactive features.
  - NASA Earth Observatory's article layouts.
  - Aga Khan Trust for Culture publications.
  - FAO and World Bank flagship report PDFs converted to web.
- **Cultural resonance:** subtle, never kitsch. No flags waving, no crescent
  moons, no clipart minarets. Permitted motifs, used sparingly:
  - A faint topographic line drawing of the Indus river basin behind hero
    sections.
  - Geometric tessellation patterns inspired by Mughal-era tilework, used at
    very low opacity as section dividers or empty-state textures.
  - An occasional bilingual touch: the page title may be paired with its Urdu
    rendering in a small, refined weight beneath the English headline.

### Colour system

Build the palette around Pakistan flag green, but treat it as ink, not paint.

- **Surface base:** warm parchment `#F7F4ED` (default page background).
- **Surface raised:** ivory `#FBF9F3`.
- **Ink (primary text):** deep forest `#0F2A1D`.
- **Ink muted (secondary text):** slate-green `#4A5E54`.
- **Brand primary:** Pakistan green, used sparingly `#01411C`.
- **Brand secondary (accent):** burnished gold `#B98A2E` (richer than #FFB81C;
  use as a single accent, not a fill).
- **Divider / hairline:** `#E4DFD2`.
- **Severity scale (data only, never decorative):**
  - No Shortage `#2F7D4F`
  - Mild `#6DA579`
  - Moderate `#D6A848`
  - Severe `#C7702C`
  - Critical `#8E2A1F`
- **Dark mode (optional second pass):** ink-on-ink palette using `#0E1815`
  base, `#16221E` raised, `#D8D1BE` text, same severity hues at slightly higher
  luminance.

### Typography

Pair a quiet serif with a precise sans.

- **Headlines and section titles:** *Source Serif 4* (or Spectral), weights
  400 and 600. Used for page titles, section headers, and large numbers in
  metric cards. Tracking very slightly tightened on display sizes.
- **Body, UI, labels:** *Inter* (or Söhne if available), weights 400 / 500 /
  600. Body is `16px / 1.65`. Labels are `13px` uppercase letter-spaced 4%,
  used for category tags and metric captions.
- **Tabular numerals:** enable `font-feature-settings: "tnum"` for every
  number in metrics, tables and charts so columns align.
- **Optional Urdu:** *Noto Nastaliq Urdu*, used only for the bilingual page
  title pairing, never for body copy.

### Layout and grid

- 12-column grid, 80px max gutter on desktop, 24px on mobile.
- Maximum content width 1320px, centered, with a 96px outer margin on large
  screens. Hero sections may extend to the viewport edge with a content column
  still locked at 1320px.
- Vertical rhythm based on an 8px baseline. Section padding 96px top / bottom
  on desktop, 56px on mobile.
- Cards use a 24px corner radius for primary surfaces, 12px for inputs and
  buttons. Avoid pill shapes except for severity tags.

### Component library Stitch should generate

For each, render at least the default and one alternative state.

1. **Buttons.**
   - Primary: solid Pakistan-green fill, ivory text, no shadow, subtle inner
     border-bottom 1px highlight, 14px font, 12px vertical padding, 24px
     horizontal. Hover: shifts to `#0A3015`. Disabled: 40% opacity.
   - Secondary: 1px hairline border in ink-muted, transparent fill, ink text.
   - Tertiary / text: ink text with an animated underline that grows from
     left to right on hover.
2. **Form inputs.** Outline style only, 1px hairline border, label sits above
   the field in the uppercase label style. Focus state thickens the bottom
   edge to 2px in burnished gold, no glow. Helper text in ink-muted 13px.
3. **Sliders.** Slim 2px track, gold filled portion, an 18px ivory thumb with a
   1px ink border. Value chip floats above the thumb in tabular numerals.
4. **Select / dropdown.** Same border treatment as inputs, chevron in
   ink-muted, panel opens with a 200ms fade and 8px upward translate.
5. **Tags / pills.** Severity tags only: filled background using the severity
   colour at 12% opacity, text in the full severity colour, 1px border in the
   same colour, uppercase label style, 6px / 10px padding.
6. **Metric card.** Ivory raised surface, 24px radius, 28px padding. A small
   uppercase label at top, a large serif number (48–72px), an optional
   delta/unit row underneath in ink-muted. No shadows; rely on hairline
   borders and surface differences. On hover the border deepens slightly.
7. **Section header.** Eyebrow (uppercase label, gold), serif title (40px
   desktop / 28px mobile), and a single-sentence description in ink-muted
   underneath. Optional thin divider rule below.
8. **Chart frame.** All charts sit in a card with a header row that contains
   the chart title (serif 20px), an inline legend, and a small overflow menu
   (download, fullscreen). Charts use the severity palette for water data and
   a single gold accent for highlighted series.
9. **Data table.** No vertical rules. Horizontal hairlines only. Header row in
   uppercase labels. Numeric columns right-aligned with tabular numerals. Row
   hover highlights with the parchment-to-ivory shift.
10. **Empty and loading states.** Loading uses a slow shimmer at 6% opacity
    on the parchment surface, never a spinning wheel. Empty states show a
    single line of muted text and a faint topographic line motif behind it.

### Navigation

A persistent left sidebar 280px wide on desktop, collapsible to icon-only at
72px. Top of the sidebar carries the wordmark; below it, a vertical nav with
four items in the order the application defines them:

1. Overview (the landing page)
2. Make Prediction
3. Map View
4. About

Each nav item is a single line of text with a hairline left indicator that
animates in on hover and locks in on the active route. At the bottom of the
sidebar, a compact build-info block: model version, dataset coverage, last
trained date, all in the uppercase label style.

On mobile the sidebar collapses behind a hamburger that opens a full-height
sheet from the left with the same items.

### Page 1 — Overview (landing)

Recreate the existing landing page with elevated production value. Top to
bottom:

1. **Hero band.** Full-bleed, parchment surface, 720px tall on desktop.
   - Eyebrow: "WATER INTELLIGENCE FOR PAKISTAN'S AGRICULTURE".
   - Headline (serif, 88px desktop / 44px mobile): "Forecasting water
     shortage where it matters most — at the district, in the month, for
     the crop you grow."
   - Optional Urdu subline beneath in Nastaliq at 24px, 60% opacity.
   - A single thin horizontal rule, then a sub-paragraph of ink-muted body
     copy describing what the dashboard does in two sentences.
   - Two CTAs: primary "Make a Prediction", secondary "Open the Map".
   - Behind the hero, a faint topographic line drawing of the Indus river
     basin at 8% opacity, anchored bottom-right.
2. **Vision band.** Two-column 8/4 split. Left column: a serif headline ("Our
   Vision") and a 3-sentence paragraph rewriting the existing vision
   statement. Right column: a small grid of three short principles — Data,
   Method, Access — each a label plus a one-line description.
3. **Impact metric strip.** Four metric cards side-by-side on a single row:
   - "Districts Covered" — 20.
   - "Major Crops" — 16.
   - "Years of Data" — 9.
   - "Model Type" — Gradient Boosting.
   Numbers in serif at 64px. Hairline divider above and below the strip.
4. **Methodology teaser.** A three-column row titled "How the index is
   computed", each column a numbered step (01 / 02 / 03) with a short
   serif headline and a sentence of body copy: Predict rainfall, Derive
   effective supply, Compute the Water Sufficiency Index. End the row
   with a tertiary CTA "Read the full methodology" linking to About.
5. **Footer band.** Ink-coloured surface, ivory text. Wordmark left,
   acknowledgements (FAO Paper 56, NASA POWER, Pakistan Bureau of
   Statistics) center, a single line of license and version on the right.
   No social icons, no email signup.

### Page 2 — Make Prediction

A two-column layout: an input column on the left (5/12) and a results column
on the right (7/12) that is empty until a prediction is run.

**Input column, top to bottom:**

- Page header with eyebrow "SINGLE PREDICTION", serif title "Forecast a
  district and crop", one-line description.
- A grouped form, each field with the input style described above:
  - District (select).
  - Crop (select).
  - Soil Type (select).
  - Month (select; rendered as the month name, not a number).
  - Year (number input, with `-` / `+` steppers).
  - Supplemental Irrigation (slider, 0–300 mm, step 10, with the value chip
    floating above the thumb).
- A single primary CTA "Run Forecast", full width of the input column.
- Beneath it, a hairline rule and a 2-line ink-muted disclaimer explaining
  that weather inputs are auto-retrieved from historical averages when not
  supplied.

**Results column, before prediction:** an empty state — a faint topographic
line motif and a single muted sentence: "Configure the inputs on the left and
run the forecast to see results here."

**Results column, after prediction, top to bottom:**

1. **Headline result card.** A wide ivory card with a severity tag in the
   top-right corner. The headline reads, for example, "Moderate water
   shortage expected for Wheat in Multan, June 2024." Beneath it, a single
   very large serif number — the WSI percentage at 96px — with a tiny
   caption "Water Sufficiency Index" underneath in the uppercase label
   style. The card's left edge carries a 4px vertical bar in the severity
   colour. No emoji, no icon.
2. **Quantitative metrics row.** Four metric cards: Predicted Rainfall,
   Irrigation Added, Effective Supply, Crop Demand. Each shows the number
   in serif and the unit (mm) in ink-muted below.
3. **Environmental factors row.** Four metric cards: Temperature,
   Humidity, Wind Speed, Solar Radiation, with units (°C, %, m/s,
   MJ/m²/day).
4. **Charts row.** Two chart frames side by side:
   - Left: a refined radial gauge for the WSI. No 3D, no shine. A thin
     ring (4px) using the severity gradient, a small tick at the current
     value, and the number repeated inside the ring in serif.
   - Right: a horizontal stacked bar showing Effective Supply vs Deficit,
     with a thin overlay marker indicating Crop Demand. Replace the
     existing pie chart entirely — bars communicate ratio more honestly.
5. **Seasonal trend chart.** A wide chart frame spanning the full results
   column. X axis: months Jan–Dec. Two line series: Historical Average
   Rainfall (ink), Crop Water Demand for the selected crop (gold). A
   subtle vertical reference line marks the user's selected month. No
   shaded area under the lines; rely on the line weight and a small
   labelled data point at each end.
6. **Recommendations panel.** A section header "What to do next", then a
   2×N grid of recommendation cards — each card is a single sentence of
   plain text on an ivory surface with a hairline border. No icons, no
   emoji, no priority colours; the severity is already established above.
7. **Export bar.** Right-aligned secondary button "Download forecast as
   CSV" and a tertiary "Copy link to this configuration".

### Page 3 — Map View

A single-column layout dominated by the map.

1. **Filter strip.** A horizontal bar containing four selects (Crop, Soil
   Type, Month, Year), the irrigation slider, and a primary "Generate
   Map" button. The strip is sticky to the top of the content area on
   scroll so the user can re-run with new parameters without losing the
   map view.
2. **Summary metric row.** Four metric cards immediately under the filter
   strip: Average WSI, Districts in Critical, Average Predicted Rainfall,
   Average Temperature.
3. **The map.** Full-width Folium-style map of Punjab, Pakistan with the
   district markers rendered as filled circles using the severity palette.
   Marker size scales subtly with the absolute WSI delta from 100. Hover
   on a marker reveals a small ivory pop-up card with district name,
   severity tag, WSI value and predicted rainfall. The map base layer is
   muted — no Google Maps default; favour a Carto Positron-style minimal
   tileset, desaturated, with country and province borders only.
4. **Legend.** Inline beneath the map: a horizontal row of severity tags
   with their numeric ranges. Tabular numerals throughout.
5. **District data table.** Below the map, an expandable section that
   reveals a sortable table listing every district with WSI, severity,
   predicted rainfall, temperature, humidity and a small inline
   sparkline of seasonal WSI. Default sort: WSI ascending, so the most
   critical districts appear first.

### Page 4 — About

A long-form, editorial page. Maximum reading-column width of 720px for
prose; full-width for visuals and call-out cards.

1. **Page header** — eyebrow "ABOUT", serif title "How this dashboard
   thinks about water shortage", one-paragraph standfirst.
2. **Methodology section.** Three numbered sub-sections (Predict rainfall,
   Derive effective supply, Compute WSI). Each has a serif sub-headline,
   a paragraph of body, and a small inline equation rendered in a
   monospace face. Footnotes use small superscript numbers and a
   bibliography at page end.
3. **Model card.** A wider band with two columns: left lists the
   algorithm details (Gradient Boosting Regressor, 8 features, retrained
   on first run, dataset 33,696 rows 2015–2023); right lists evaluation
   metrics (MAE 1.41, RMSE 2.28, R² 0.0645) and an honesty note
   acknowledging the low R² and what it means for interpretation.
4. **Coverage section.** Two columns of compact alphabetised lists —
   districts on the left, crops on the right — using the uppercase label
   style for the heading and body text for the items.
5. **Disclaimer band.** A full-width ink-coloured band with ivory text
   restating that this is decision support, not a forecast service, and
   not a substitute for local expertise.
6. **Acknowledgements and references.** Plain text, hanging indent,
   academic style. Include FAO Irrigation and Drainage Paper 56, NASA
   POWER, Pakistan Bureau of Statistics, and the open-source libraries
   the project depends on.

### Motion and interaction

- Motion is slow and weighty. Default ease is `cubic-bezier(0.22, 1, 0.36,
  1)`, duration 320ms for the majority of state transitions.
- Page transitions: a 240ms fade plus a 16px upward translate of the
  content column. The sidebar does not move during page transitions.
- Hover on cards: 1px border darkening only. No lift, no scale.
- The hero's topographic background fades in across 1200ms after first
  paint. No looping motion, no parallax.
- Numbers in metric cards count up from zero to their final value across
  600ms with an ease-out curve, once per page mount.
- The map markers fade in district by district in a 1200ms staggered
  cascade after Generate Map completes.

### Accessibility

- All text meets WCAG AA contrast against its surface.
- Severity is never communicated by colour alone — the severity tag also
  carries its name in text.
- Focus rings are 2px in burnished gold, with a 2px parchment offset, on
  every interactive element.
- The dashboard is fully usable by keyboard. Tab order is sidebar →
  filter strip → primary controls → results.
- Charts include a hidden table fallback with the same data for screen
  readers.

### Responsiveness

- Three breakpoints: 480px, 768px, 1280px.
- Below 1280px, the Make Prediction page stacks results below inputs.
- Below 768px, metric strips collapse from four columns to a 2×2 grid.
- Below 480px, charts simplify: the radial gauge becomes a horizontal bar,
  and the seasonal trend chart drops to the historical-rainfall series
  only, with the crop demand series exposed via a toggle.

### Deliverables I would like from Stitch

Generate, in order:

1. A style sheet screen showing the colour system, typography scale, and
   the component library above.
2. The Overview page, full desktop width.
3. The Make Prediction page, in three states: empty, mid-form, post-result.
4. The Map View page, with the map populated and one district pop-up
   open.
5. The About page, full desktop width.
6. A mobile variant of Overview and Make Prediction.
7. Optionally, a dark-mode variant of Overview.

Do not invent additional pages, features, or product surface area. The four
pages above are the entire application.

---

## How to use this prompt

1. Open https://stitch.withgoogle.com.
2. Start a new project. When prompted for a description, paste the entire
   block between the two horizontal rules above, starting from "I am
   designing the interface..." and ending with "...is the entire
   application."
3. Stitch will produce an initial set of screens. Iterate one page at a
   time using targeted follow-ups (for example: "Tighten the Make
   Prediction post-result card; the WSI number should be larger and the
   severity tag should sit top-right, not top-left.").
4. If Stitch leans cartoonish, push back explicitly: "Remove any
   illustrative figures. The page should feel like a printed report, not
   a marketing landing page."
5. Export the components into Figma when satisfied. The colour and type
   tokens above map cleanly to Figma styles.
