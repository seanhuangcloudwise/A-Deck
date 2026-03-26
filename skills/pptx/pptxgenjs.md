# PptxGenJS Tutorial

## Setup & Basic Structure

```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
// or "LAYOUT_16x10", "LAYOUT_4x3", "LAYOUT_WIDE"
pres.author = "Your Name";
pres.title = "Presentation Title";

let slide = pres.addSlide();
slide.addText("Hello World!", { x: 0.5, y: 0.5, fontSize: 36, color: "363636" });

pres.writeFile({ fileName: "Presentation.pptx" });
```

## Layout Dimensions

Slide coordinates in inches:
- `LAYOUT_16x9`: 10" × 5.625" (default)
- `LAYOUT_16x10`: 10" × 6.25"
- `LAYOUT_4x3`: 10" × 7.5"
- `LAYOUT_WIDE`: 13.3" × 7.5"

---

## Text & Formatting

```javascript
// Basic text
slide.addText("Simple Text", {
  x: 1, y: 1, w: 8, h: 2,
  fontSize: 24, fontFace: "Arial",
  color: "363636", bold: true,
  align: "center", valign: "middle"
});

// Character spacing (use charSpacing, NOT letterSpacing — letterSpacing is silently ignored)
slide.addText("SPACED TEXT", { x: 1, y: 1, w: 8, h: 1, charSpacing: 6 });

// Rich text arrays
slide.addText([
  { text: "Bold ", options: { bold: true } },
  { text: "Italic ", options: { italic: true } }
], { x: 1, y: 3, w: 8, h: 1 });

// Multi-line text (requires breakLine: true)
slide.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2", options: { breakLine: true } },
  { text: "Line 3" }  // Last item doesn't need breakLine
], { x: 0.5, y: 0.5, w: 8, h: 2 });

// Text box margin (internal padding)
slide.addText("Title", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  margin: 0  // Use 0 when aligning text with shapes or icons at the same x-position
});
```

**Tip:** Text boxes have internal margin by default. Set `margin: 0` when you need text
to align precisely with shapes, lines, or icons at the same x-position.

---

## Lists & Bullets

```javascript
// ✅ CORRECT: Multiple bullets
slide.addText([
  { text: "First item",  options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true, breakLine: true } },
  { text: "Third item",  options: { bullet: true } }
], { x: 0.5, y: 0.5, w: 8, h: 3 });

// ❌ WRONG: Never use unicode bullets
slide.addText("• First item", { ... });  // Creates double bullets

// Sub-items and numbered lists
{ text: "Sub-item", options: { bullet: true, indentLevel: 1 } }
{ text: "First",   options: { bullet: { type: "number" }, breakLine: true } }
```

---

## Shapes

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 1.5, h: 3.0,
  fill: { color: "FF0000" }, line: { color: "000000", width: 2 }
});

slide.addShape(pres.shapes.OVAL, { x: 4, y: 1, w: 2, h: 2, fill: { color: "0000FF" } });

slide.addShape(pres.shapes.LINE, {
  x: 1, y: 3, w: 5, h: 0, line: { color: "FF0000", width: 3, dashType: "dash" }
});

// With transparency
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "0088CC", transparency: 50 }
});

// Rounded rectangle
// ⚠️ Don't pair with rectangular accent overlays — they won't cover rounded corners.
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2, fill: { color: "FFFFFF" }, rectRadius: 0.1
});

// With shadow — ALWAYS use a fresh object per call (never reuse)
const makeShadow = () => ({
  type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15
});
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2, fill: { color: "FFFFFF" }, shadow: makeShadow()
});
```

Shadow options:

| Property | Type    | Range      | Notes |
|----------|---------|------------|-------|
| `type`   | string  | `"outer"`, `"inner"` | |
| `color`  | string  | 6-char hex | No `#` prefix, no 8-char hex |
| `blur`   | number  | 0-100 pt   | |
| `offset` | number  | 0-200 pt   | **Must be non-negative** |
| `angle`  | number  | 0-359 deg  | 135 = bottom-right, 270 = upward |
| `opacity`| number  | 0.0-1.0    | Never encode opacity in color string |

To cast a shadow upward (e.g. footer bar), use `angle: 270` with positive offset.

---

## Images

```javascript
// From file path
slide.addImage({ path: "images/chart.png", x: 1, y: 1, w: 5, h: 3 });

// From URL
slide.addImage({ path: "https://example.com/image.jpg", x: 1, y: 1, w: 5, h: 3 });

// From base64 (faster, no file I/O)
slide.addImage({ data: "image/png;base64,iVBORw0KGgo...", x: 1, y: 1, w: 5, h: 3 });

// Options
slide.addImage({
  path: "image.png", x: 1, y: 1, w: 5, h: 3,
  rotate: 45,
  rounding: true,       // Circular crop
  transparency: 50,
  flipH: true, flipV: false,
  altText: "Description",
  hyperlink: { url: "https://example.com" }
});

// Sizing modes
{ sizing: { type: "contain", w: 4, h: 3 } }   // fit inside, preserve ratio
{ sizing: { type: "cover",   w: 4, h: 3 } }   // fill area (may crop)
{ sizing: { type: "crop", x: 0.5, y: 0.5, w: 2, h: 2 } }

// Preserve aspect ratio helper
const origW = 1978, origH = 923, maxH = 3.0;
const calcW = maxH * (origW / origH);
slide.addImage({ path: "img.png", x: (10 - calcW) / 2, y: 1.2, w: calcW, h: maxH });
```

---

## Icons

Two methods depending on available dependencies.

### Method A — jimp (Pure JS, no native dependencies, recommended)

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const Jimp = require("jimp");
const { FaCheckCircle, FaChartLine } = require("react-icons/fa");

async function iconToBase64Png(IconComponent, hexColor = "#4472C4", size = 128) {
  // Render icon SVG
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: hexColor, size: String(size) })
  );

  // Convert SVG string to base64 PNG using Jimp
  const svgBuffer = Buffer.from(svg);
  // Jimp cannot parse SVG directly — save as temp file and use a workaround,
  // or inline a minimal canvas via svg2png-wasm.
  // Simplest cross-platform approach: use the @resvg/resvg-js package:
  const { Resvg } = require("@resvg/resvg-js");
  const resvg = new Resvg(svgBuffer, { fitTo: { mode: "width", value: size } });
  const pngData = resvg.render();
  const pngBuffer = pngData.asPng();
  return "image/png;base64," + pngBuffer.toString("base64");
}
```

Install: `npm install @resvg/resvg-js react react-dom react-icons`

### Method B — sharp (requires prebuilt native binary)

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheckCircle } = require("react-icons/fa");

async function iconToBase64Png(IconComponent, hexColor = "#4472C4", size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: hexColor, size: String(size) })
  );
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}
```

Install: `npm install sharp react react-dom react-icons`
On Apple Silicon: `npm install @img/sharp-darwin-arm64`

### Add Icon to Slide

```javascript
// Works with either method (both return the same base64 string format)
const iconData = await iconToBase64Png(FaCheckCircle, "#4472C4", 256);
slide.addImage({ data: iconData, x: 0.5, y: 1.2, w: 0.5, h: 0.5 });
```

**Note:** Use size 256+ for crisp icons. `w`/`h` control display size in inches.

### Icon Libraries

- `react-icons/fa`  — Font Awesome
- `react-icons/md`  — Material Design
- `react-icons/hi`  — Heroicons
- `react-icons/bi`  — Bootstrap Icons

### Simple Fallback (no icons needed)

When icon dependencies are unavailable, replace with a colored circle shape:

```javascript
// Colored circle as icon placeholder
slide.addShape(pres.shapes.OVAL, {
  x: 0.5, y: 1.2, w: 0.5, h: 0.5, fill: { color: "4472C4" }
});
// Overlay a text character as pseudo-icon
slide.addText("✓", {
  x: 0.5, y: 1.2, w: 0.5, h: 0.5,
  fontSize: 16, color: "FFFFFF", align: "center", valign: "middle", margin: 0
});
```

---

## Slide Backgrounds

```javascript
// Solid color
slide.background = { color: "F1F1F1" };

// With transparency
slide.background = { color: "FF3399", transparency: 50 };

// Image from URL
slide.background = { path: "https://example.com/bg.jpg" };

// Image from base64
slide.background = { data: "image/png;base64,iVBORw0KGgo..." };
```

---

## Tables

```javascript
slide.addTable([
  ["Header 1", "Header 2"],
  ["Cell 1",   "Cell 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" }, fill: { color: "F1F1F1" }
});

// Advanced with merged cells
let tableData = [
  [
    { text: "Header", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } },
    "Cell"
  ],
  [{ text: "Merged", options: { colspan: 2 } }]
];
slide.addTable(tableData, { x: 1, y: 3.5, w: 8, colW: [4, 4] });
```

---

## Charts

```javascript
// Bar chart
slide.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1","Q2","Q3","Q4"], values: [4500,5500,6200,7100]
}], {
  x: 0.5, y: 0.6, w: 6, h: 3, barDir: "col",
  showTitle: true, title: "Quarterly Sales"
});

// Line chart
slide.addChart(pres.charts.LINE, [{
  name: "Temp", labels: ["Jan","Feb","Mar"], values: [32,35,42]
}], { x: 0.5, y: 4, w: 6, h: 3, lineSize: 3, lineSmooth: true });

// Pie chart
slide.addChart(pres.charts.PIE, [{
  name: "Share", labels: ["A","B","Other"], values: [35,45,20]
}], { x: 7, y: 1, w: 5, h: 4, showPercent: true });

// Available types: BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR
```

### Better-Looking Charts

Default charts look dated. Apply these options for a modern appearance:

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",

  // Match your palette
  chartColors: ["0D9488", "14B8A6", "5EEAD4"],

  // Clean background
  chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },

  // Muted axis labels
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",

  // Subtle grid (value axis only)
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },

  // Data labels on bars
  showValue: true, dataLabelPosition: "outEnd", dataLabelColor: "1E293B",

  // Hide legend for single series
  showLegend: false,
});
```

Key chart options: `chartColors`, `chartArea`, `catAxisLabelColor`, `valAxisLabelColor`,
`valGridLine`, `catGridLine`, `lineSmooth`, `legendPos` (`"b"`,`"t"`,`"l"`,`"r"`,`"tr"`)

---

## Slide Masters

```javascript
pres.defineSlideMaster({
  title: "TITLE_SLIDE",
  background: { color: "283A5E" },
  objects: [{
    placeholder: { options: { name: "title", type: "title", x: 1, y: 2, w: 8, h: 2 } }
  }]
});

let titleSlide = pres.addSlide({ masterName: "TITLE_SLIDE" });
titleSlide.addText("My Title", { placeholder: "title" });
```

---

## Common Pitfalls

⚠️ These issues cause file corruption, visual bugs, or broken output. Avoid them ALL.

1. **NEVER use `#` with hex colors** — causes file corruption
   ```javascript
   color: "FF0000"   // ✅ CORRECT
   color: "#FF0000"  // ❌ WRONG
   ```

2. **NEVER encode opacity in 8-char hex** — `"00000020"` corrupts the file
   ```javascript
   shadow: { blur: 6, offset: 2, color: "000000", opacity: 0.12 }  // ✅
   shadow: { blur: 6, offset: 2, color: "00000020" }               // ❌ CORRUPTS
   ```

3. **Use `bullet: true`** — NEVER unicode symbols like `•` (creates double bullets)

4. **Use `breakLine: true`** between rich text array items

5. **Avoid `lineSpacing` with bullets** — use `paraSpaceAfter` instead

6. **Each presentation needs a fresh instance** — don't reuse `pptxgen()` objects

7. **NEVER reuse option objects across calls** — PptxGenJS mutates objects in-place
   ```javascript
   const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 });
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });  // ✅ fresh each time
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });  // ✅
   ```

8. **Don't use `ROUNDED_RECTANGLE` with rectangular accent overlays** — corners won't align

9. **Shadow `offset` must be non-negative** — use `angle: 270` for upward shadows, not negative offset

---

## Quick Reference

- **Shapes**: `RECTANGLE`, `OVAL`, `LINE`, `ROUNDED_RECTANGLE`
- **Charts**: `BAR`, `LINE`, `PIE`, `DOUGHNUT`, `SCATTER`, `BUBBLE`, `RADAR`
- **Layouts**: `LAYOUT_16x9` (10"×5.625"), `LAYOUT_16x10`, `LAYOUT_4x3`, `LAYOUT_WIDE`
- **Text align**: `"left"`, `"center"`, `"right"`
- **Chart data labels**: `"outEnd"`, `"inEnd"`, `"center"`
