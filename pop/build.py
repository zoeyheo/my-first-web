# POP 카드(9×5.5cm, 10px = 1mm)와 A4 인쇄용 시트를 제품별로 생성
import os, subprocess, tempfile

FONT = "Pretendard, 'Noto Sans KR', sans-serif"
OUTLINE = "#9E9E9E"  # 재단선(외곽선) 회색

# (파일 이름, 회사명, 제품명, 분류)
PRODUCTS = [
    ("healthrian", "헬스리안 (Healthrian)", "CARDIO EM", "- 웨어러블 디바이스 -"),
    ("geronx", "제론엑스 (Geron X)", "늘밴드 (NEUL Band)", "- 웨어러블 디바이스 -"),
]

def card(company, product, category, x=0, y=0):
    return f'''<g transform="translate({x} {y})">
  <rect x="1" y="1" width="898" height="548" fill="#FFFFFF" stroke="{OUTLINE}" stroke-width="2"/>
  <text x="450" y="153" text-anchor="middle" font-family="{FONT}" font-size="38" font-weight="600" fill="#000000">{company}</text>
  <text x="450" y="293" text-anchor="middle" font-family="{FONT}" font-size="76" font-weight="800" fill="#000000">{product}</text>
  <text x="450" y="413" text-anchor="middle" font-family="{FONT}" font-size="76" font-weight="500" fill="#000000">{category}</text>
</g>'''

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'

# A4(210×297mm) 시트: 2열 × 5행 = 10장, 가운데 정렬
W, H, COLS, ROWS = 2100, 2970, 2, 5
x0, y0 = (W - 900 * COLS) // 2, (H - 550 * ROWS) // 2

for name, *text in PRODUCTS:
    # 단일 카드
    open(f"{name}_pop_90x55.svg", "w").write(svg(900, 550, "<!-- POP 카드 9 × 5.5cm (10px = 1mm) -->\n" + card(*text)))

    # A4 시트
    cards = "\n".join(card(*text, x0 + c * 900, y0 + r * 550) for r in range(ROWS) for c in range(COLS))
    a4 = svg(W, H, f'<!-- A4 210 × 297mm (10px = 1mm), 카드 {COLS * ROWS}장 -->\n<rect width="{W}" height="{H}" fill="#FFFFFF"/>\n' + cards)
    open(f"{name}_pop_A4.svg", "w").write(a4)

    # A4 인쇄용 PDF (실제 크기 100%)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write('<!doctype html><meta charset="utf-8"><style>@page{size:A4;margin:0}html,body{margin:0}svg{display:block;width:210mm;height:297mm}</style>\n' + a4)
    subprocess.run([os.environ.get("CHROME", "chromium"), "--headless", "--no-sandbox", "--no-pdf-header-footer",
                    f"--print-to-pdf={name}_pop_A4.pdf", f.name], check=True, capture_output=True)
    os.unlink(f.name)
