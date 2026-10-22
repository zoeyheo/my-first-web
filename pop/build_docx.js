// POP 카드(9×5.5cm)를 A4 Word 문서에 한 행 2장씩 배치
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, HeightRule, BorderStyle, VerticalAlign, AlignmentType, TableLayoutType,
} = require("docx");

const mm = (v) => Math.round((v / 25.4) * 1440); // mm → DXA
const FONT = { ascii: "Pretendard", hAnsi: "Pretendard", eastAsia: "Pretendard", cs: "Pretendard" };
const OUTLINE = { style: BorderStyle.SINGLE, size: 4, color: "9E9E9E" }; // 재단선 0.5pt 회색

// [회사명, 제품명(한글), 제품명(영문), 분류]
const CARDS = [
  ["헬스리안 (Healthrian)", "카디오 이엠", "(CARDIO EM)", "- Sensor Module -"],
  ["헬스리안 (Healthrian)", "카디오 이엠", "(CARDIO EM)", "- Patch & Holder -"],
  ["헬스리안 (Healthrian)", "카디오 이엠", "(CARDIO EM)", "- Cradle & Cable -"],
  ["헬스리안 (Healthrian)", "심혈관 모니터링용 센서 칩", "(AP1601)", "- ECG/APW Sensor IC -"],
  ["헬스리안 (Healthrian)", "다주파 생체 임피던스 칩", "(BIA_V3)", "- Multi-frequency BIA SoC -"],
  ["제론엑스 (Geron X)", "늘밴드", "(NEUL Band)", "- Wearable Device -"],
  ["제론엑스 (Geron X)", "늘허브", "(NEUL Hub)", "- IoT Sensor -"],
  ["하티브 (HATIV)", "하티브 심전계 P30", "(HATIV P30)", "- Wearable Device -"],
  ["하티브 (HATIV)", "하티브 심전계 K30", "(HATIV K30)", "- Kiosk-type Device -"],
  ["하티브 (HATIV)", "하티브 발목집게전극 E", "(HATIV E)", "- ECG Limb Electrode -"],
];

const CARD_W = mm(90), CARD_H = mm(55), COLS = 2;
const GAP = mm(2); // 카드 사이 간격 (재단선이 옆 카드와 붙지 않도록)
const NONE = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };

const line = (text, size, bold, after) =>
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after, line: 264, lineRule: "auto" },
    children: [new TextRun({ text, size: size * 2, bold, font: FONT, color: "000000" })],
  });

const card = ([company, nameKo, nameEn, category]) =>
  new TableCell({
    width: { size: CARD_W, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 0, bottom: 0, left: mm(2), right: mm(2) },
    borders: { top: OUTLINE, bottom: OUTLINE, left: OUTLINE, right: OUTLINE },
    children: [
      line(company, 9, true, 120),
      line(nameKo, 20, true, 0),
      line(nameEn, 20, true, 100),
      line(category, 16, false, 0),
    ],
  });

// 간격용 빈 칸 (테두리 없음)
const spacer = (width) =>
  new TableCell({
    width: { size: width, type: WidthType.DXA },
    margins: { top: 0, bottom: 0, left: 0, right: 0 },
    borders: { top: NONE, bottom: NONE, left: NONE, right: NONE },
    children: [new Paragraph({ spacing: { before: 0, after: 0, line: 20, lineRule: "exact" }, children: [new TextRun({ text: "", size: 2 })] })],
  });

// 열 구성: 카드 | 간격 | 카드
const columnWidths = Array.from({ length: COLS * 2 - 1 }, (_, i) => (i % 2 ? GAP : CARD_W));
const TABLE_W = CARD_W * COLS + GAP * (COLS - 1);

const rows = [];
for (let i = 0; i < CARDS.length; i += COLS) {
  if (i > 0) // 행 사이 간격
    rows.push(new TableRow({ height: { value: GAP, rule: HeightRule.EXACT }, children: columnWidths.map(spacer) }));
  const cards = CARDS.slice(i, i + COLS);
  while (cards.length < COLS) cards.push(["", "", "", ""]); // 홀수일 때 빈 칸
  const cells = cards.flatMap((c, j) => (j ? [spacer(GAP), card(c)] : [card(c)]));
  rows.push(new TableRow({ height: { value: CARD_H, rule: HeightRule.EXACT }, cantSplit: true, children: cells }));
}

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        // 카드 영역 182 × 283mm(간격 포함)를 가운데 배치 (아래 여백은 표 뒤 필수 문단 자리 확보용으로 조금 작게)
        margin: { top: mm(7), bottom: mm(6), left: mm(14), right: mm(14), header: 0, footer: 0 },
      },
    },
    children: [
      new Table({
        width: { size: TABLE_W, type: WidthType.DXA },
        columnWidths,
        layout: TableLayoutType.FIXED,
        rows,
      }),
      // Word는 표 뒤에 문단이 반드시 필요 → 빈 페이지가 생기지 않도록 1pt로 최소화
      new Paragraph({ spacing: { before: 0, after: 0, line: 20, lineRule: "exact" }, children: [new TextRun({ text: "", size: 2 })] }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => fs.writeFileSync("pop_cards_A4.docx", buf));
