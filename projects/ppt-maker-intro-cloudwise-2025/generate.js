const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const { Resvg } = require("@resvg/resvg-js");
const {
  FaRobot,
  FaSitemap,
  FaPalette,
  FaCheckCircle,
  FaClipboardCheck,
  FaBook,
  FaRocket,
  FaEnvelope,
} = require("react-icons/fa");

// cloudwise 2025 style signature
const PALETTE = {
  neutral: "A5A7AA",
  accent: "00CCD7",
  dark: "2F2F2F",
  light: "FFFFFF",
  soft: "E7E6E6",
  text: "1F2937",
};

const FONT = {
  header: "Microsoft YaHei",
  body: "Microsoft YaHei",
  alt: "Arial",
};

function iconToBase64(IconComponent, color, size = 220) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
  const resvg = new Resvg(svg, { fitTo: { mode: "width", value: size } });
  const pngBuffer = resvg.render().asPng();
  return "image/png;base64," + Buffer.from(pngBuffer).toString("base64");
}

const makeShadow = () => ({
  type: "outer",
  color: "000000",
  blur: 7,
  offset: 2,
  opacity: 0.12,
  angle: 135,
});

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "PPT Maker Agent";
  pres.title = "PPT Maker Agent Self Intro - Cloudwise 2025 Master";

  // True master usage: all slides reference this master name
  pres.defineSlideMaster({
    title: "CLOUDWISE_2025",
    bkgd: PALETTE.light,
    objects: [
      {
        rect: {
          x: 0,
          y: 0,
          w: 10,
          h: 0.14,
          fill: { color: PALETTE.accent },
          line: { color: PALETTE.accent, pt: 0 },
        },
      },
      {
        rect: {
          x: 0,
          y: 5.50,
          w: 10,
          h: 0.125,
          fill: { color: PALETTE.neutral },
          line: { color: PALETTE.neutral, pt: 0 },
        },
      },
      {
        text: {
          text: "Master: cloudwise 2025 | Scene: product-brochure",
          options: {
            x: 0.25,
            y: 5.515,
            w: 6.5,
            h: 0.1,
            fontFace: FONT.alt,
            fontSize: 8,
            color: PALETTE.dark,
            margin: 0,
          },
        },
      },
    ],
  });

  // Slide 1
  const s1 = pres.addSlide({ masterName: "CLOUDWISE_2025" });
  s1.background = { color: PALETTE.dark };
  s1.addShape(pres.shapes.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 0.14,
    fill: { color: PALETTE.accent },
    line: { color: PALETTE.accent, pt: 0 },
  });
  s1.addShape(pres.shapes.RECTANGLE, {
    x: 0,
    y: 5.50,
    w: 10,
    h: 0.125,
    fill: { color: PALETTE.accent },
    line: { color: PALETTE.accent, pt: 0 },
  });
  const robot = iconToBase64(FaRobot, "#" + PALETTE.accent, 240);
  s1.addImage({ data: robot, x: 0.6, y: 1.1, w: 0.95, h: 0.95 });
  s1.addText("PPT Maker Agent", {
    x: 1.8,
    y: 1.1,
    w: 7.7,
    h: 0.9,
    fontFace: FONT.header,
    fontSize: 48,
    bold: true,
    color: PALETTE.light,
    margin: 0,
  });
  s1.addText("Self-introduction regenerated with true slide master", {
    x: 1.8,
    y: 2.1,
    w: 7.2,
    h: 0.45,
    fontFace: FONT.body,
    fontSize: 16,
    color: PALETTE.soft,
    margin: 0,
  });

  // Slide 2
  const s2 = pres.addSlide({ masterName: "CLOUDWISE_2025" });
  s2.addShape(pres.shapes.RECTANGLE, {
    x: 0,
    y: 0.14,
    w: 10,
    h: 0.75,
    fill: { color: PALETTE.neutral },
    line: { color: PALETTE.neutral, pt: 0 },
  });
  s2.addText("目录 / Agenda", {
    x: 0.6,
    y: 0.28,
    w: 4.3,
    h: 0.45,
    fontFace: FONT.header,
    bold: true,
    fontSize: 30,
    color: PALETTE.dark,
    margin: 0,
  });
  const agenda = [
    "01 Background & Positioning",
    "02 Core Capabilities",
    "03 Workflow and Quality System",
    "04 Master + Knowledge Integration",
    "05 Vision & Contact",
  ];
  agenda.forEach((item, i) => {
    const y = 1.3 + i * 0.78;
    s2.addShape(pres.shapes.RECTANGLE, {
      x: 0.8,
      y,
      w: 0.08,
      h: 0.42,
      fill: { color: PALETTE.accent },
      line: { color: PALETTE.accent, pt: 0 },
    });
    s2.addText(item, {
      x: 1.0,
      y,
      w: 8,
      h: 0.42,
      fontFace: FONT.body,
      fontSize: 18,
      color: PALETTE.dark,
      margin: 0,
    });
  });

  // Slide 3
  const s3 = pres.addSlide({ masterName: "CLOUDWISE_2025" });
  s3.addText("AI Presentation Architecture", {
    x: 0.6,
    y: 0.35,
    w: 7.9,
    h: 0.5,
    fontFace: FONT.header,
    bold: true,
    fontSize: 33,
    color: PALETTE.dark,
    margin: 0,
  });
  const archIcon = iconToBase64(FaSitemap, "#" + PALETTE.accent, 170);
  s3.addImage({ data: archIcon, x: 8.8, y: 0.28, w: 0.65, h: 0.65 });
  const cards = [
    ["Create", "PptxGenJS generation"],
    ["Edit", "XML unpack/edit/pack"],
    ["Analyze", "Text/visual audit"],
    ["Template", "Structure reuse + adaptation"],
  ];
  cards.forEach((c, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.7 + col * 4.4;
    const y = 1.2 + row * 1.95;
    s3.addShape(pres.shapes.RECTANGLE, {
      x,
      y,
      w: 3.85,
      h: 1.5,
      fill: { color: PALETTE.light },
      line: { color: PALETTE.soft, pt: 1 },
      shadow: makeShadow(),
    });
    s3.addShape(pres.shapes.RECTANGLE, {
      x,
      y,
      w: 3.85,
      h: 0.09,
      fill: { color: PALETTE.accent },
      line: { color: PALETTE.accent, pt: 0 },
    });
    s3.addText(c[0], {
      x: x + 0.2,
      y: y + 0.22,
      w: 3.1,
      h: 0.32,
      fontFace: FONT.header,
      bold: true,
      fontSize: 20,
      color: PALETTE.dark,
      margin: 0,
    });
    s3.addText(c[1], {
      x: x + 0.2,
      y: y + 0.68,
      w: 3.3,
      h: 0.5,
      fontFace: FONT.body,
      fontSize: 13,
      color: "44546A",
      margin: 0,
    });
  });

  // Slide 4
  const s4 = pres.addSlide({ masterName: "CLOUDWISE_2025" });
  s4.addText("Core Capabilities", {
    x: 0.6,
    y: 0.35,
    w: 8,
    h: 0.6,
    fontFace: FONT.header,
    bold: true,
    fontSize: 34,
    color: PALETTE.dark,
    margin: 0,
  });
  const capabilityIcons = [
    [FaPalette, "Design System", "Palette+Typography control"],
    [FaCheckCircle, "QA Engine", "Mandatory content and visual checks"],
    [FaClipboardCheck, "Knowledge Learning", "Item-by-item confirmation gate"],
    [FaBook, "Master Library", "Extract, name, and reuse masters"],
  ];
  capabilityIcons.forEach((it, i) => {
    const y = 1.25 + i * 1.0;
    const ico = iconToBase64(it[0], "#" + PALETTE.accent, 150);
    s4.addShape(pres.shapes.OVAL, {
      x: 0.75,
      y: y + 0.04,
      w: 0.48,
      h: 0.48,
      fill: { color: PALETTE.dark },
      line: { color: PALETTE.dark, pt: 0 },
    });
    s4.addImage({ data: ico, x: 0.81, y: y + 0.1, w: 0.35, h: 0.35 });
    s4.addText(it[1], {
      x: 1.42,
      y,
      w: 3.6,
      h: 0.32,
      fontFace: FONT.header,
      bold: true,
      fontSize: 18,
      color: PALETTE.dark,
      margin: 0,
    });
    s4.addText(it[2], {
      x: 1.42,
      y: y + 0.34,
      w: 7.7,
      h: 0.4,
      fontFace: FONT.body,
      fontSize: 13,
      color: "5A5A5A",
      margin: 0,
    });
  });

  // Slide 5
  const s5 = pres.addSlide({ masterName: "CLOUDWISE_2025" });
  s5.addText("Production Workflow", {
    x: 0.6,
    y: 0.35,
    w: 8,
    h: 0.6,
    fontFace: FONT.header,
    bold: true,
    fontSize: 34,
    color: PALETTE.dark,
    margin: 0,
  });
  const steps = ["Detect", "Extract", "Confirm", "Generate", "QA", "Deliver"];
  steps.forEach((step, i) => {
    const x = 0.55 + i * 1.55;
    s5.addShape(pres.shapes.OVAL, {
      x,
      y: 2.1,
      w: 0.66,
      h: 0.66,
      fill: { color: i % 2 === 0 ? PALETTE.accent : PALETTE.neutral },
      line: { color: "FFFFFF", pt: 0.4 },
      shadow: makeShadow(),
    });
    s5.addText(String(i + 1), {
      x,
      y: 2.1,
      w: 0.66,
      h: 0.66,
      fontFace: FONT.alt,
      bold: true,
      fontSize: 19,
      color: PALETTE.dark,
      align: "center",
      valign: "middle",
      margin: 0,
    });
    s5.addText(step, {
      x: x - 0.15,
      y: 2.85,
      w: 0.95,
      h: 0.3,
      fontFace: FONT.body,
      fontSize: 11,
      bold: true,
      color: PALETTE.dark,
      align: "center",
      margin: 0,
    });
    if (i < steps.length - 1) {
      s5.addShape(pres.shapes.LINE, {
        x: x + 0.66,
        y: 2.43,
        w: 0.89,
        h: 0,
        line: { color: PALETTE.neutral, pt: 1.2 },
      });
    }
  });

  // Slide 6
  const s6 = pres.addSlide({ masterName: "CLOUDWISE_2025" });
  s6.background = { color: PALETTE.dark };
  s6.addShape(pres.shapes.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 0.14,
    fill: { color: PALETTE.accent },
    line: { color: PALETTE.accent, pt: 0 },
  });
  s6.addShape(pres.shapes.RECTANGLE, {
    x: 0,
    y: 5.50,
    w: 10,
    h: 0.125,
    fill: { color: PALETTE.accent },
    line: { color: PALETTE.accent, pt: 0 },
  });
  const rocket = iconToBase64(FaRocket, "#" + PALETTE.accent, 250);
  s6.addImage({ data: rocket, x: 0.65, y: 1.0, w: 1.0, h: 1.0 });
  s6.addText("Vision", {
    x: 1.85,
    y: 1.08,
    w: 6,
    h: 0.6,
    fontFace: FONT.header,
    bold: true,
    fontSize: 39,
    color: PALETTE.light,
    margin: 0,
  });
  s6.addText(
    "Build scene-aware presentation workflows where knowledge and reusable masters continuously improve output quality.",
    {
      x: 1.85,
      y: 1.88,
      w: 7.1,
      h: 1.15,
      fontFace: FONT.body,
      fontSize: 17,
      color: PALETTE.soft,
      margin: 0,
    }
  );

  // Slide 7
  const s7 = pres.addSlide({ masterName: "CLOUDWISE_2025" });
  s7.addText("Thank You", {
    x: 0.8,
    y: 1.2,
    w: 4,
    h: 0.6,
    fontFace: FONT.header,
    bold: true,
    fontSize: 42,
    color: PALETTE.dark,
    margin: 0,
  });
  const mail = iconToBase64(FaEnvelope, "#" + PALETTE.accent, 160);
  s7.addImage({ data: mail, x: 0.95, y: 2.15, w: 0.45, h: 0.45 });
  s7.addText("GitHub: anthropics/skills/pptx", {
    x: 1.55,
    y: 2.2,
    w: 6.6,
    h: 0.35,
    fontFace: FONT.body,
    fontSize: 15,
    color: "44546A",
    margin: 0,
  });
  s7.addText("Master: cloudwise 2025 (true slide master mode)", {
    x: 1.55,
    y: 2.65,
    w: 7.7,
    h: 0.35,
    fontFace: FONT.alt,
    fontSize: 13,
    color: PALETTE.neutral,
    margin: 0,
  });

  const out = path.join(__dirname, "ppt-maker-intro-cloudwise-2025-mastered.pptx");
  await pres.writeFile({ fileName: out });
  console.log("Generated:", out);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
