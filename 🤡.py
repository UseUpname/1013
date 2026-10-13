"""조선 전생 장부 – 나의 엽전 일대기

streamlit run joseon_ledger.py

선택할 때마다 엽전이 들고 나는 '장부형' 전생 테스트.
두 갈래(모험 ↔ 안전, 씀씀이 ↔ 절약)를 조합해 네 가지 전생 신분이 나온다.
"""

import streamlit as st

st.set_page_config(
    page_title="조선 전생 장부",
    page_icon="🪙",
    layout="centered",
)

# ──────────────────────────────────────────────
# 한지 · 장부 감성 스타일
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');
    /* 글꼴은 글자에만 입히고, Streamlit 아이콘 글꼴은 건드리지 않는다
       (전체(*)에 덮어쓰면 펼치기 화살표가 'arrow_right' 글자로 깨져 보임) */
    html, body, .stApp, p, li, span, div, label, button, td, th, h1, h2, h3, h4 {
        font-family: 'Gowun Batang', serif;
    }
    [data-testid="stIconMaterial"], .material-symbols-rounded, .material-icons {
        font-family: 'Material Symbols Rounded' !important;
    }

    /* 한국어는 단어 중간에서 끊기지 않게 */
    .stApp { background-color: #f7f3eb; color: #2b1e1a; word-break: keep-all; overflow-wrap: break-word; }

    /* 제목 옆에 뜨는 🔗 링크 아이콘 숨김 */
    [data-testid="stHeaderActionElements"], .stMarkdown a.anchor-link { display: none !important; }

    /* 결과 제목 */
    .result-title {
        text-align: center; color: #5c3a21; font-weight: 700;
        font-size: clamp(1.3rem, 5vw, 1.75rem); line-height: 1.4; margin: 8px 0 4px 0;
    }
    .result-sub { text-align: center; color: #8b5a2b; font-weight: 700; font-size: 1rem; margin-bottom: 14px; }

    /* 결과 수치 상자 (긴 글자도 줄바꿈되도록 st.metric 대신 사용) */
    .stat-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 8px; }
    .stat {
        background: #fffdf9; border: 2px solid #d4a373; border-radius: 8px; padding: 12px 14px;
    }
    .stat .label { font-size: 0.82rem; color: #8b5a2b; margin-bottom: 4px; }
    .stat .value { font-size: 1.5rem; font-weight: 700; line-height: 1.3; }
    .stat .value.small { font-size: 1.05rem; line-height: 1.45; }
    .stat .note { font-size: 0.8rem; color: #7a6a5c; margin-top: 4px; }
    .neg { color: #a4161a; } .pos { color: #2d6a4f; }
    @media (max-width: 480px) { .stat-row { grid-template-columns: 1fr; } }

    .section-title { font-size: 1.15rem; font-weight: 700; margin: 18px 0 6px 0; color: #3c2a21; }
    .story { font-size: 1rem; line-height: 1.75; }

    /* 현판 */
    .hyeonpan {
        background: #3c2a21; color: #f4ece1;
        padding: 20px; border-radius: 6px;
        border: 4px double #8b5a2b;
        text-align: center; margin-bottom: 18px;
    }
    .hyeonpan h1 { font-size: 1.55rem !important; color: #ffb703; margin: 0 0 6px 0; }
    .hyeonpan p  { color: #d4c3b3; font-size: 0.92rem; margin: 0; }

    /* 상단 장부 잔액 띠 */
    .ledger-bar {
        display: flex; justify-content: space-between; align-items: center;
        background: #fffdf9; border: 2px solid #3c2a21; border-radius: 8px;
        padding: 10px 16px; margin-bottom: 14px;
    }
    .ledger-bar .coins { letter-spacing: 3px; font-size: 1.05rem; color: #bc6c25; }
    .ledger-bar .money { font-weight: 700; font-size: 1.15rem; color: #3c2a21; }

    /* 두루마리 질문 카드 */
    .scroll-card {
        background: #fffaf0;
        border-left: 10px solid #8b5a2b; border-right: 10px solid #8b5a2b;
        padding: 18px 22px; margin: 6px 0 16px 0; border-radius: 4px;
    }
    .scroll-card .scene { color: #8b5a2b; font-size: 0.85rem; margin-bottom: 6px; }
    .scroll-card h3 { margin: 0 !important; line-height: 1.5; }

    /* 세로로 쌓이는 선택 패찰 */
    div[class*="st-key-pick_"] button {
        border-radius: 4px !important;
        border: 2px solid #3c2a21 !important;
        background: #fffdf9 !important; color: #3c2a21 !important;
        min-height: 64px !important; height: auto !important;
        padding: 12px 18px !important;
        justify-content: flex-start !important; text-align: left !important;
        white-space: normal !important;
    }
    div[class*="st-key-pick_"] button p { white-space: normal !important; font-size: 1.0rem !important; }
    div[class*="st-key-pick_"] button:hover {
        background: #f1e4d3 !important; border-color: #8b5a2b !important;
    }

    /* 결과: 저울 게이지 */
    .gauge { margin: 10px 0 16px 0; }
    .gauge .labels { display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 700; }
    .gauge .track { position: relative; height: 14px; background: #e8d5c4; border-radius: 7px; margin-top: 4px; }
    .gauge .knob {
        position: absolute; top: -5px; width: 24px; height: 24px; margin-left: -12px;
        background: #ffb703; border: 3px solid #3c2a21; border-radius: 50%;
    }

    /* 결과: 장부 표 */
    table.jangbu { width: 100%; border-collapse: collapse; background: #fffdf9; font-size: 0.92rem; }
    table.jangbu th, table.jangbu td { border: 1px solid #c9b29b; padding: 6px 8px; }
    table.jangbu th { background: #3c2a21; color: #f4ece1; }
    table.jangbu td.plus  { color: #2d6a4f; text-align: right; font-weight: 700; }
    table.jangbu td.minus { color: #a4161a; text-align: right; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

START_COIN = 100

# ──────────────────────────────────────────────
# 문항: 선택마다 '갈래 기울기(lean)'와 '엽전 증감(coin)'이 붙는다
#   risk  갈래: +1 모험, -1 안전
#   spend 갈래: +1 씀씀이, -1 절약
# ──────────────────────────────────────────────
QUESTIONS = [
    {
        "scene": "🏺 봄 · 집 마당", "axis": "risk", "category": "여윳돈 관리",
        "prompt": "여윳돈 100냥이 생겼다! 어떻게 지킬까?",
        "options": [
            {"text": "땅을 파고 항아리에 엽전을 꽁꽁 숨겨둔다", "lean": -1, "coin": 0, "memo": "항아리에 묻음"},
            {"text": "장사하는 친구에게 빌려주고 이자를 받아낸다", "lean": +1, "coin": 40, "memo": "친구 이자 수입"},
        ],
    },
    {
        "scene": "👞 봄 · 저잣거리", "axis": "spend", "category": "소비 습관",
        "prompt": "눈에 쏙 들어오는 명품 비단신을 발견했다!",
        "options": [
            {"text": "실속형 짚신이면 충분하다, 눈길도 안 준다", "lean": -1, "coin": 10, "memo": "짚신으로 버팀"},
            {"text": "품위도 자기 투자! 기꺼이 지갑을 연다", "lean": +1, "coin": -30, "memo": "비단신 구입"},
        ],
    },
    {
        "scene": "🌾 여름 · 흉년", "axis": "risk", "category": "위기 대처",
        "prompt": "흉년으로 장사 수입이 반토막 났다. 어떻게 할까?",
        "options": [
            {"text": "불필요한 지출을 끊고 허리띠를 바짝 졸라맨다", "lean": -1, "coin": -10, "memo": "흉년 버티기"},
            {"text": "새 살림 도구나 유통 품목을 찾아 돌파구를 연다", "lean": +1, "coin": 30, "memo": "새 품목 개척"},
        ],
    },
    {
        "scene": "🧺 여름 · 논두렁", "axis": "spend", "category": "품삯",
        "prompt": "고된 논일을 끝낸 일꾼들에게 품삯을 줄 때 나는?",
        "options": [
            {"text": "오늘 일한 만큼 칼같이 계산해서 준다", "lean": -1, "coin": -15, "memo": "품삯 정산"},
            {"text": "앞으로의 신뢰를 보고 넉넉히 얹어준다", "lean": +1, "coin": -25, "memo": "품삯 + 웃돈"},
        ],
    },
    {
        "scene": "📯 여름 · 소문", "axis": "risk", "category": "정보 활용",
        "prompt": "'어느 고을 특산품 값이 폭등한다'는 소문이 돈다!",
        "options": [
            {"text": "뜬소문일지 몰라, 내 논밭 일에만 집중한다", "lean": -1, "coin": 10, "memo": "논밭 수확"},
            {"text": "보부상 줄을 통해 진위를 캐고 바로 움직인다", "lean": +1, "coin": 50, "memo": "특산품 차익"},
        ],
    },
    {
        "scene": "🏚 가을 · 객주", "axis": "risk", "category": "빚과 신용",
        "prompt": "객주 주인에게 급히 돈을 빌려야 할 일이 생겼다면?",
        "options": [
            {"text": "아쉬운 소리도, 빚도 질색이다", "lean": -1, "coin": 0, "memo": "빚 없음"},
            {"text": "신용도 자산! 계획을 세워 빌린 돈을 굴린다", "lean": +1, "coin": 60, "memo": "빌린 돈 굴린 이문"},
        ],
    },
    {
        "scene": "🏡 가을 · 이사철", "axis": "spend", "category": "집 고르기",
        "prompt": "살 집을 고르는 가장 중요한 기준은?",
        "options": [
            {"text": "텃밭 딸린 정겨운 초가집이면 족하다", "lean": -1, "coin": 20, "memo": "텃밭 채소 수입"},
            {"text": "번듯한 기와집이 체면이고 자산이다", "lean": +1, "coin": -50, "memo": "기와집 수리비"},
        ],
    },
    {
        "scene": "⛵ 가을 · 서해 뱃길", "axis": "risk", "category": "모험 무역",
        "prompt": "청나라 무역선을 탔는데 폭풍우를 만났다!",
        "options": [
            {"text": "역시 모험은 아니었어… 다음엔 내 땅만 믿는다", "lean": -1, "coin": 0, "memo": "무사 귀환"},
            {"text": "위험이 클수록 이문도 크다! 끝까지 버틴다", "lean": +1, "coin": -40, "memo": "폭풍에 짐 일부 유실"},
        ],
    },
    {
        "scene": "📒 겨울 · 사랑방", "axis": "spend", "category": "장부 정리",
        "prompt": "한 달 엽전 장부를 들여다보는 나의 모습은?",
        "options": [
            {"text": "한 푼 오차도 없이 대조하고 반성한다", "lean": -1, "coin": 15, "memo": "새는 돈 막음"},
            {"text": "큰 틀에서 흑자면 그만, 대충 훑는다", "lean": +1, "coin": -20, "memo": "어디 갔는지 모를 돈"},
        ],
    },
    {
        "scene": "⛏ 겨울 · 마을 회의", "axis": "risk", "category": "동업 제안",
        "prompt": "이웃이 '대박 금광 사업'을 같이 하자고 한다!",
        "options": [
            {"text": "눈에 보이는 곡식과 땅이 아니면 안 믿는다", "lean": -1, "coin": 10, "memo": "곡식 저장"},
            {"text": "성장 가능성을 따져보고 과감히 투자한다", "lean": +1, "coin": 100, "memo": "금광 지분 배당"},
        ],
    },
    {
        "scene": "🍵 노년 · 은퇴", "axis": "spend", "category": "노후",
        "prompt": "은퇴 후 꿈꾸는 노후는?",
        "options": [
            {"text": "논 몇 마지기 물려주고 조용히 시골살이", "lean": -1, "coin": 20, "memo": "소박한 노후"},
            {"text": "큰 가옥에서 손님 치르며 넉넉하게", "lean": +1, "coin": -40, "memo": "잔치 비용"},
        ],
    },
    {
        "scene": "🪙 마지막 장", "axis": "spend", "category": "돈의 의미",
        "prompt": "내 인생에서 엽전이란?",
        "options": [
            {"text": "땀 흘린 정직한 대가, 가족을 지키는 도구", "lean": -1, "coin": 10, "memo": "가족 비상금"},
            {"text": "쓰라고 있는 것! 써야 세상이 돈다", "lean": +1, "coin": -10, "memo": "인심 쓰기"},
        ],
    },
]


def face_svg(bg, ring, hat_color, hat_shape):
    """전생 신분별 얼굴. hat_shape: gat(갓) / satgat(삿갓) / dugeon(두건) / sugeon(머릿수건)"""
    hats = {
        "gat": f'<polygon points="50,14 32,34 68,34" fill="{hat_color}"/>'
               f'<rect x="14" y="32" width="72" height="5" rx="2" fill="{hat_color}"/>',
        "satgat": f'<polygon points="50,10 10,38 90,38" fill="{hat_color}"/>',
        "dugeon": f'<path d="M 26 40 Q 50 8 74 40 Z" fill="{hat_color}"/>',
        "sugeon": f'<rect x="24" y="30" width="52" height="9" rx="4" fill="{hat_color}"/>'
                  f'<circle cx="78" cy="35" r="4" fill="{hat_color}"/>',
    }
    return f"""
    <svg width="140" height="140" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="52" r="45" fill="{bg}" stroke="{ring}" stroke-width="3"/>
      <circle cx="50" cy="60" r="23" fill="#fcd5ce"/>
      {hats[hat_shape]}
      <circle cx="41" cy="58" r="3" fill="#2b1e1a"/>
      <circle cx="59" cy="58" r="3" fill="#2b1e1a"/>
      <circle cx="35" cy="64" r="3.5" fill="#ffb5a7" opacity="0.7"/>
      <circle cx="65" cy="64" r="3.5" fill="#ffb5a7" opacity="0.7"/>
      <path d="M 44 68 Q 50 73 56 68" stroke="#2b1e1a" stroke-width="2" fill="none" stroke-linecap="round"/>
    </svg>"""


# (risk 갈래, spend 갈래) → 전생 신분
TYPES = {
    ("안전", "절약"): {
        "title": "곳간지기 농부 🌾",
        "sub": "한 톨도 허투루 안 쓰는 든든한 살림꾼",
        "desc": "땅과 곡식처럼 눈에 보이는 것만 믿고, 들어온 엽전은 꼭꼭 쌓아두던 사람입니다. "
                "흉년이 와도 마을에서 가장 늦게 굶는 집이 바로 당신 집이었죠.",
        "tip": "가끔은 이웃 장사꾼 이야기에도 귀를 열어보세요. 곳간 문을 반 뼘만 열어도 볕이 듭니다.",
        "svg": face_svg("#e8d5c4", "#8b5a2b", "#a0522d", "satgat"),
    },
    ("안전", "씀씀이"): {
        "title": "체면 지키는 양반 나리 🎐",
        "sub": "재산은 안전하게, 쓰는 건 품위 있게",
        "desc": "위험한 장사엔 손대지 않지만 비단신과 기와집, 손님 대접만큼은 아끼지 않던 사람입니다. "
                "곳간보다 사랑방이 더 붐비던 집이었죠.",
        "tip": "들어오는 길은 좁은데 나가는 길이 넓어요. 장부 한 번만 들여다보면 체면도 곳간도 지킬 수 있습니다.",
        "svg": face_svg("#e3eaf2", "#4a5d73", "#2b1e1a", "gat"),
    },
    ("모험", "절약"): {
        "title": "발로 뛰는 보부상 🎒",
        "sub": "소문은 빠르게, 지갑은 단단하게",
        "desc": "등짐을 지고 팔도를 누비며 남보다 먼저 시세를 읽던 사람입니다. "
                "번 돈은 허투루 쓰지 않고 다음 장사 밑천으로 돌렸죠.",
        "tip": "기회를 보는 눈과 아끼는 손을 다 가졌어요. 다만 몸이 밑천이니 쉬는 것도 투자랍니다.",
        "svg": face_svg("#e6f0e1", "#52734d", "#52734d", "dugeon"),
    },
    ("모험", "씀씀이"): {
        "title": "판을 키우는 거상 💰",
        "sub": "크게 벌고 크게 쓰는 저잣거리의 큰손",
        "desc": "금광이든 무역선이든 판이 크면 일단 뛰어들고, 번 만큼 화끈하게 쓰던 사람입니다. "
                "객주마다 당신 이름 석 자 모르는 사람이 없었죠.",
        "tip": "들고 나는 폭이 큰 만큼 비상금 항아리 하나쯤은 따로 묻어두세요.",
        "svg": face_svg("#faedcd", "#d4a373", "#bc6c25", "sugeon"),
    },
}


def wealth_tier(coin):
    if coin < 0:
        return "📜 객주에 빚 문서가 남은 살림"
    if coin <= 60:
        return "🫙 바닥 보이는 엽전 꾸러미"
    if coin <= 150:
        return "🧺 소박하지만 굶진 않는 살림"
    if coin <= 250:
        return "🏚 넉넉한 곳간"
    return "🏯 만석꾼 부럽지 않은 금고"


# ──────────────────────────────────────────────
# 상태: 고른 선택지 번호를 순서대로 쌓는 '장부(history)' 하나로 관리
# ──────────────────────────────────────────────
st.session_state.setdefault("history", [])
st.session_state.setdefault("last_entry", None)
history = st.session_state.history


def balance(hist):
    return START_COIN + sum(QUESTIONS[i]["options"][c]["coin"] for i, c in enumerate(hist))


def signed(n):
    return f"+{n}" if n > 0 else str(n)


def reset():
    st.session_state.history = []
    st.session_state.last_entry = None


st.markdown(
    """
    <div class="hyeonpan">
        <h1>🪙 조선 전생 장부 🪙</h1>
        <p>열두 장의 장부를 넘기며 엽전을 벌고 써보세요. 마지막 잔액이 당신의 전생 재산입니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# 문항 화면
# ──────────────────────────────────────────────
if len(history) < len(QUESTIONS):
    idx = len(history)
    q = QUESTIONS[idx]
    coins = "●" * idx + "○" * (len(QUESTIONS) - idx)

    st.markdown(
        f"""
        <div class="ledger-bar">
            <span class="coins">{coins}</span>
            <span class="money">잔액 {balance(history)}냥</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.last_entry:
        memo, coin = st.session_state.last_entry
        st.caption(f"📜 방금 적힌 장부: {memo} ({signed(coin)}냥)")

    st.markdown(
        f"""
        <div class="scroll-card">
            <div class="scene">{q['scene']} · {idx + 1}장 / {len(QUESTIONS)}장</div>
            <h3>{q['prompt']}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 고르면 바로 다음 장으로 넘어간다
    for i, opt in enumerate(q["options"]):
        if st.button(f"🖌 {opt['text']}", key=f"pick_{idx}_{i}", use_container_width=True):
            history.append(i)
            st.session_state.last_entry = (opt["memo"], opt["coin"])
            st.rerun()

    if history:
        st.write("")
        if st.button("↩ 방금 적은 장부 지우기", key="undo"):
            history.pop()
            st.session_state.last_entry = None
            st.rerun()

# ──────────────────────────────────────────────
# 결과 화면
# ──────────────────────────────────────────────
else:
    risk = sum(QUESTIONS[i]["options"][c]["lean"] for i, c in enumerate(history) if QUESTIONS[i]["axis"] == "risk")
    spend = sum(QUESTIONS[i]["options"][c]["lean"] for i, c in enumerate(history) if QUESTIONS[i]["axis"] == "spend")
    n_risk = sum(1 for q in QUESTIONS if q["axis"] == "risk")
    n_spend = sum(1 for q in QUESTIONS if q["axis"] == "spend")

    key = ("모험" if risk > 0 else "안전", "씀씀이" if spend > 0 else "절약")
    t = TYPES[key]
    final = balance(history)

    st.markdown(f"<div style='text-align:center'>{t['svg']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='result-title'>전생의 당신은<br>{t['title']}</div>"
        f"<div class='result-sub'>{t['sub']}</div>",
        unsafe_allow_html=True,
    )

    diff = final - START_COIN
    tier_icon, tier_name = wealth_tier(final).split(" ", 1)
    st.markdown(
        f"""
        <div class="stat-row">
            <div class="stat">
                <div class="label">최종 잔액</div>
                <div class="value {'neg' if final < 0 else ''}">{final:,}냥</div>
                <div class="note">시작 {START_COIN}냥에서 <span class="{'neg' if diff < 0 else 'pos'}">{signed(diff)}냥</span></div>
            </div>
            <div class="stat">
                <div class="label">재산 등급</div>
                <div class="value small">{tier_icon} {tier_name}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>⚖️ 두 갈래 저울</div>", unsafe_allow_html=True)

    def gauge(left, right, score, total):
        pos = (score + total) / (2 * total) * 100
        return f"""
        <div class="gauge">
            <div class="labels"><span>{left}</span><span>{right}</span></div>
            <div class="track"><div class="knob" style="left:{pos:.0f}%"></div></div>
        </div>"""

    st.markdown(
        gauge("🛡 안전", "모험 🌊", risk, n_risk) + gauge("🧮 절약", "씀씀이 🎁", spend, n_spend),
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='section-title'>📜 전생 이야기</div><div class='story'>{t['desc']}</div>",
        unsafe_allow_html=True,
    )
    st.write("")
    st.info(f"💡 {t['tip']}")

    with st.expander("📒 한 해 동안의 장부 펼쳐보기"):
        rows = []
        for i, c in enumerate(history):
            q = QUESTIONS[i]
            opt = q["options"][c]
            cls = "plus" if opt["coin"] >= 0 else "minus"
            rows.append(
                f"<tr><td>{q['scene']}</td><td>{opt['memo']}</td>"
                f"<td class='{cls}'>{signed(opt['coin'])}</td></tr>"
            )
        st.markdown(
            "<table class='jangbu'><tr><th>때·곳</th><th>적요</th><th>냥</th></tr>"
            f"<tr><td>시작</td><td>물려받은 밑천</td><td class='plus'>{START_COIN}</td></tr>"
            + "".join(rows)
            + f"<tr><td colspan='2'><b>합계</b></td><td class='{"plus" if final >= 0 else "minus"}'><b>{final}</b></td></tr></table>",
            unsafe_allow_html=True,
        )

    st.divider()
    if st.button("🔄 새 장부로 다시 살아보기", use_container_width=True, key="restart"):
        reset()
        st.rerun()