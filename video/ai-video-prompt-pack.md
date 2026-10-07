# CARDIO EM 시연 영상 · AI 영상 생성 프롬프트 팩

참고 이미지 2장(구급차 / 병실)의 톤을 기준으로, 스토리보드 10개 장면을 실사풍 AI 영상 도구(이미지→영상 지원 도구 권장)에서 뽑기 위한 지시문입니다.
영상 길이·해상도·지원 기능은 도구마다 다르므로 각 도구에서 확인해 주세요. (이 문서는 특정 도구의 기능을 검증하지 않았습니다.)

## 1. 스타일 바이블 (모든 장면 공통)

참고 이미지에서 읽히는 요소만 정리했습니다.

- **룩:** 실사 시네마틱, 얕은 심도(배경 약간 흐림), 35mm 느낌, 자연스러운 피부 질감, 과한 보정 없음
- **구급차 톤:** 어둑한 실내 + 창밖에서 들어오는 파랑·빨강 경광등 반사, 장비 선반(ALS 가방, 모니터), 노란 손잡이, 남색 유니폼의 구급대원 2인(남·여), 보라색 니트릴 장갑
- **병실 톤:** 큰 창으로 들어오는 부드러운 자연광, 도시 전경, 베이지·우드 가구, 리클라이닝 병상, 벽걸이 환자 모니터, 푸른 환자복의 중년 남성 환자
- **카메라:** 3인칭은 눈높이~약간 높은 앵글의 느린 푸시인/슬라이드, 1인칭은 어깨높이 시점(손이 화면 아래에서 들어옴)
- **색:** 구급차=차가운 청록·네이비 + 경광등 포인트, 병실=따뜻한 화이트·베이지. 한 영상 안에서 두 톤이 장면별로 분리되도록 유지

**공통 네거티브 프롬프트(권장):** cartoon, 3D render, illustration, extra fingers, distorted hands, garbled text, unreadable logos, warped medical devices, text overlays, subtitles, watermark, over-saturated

## 2. 제품 묘사 (매뉴얼 기준, 모든 프롬프트에 붙여 쓰기)

> a small white rounded-rectangular ECG sensor module with a thin blue "CARDIO EM" logo on its front face and one small status LED, sitting in a white adhesive electrode patch holder on the chest; a white limb-lead cable with four snap electrodes (white RA, black LA, green RL, red LL); a light-blue charging cradle

- 모듈의 작은 로고와 앱 화면 글자는 AI가 자주 깨뜨립니다. **생성 후 합성 단계에서 로고·UI를 올리는 것을 전제로** 하세요(아래 4장).
- 매뉴얼 근거: 구성품 p.6–11, 전극 부착 p.20–24, 앱 연결 p.25–28.

## 3. 장면별 프롬프트

각 장면은 5~8초 클립 2~4개를 이어 붙이는 것을 가정했습니다. 한 줄 영어 프롬프트는 도구에 붙여 넣는 용도이고, 한국어 연출 메모는 편집용입니다.

### S01 오프닝 · 3인칭 (병실 → 구급차 → 협진)
- **시작 프레임:** 참고 이미지 2(병실)를 그대로 첫 프레임으로 사용
- `Cinematic realistic hospital room, soft daylight through a large window, middle-aged male patient resting in an adjustable bed, wall-mounted patient monitor showing a clean ECG trace, a small white CARDIO EM sensor module on his chest, slow gentle push-in, shallow depth of field`
- 연출 메모: 자막 “병원에서만 받던 정밀 심전도 분석, 이제 어디서나 가볍게”. 이어서 구급차(참고 이미지 1), 병원 밖 협진 컷으로 와이프.

### S02 제품 구성 · 3인칭 (스튜디오)
- `Product shot on a clean white table, soft top light, slow 180-degree orbit: sensor module, light-blue charging cradle, white electrode patch with holder, limb-lead cable with four colored snaps, charging cable laid out neatly, macro detail, photorealistic`
- 연출 메모: 라벨(센서모듈·크래들·전극홀더·옵션)은 합성으로 추가. 옵션 품목은 점선 라벨.

### S03 사용 전 준비 · 1인칭
- `First-person POV, hands in blue nitrile gloves open a box on a table and pick up a small white sensor module, place it on a light-blue cradle, a small LED lights orange then turns green, shallow depth of field, realistic`
- 연출 메모: 충전 중 주황 → 완료 초록(매뉴얼 p.19). 이후 태블릿에서 ‘CARDIO PRO’ 설치 화면은 화면 녹화로 합성.

### S04 전극패치·홀더 조립 · 1인칭(탑뷰)
- `Top-down POV, gloved hands connect colored snap electrodes to a white limb-lead cable, peel the liner from a white adhesive electrode patch, press the white electrode holder onto the patch, clip the cable into the holder, clean tabletop, realistic macro`
- 연출 메모: 센서모듈은 전극이 흉부에 고정된 뒤 결합(매뉴얼 p.23).

### S05 환자에게 전극 부착 · 3인칭
- **시작 프레임:** 참고 이미지 1(구급차) 또는 2(병실)
- `Medium shot, a female paramedic in a navy uniform and purple gloves applies a white electrode patch to the bare chest of a male patient lying on a stretcher, then places four limb electrodes, then clicks the small white sensor module into the holder, realistic, ambulance interior with cool light and faint red-blue reflections`
- 연출 메모: 피부에 직접 접촉(옷 위 X). 건조한 피부는 닦은 뒤 부착(매뉴얼 p.35).

### S06 로그인·기기 연결 · 1인칭(태블릿)
- `First-person POV, two hands hold a rugged tablet, a finger taps the screen, the patient lying on a stretcher visible out of focus behind the tablet, realistic`
- 연출 메모: **화면은 반드시 합성**(실제 앱 녹화: 로그인 → 블루투스 연결 → CardioEM 선택 → ▶).

### S07 측정 시작 · 3인칭 + 화면 인서트
- `Over-the-shoulder shot of a paramedic looking at a rugged tablet showing a live multi-lead ECG, the patient calm on the stretcher, cool blue ambient light, shallow depth of field`
- 연출 메모: 전극 상태 빨강 → 초록 전환은 앱 화면 녹화로 합성(매뉴얼 p.27).

### S08 종료·저장·불러오기 · 1인칭
- `First-person POV, a gloved thumb taps the stop button on a tablet, then browses a list of saved recordings, realistic`
- 연출 메모: 화면 합성.

### S09 분석 기능 · 3인칭 + 화면
- `A cardiologist in a white coat reviews an ECG report on a large wall-mounted monitor in a bright modern clinic, pointing at the waveform, shallow depth of field, realistic`
- 연출 메모: 비트 분류(N·V·S·F·Q·X), 리듬 분류(AF/AFL), 경향성 그래프, ECG 스트립은 앱 화면으로 합성(매뉴얼 p.32–34).

### S10 구급차 이송 중 측정 · 혼합
- **시작 프레임:** 참고 이미지 1 그대로
- `Slow push-in on the paramedics treating the patient in the ambulance, flashing red and blue light reflecting through the window, a rugged tablet in the foreground showing live ECG, handheld micro-shake, cinematic realistic`
- 연출 메모: 이송 중 기록 저장·병원 공유 UI는 합성. 실시간 병원 전송 기능은 매뉴얼에 없으므로 “공유”로만 표현.

### S11 리포트 PDF·공유 · 1인칭 + 화면
- 화면 녹화 중심(PDF 아이콘 → ECG 용지 → PR·QRS·QT·QTc → 저장/공유).

### S12 클로징 · 3인칭
- `Close-up of a gloved hand detaching a small white sensor module and placing it on a light-blue cradle, then slow pull-back to reveal the ward, soft daylight, realistic`
- 엔드카드: “병원에서만 받던 정밀 심전도 분석, 이제 어디서나 가볍게.” + 로고 + 연락처

## 4. 합성·후반 작업 체크리스트

1. 모든 클립은 **같은 해상도·프레임레이트**로 뽑기 (예: 1920×1080, 24fps)
2. **모듈 로고(CARDIO EM)** 와 **앱 화면 UI**는 생성 영상 위에 추적(트래킹)해서 합성
3. 환자·인물 얼굴 일관성이 필요하면 같은 참고 이미지를 모든 클립의 시작 프레임으로 재사용
4. 자막은 `cardio-em-demo.ko.srt` / `.en.srt`를 장면 길이에 맞춰 조정해 사용
5. 실제 인물 모델·소품 사용 시 초상권·인허가 문구 확인 (“정밀” 등 성능 표현 근거 포함)
6. 음악·내레이션은 별도 제작 (성우 녹음 또는 TTS)

## 5. 이미 만들어 둔 합성 컷 (이 프롬프트 팩의 목표 톤 확인용)

`video/cardio-em-photo-look-cut.mp4` — 참고 이미지 2장 위에 CARDIO EM 센서모듈, 심전도 화면, 경광등 반사를 합성한 27초 컷입니다. 원본이 작은 이미지(약 720px)라 해상도는 낮습니다.
