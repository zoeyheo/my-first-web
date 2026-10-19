# POP 카드(9×5.5cm, 10px = 1mm)와 A4 인쇄용 시트를 생성
FONT = "Pretendard, 'Noto Sans KR', sans-serif"
OUTLINE = "#9E9E9E"  # 재단선(외곽선) 회색
ECG = "#BDBDBD"      # 장식용 심전도 파형(회색, 피그마에서 색 지정)

def card(x=0, y=0):
    return f'''<g transform="translate({x} {y})">
  <rect x="1" y="1" width="898" height="548" fill="#FFFFFF" stroke="{OUTLINE}" stroke-width="2"/>
  <text x="450" y="135" text-anchor="middle" font-family="{FONT}" font-size="38" font-weight="600" fill="#000000">헬스리안 (Healthrian)</text>
  <text x="450" y="262" text-anchor="middle" font-family="{FONT}" font-size="76" font-weight="800" letter-spacing="2" fill="#000000">CARDIO EM</text>
  <text x="450" y="370" text-anchor="middle" font-family="{FONT}" font-size="76" font-weight="500" fill="#000000">- 웨어러블 디바이스 -</text>
  <path d="M120 465 H360 L372 465 L380 455 L388 465 L400 465 L406 473 L418 425 L430 495 L438 465 L452 465 L464 452 L478 465 H780" fill="none" stroke="{ECG}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</g>'''

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'

# 단일 카드
open("healthrian_pop_90x55.svg", "w").write(svg(900, 550, "<!-- POP 카드 9 × 5.5cm (10px = 1mm) -->\n" + card()))

# A4(210×297mm) 시트: 2열 × 5행 = 10장, 가운데 정렬
W, H, COLS, ROWS = 2100, 2970, 2, 5
x0, y0 = (W - 900 * COLS) // 2, (H - 550 * ROWS) // 2
cards = "\n".join(card(x0 + c * 900, y0 + r * 550) for r in range(ROWS) for c in range(COLS))
a4 = svg(W, H, f'<!-- A4 210 × 297mm (10px = 1mm), 카드 {COLS * ROWS}장 -->\n<rect width="{W}" height="{H}" fill="#FFFFFF"/>\n' + cards)
open("healthrian_pop_A4.svg", "w").write(a4)

# A4 인쇄용 PDF (실제 크기 100%)
import os, subprocess, tempfile
with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
    f.write('<!doctype html><meta charset="utf-8"><style>@page{size:A4;margin:0}html,body{margin:0}svg{display:block;width:210mm;height:297mm}</style>\n' + a4)
subprocess.run([os.environ.get("CHROME", "chromium"), "--headless", "--no-sandbox", "--no-pdf-header-footer",
                "--print-to-pdf=healthrian_pop_A4.pdf", f.name], check=True, capture_output=True)
os.unlink(f.name)
