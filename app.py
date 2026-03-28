import streamlit as st
import time

# ── 페이지 설정 ──
st.set_page_config(
    page_title="마이타임",
    page_icon="⏱",
    layout="wide",
)

# ── 세션 상태 초기화 ──
def init_state():
    defaults = {
        "coins": 0,
        "theme": "dark",   # dark / light / ocean
        "todos": [
            {"id": 1, "text": "오늘 수학 숙제 하기", "done": False},
            {"id": 2, "text": "영어 단어 20개 외우기", "done": False},
            {"id": 3, "text": "운동 30분", "done": False},
        ],
        "next_id": 4,
        "active_pet": None,
        "owned_pets": [],
        "owned_items": [],
        "study_sessions": 0,
        "total_minutes": 0,
        "pomo_running": False,
        "pomo_is_study": True,
        "pomo_seconds": 25 * 60,
        "pomo_start_time": None,
        "pomo_elapsed": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── 테마 색상 정의 ──
THEMES = {
    "dark": {
        "bg":        "#0e0f18",
        "surface":   "#161824",
        "surface2":  "#1e2035",
        "border":    "#2a2e50",
        "text":      "#e8eaf0",
        "muted":     "#6b7090",
        "btn_bg":    "#1e2035",
        "btn_hover": "#252a45",
        "input_bg":  "#161824",
    },
    "light": {
        "bg":        "#f4f5fb",
        "surface":   "#ffffff",
        "surface2":  "#eef0f8",
        "border":    "#d0d4e8",
        "text":      "#1a1d35",
        "muted":     "#7a80a0",
        "btn_bg":    "#eef0f8",
        "btn_hover": "#e0e4f0",
        "input_bg":  "#ffffff",
    },
    "ocean": {
        "bg":        "#071420",
        "surface":   "#0d2030",
        "surface2":  "#0f2840",
        "border":    "#1a4060",
        "text":      "#d0eeff",
        "muted":     "#5a90b0",
        "btn_bg":    "#0f2840",
        "btn_hover": "#1a3a55",
        "input_bg":  "#0d2030",
    },
}

T = THEMES[st.session_state.theme]

# ── 다이나믹 CSS ──
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Noto Sans KR', sans-serif !important;
}}
.stApp {{
    background: {T['bg']} !important;
    color: {T['text']} !important;
    transition: background 0.4s ease, color 0.4s ease;
}}
[data-testid="stHeader"] {{ background: transparent !important; }}

.logo-text {{ font-size: 24px; font-weight: 900; color: #f5a623; letter-spacing: -0.5px; }}
.logo-icon {{
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, #e06b3a, #f5a623);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}}
.coin-badge {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {T['surface2']}; border: 1px solid {T['border']};
    padding: 8px 18px; border-radius: 999px;
    font-size: 18px; font-weight: 700; color: #f5c842;
    box-shadow: 0 0 12px #f5c84220;
    float: right;
}}
.card {{
    background: {T['surface']};
    border: 1.5px solid {T['border']};
    border-radius: 14px; padding: 18px 20px;
    margin-bottom: 12px;
    transition: background 0.4s, border-color 0.2s;
}}
.card:hover {{ border-color: {T['muted']}; }}
.card-done {{ opacity: .5; }}
.section-title {{ font-size: 22px; font-weight: 800; margin-bottom: 6px; color: {T['text']}; }}
.section-sub {{ font-size: 13px; color: {T['muted']}; margin-bottom: 20px; }}
.timer-big {{
    font-size: 80px; font-weight: 900;
    letter-spacing: -4px; color: {T['text']};
    text-align: center; line-height: 1;
    font-variant-numeric: tabular-nums;
}}
.timer-mode {{ text-align: center; font-size: 16px; font-weight: 500; margin-top: 8px; margin-bottom: 24px; }}
.mode-study {{ color: #4e7fff; }}
.mode-rest  {{ color: #22c984; }}

/* Streamlit 요소 */
.stButton > button {{
    background: {T['btn_bg']} !important; color: {T['text']} !important;
    border: 1.5px solid {T['border']} !important; border-radius: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important; font-weight: 600 !important;
    transition: all .2s !important;
}}
.stButton > button:hover {{
    border-color: #4e7fff !important; background: {T['btn_hover']} !important;
}}
.stTextInput > div > div > input {{
    background: {T['input_bg']} !important; color: {T['text']} !important;
    border: 1.5px solid {T['border']} !important; border-radius: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: #4e7fff !important; box-shadow: 0 0 0 1px #4e7fff !important;
}}
.stProgress > div > div > div {{ background: linear-gradient(90deg, #22c984, #a0f0c0) !important; }}
div[data-testid="stMetricValue"] {{ color: #f5a623 !important; font-weight: 800 !important; }}
[data-testid="stMetricLabel"] {{ color: {T['muted']} !important; }}
label {{ color: {T['text']} !important; }}
.stTabs [data-baseweb="tab-list"] {{ background: {T['surface2']} !important; border-radius: 12px !important; }}
.stTabs [data-baseweb="tab"] {{ color: {T['muted']} !important; }}
.stTabs [aria-selected="true"] {{ color: {T['text']} !important; background: {T['surface']} !important; border-radius: 8px !important; }}
div[data-testid="stNotification"] {{ background: {T['surface2']} !important; color: {T['text']} !important; }}
</style>
""", unsafe_allow_html=True)

# ── 데이터 ──
SHOP_ITEMS = [
    {"id": "bg1",    "icon": "🌙", "name": "다크문 테마",  "desc": "차분한 달빛 배경",   "price": 10},
    {"id": "bg2",    "icon": "🌊", "name": "오션 테마",    "desc": "편안한 파도 배경",   "price": 15},
    {"id": "boost1", "icon": "⚡", "name": "집중 부스터",  "desc": "다음 뽀모 코인 2배", "price": 8},
    {"id": "deco1",  "icon": "🎵", "name": "집중 음악",    "desc": "백색소음 활성화",    "price": 12},
]
ALL_PETS = [
    {"id": "cat",    "emoji": "🐱", "name": "고양이", "trait": "호기심이 많고 독립적이에요", "price": 20},
    {"id": "dog",    "emoji": "🐶", "name": "강아지", "trait": "활발하고 충성스러워요",     "price": 20},
    {"id": "rabbit", "emoji": "🐰", "name": "토끼",   "trait": "조용하고 귀여워요",         "price": 25},
    {"id": "dragon", "emoji": "🐲", "name": "드래곤", "trait": "희귀하고 강력해요",         "price": 50},
]

# ── 헤더 ──
h1, h2, h3 = st.columns([3, 4, 3])
with h1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:10px 0">
      <div class="logo-icon">⏱</div>
      <div class="logo-text">마이타임</div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    # 테마 토글 버튼
    tc1, tc2, tc3 = st.columns(3)
    themes = [("dark", "🌙 다크"), ("light", "☀️ 라이트"), ("ocean", "🌊 오션")]
    for col, (tid, label) in zip([tc1, tc2, tc3], themes):
        with col:
            if st.button(label, use_container_width=True, key=f"theme_{tid}"):
                st.session_state.theme = tid
                st.rerun()

with h3:
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-end;padding:8px 0">
      <span class="coin-badge">🪙 {st.session_state.coins} 코인</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"<hr style='border:none;border-top:1px solid {T['border']};margin:8px 0 24px'>", unsafe_allow_html=True)

# ── 탭 ──
tab1, tab2, tab3, tab4 = st.tabs(["✅  할일", "🍅  뽀모도로", "🏪  상점", "🐾  펫"])


# ════════════════════════════════
# TAB 1 — 할일
# ════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">할일 체크리스트</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">완료하면 🪙 2 코인 획득!</div>', unsafe_allow_html=True)

    todos      = st.session_state.todos
    done_count = sum(1 for td in todos if td["done"])
    total_count= len(todos)
    progress   = done_count / total_count if total_count else 0

    cp, cl = st.columns([5, 1])
    with cp: st.progress(progress)
    with cl: st.markdown(f"<div style='color:{T['muted']};font-size:14px;padding-top:6px'>{done_count} / {total_count}</div>", unsafe_allow_html=True)

    ci, cb = st.columns([5, 1])
    with ci:
        new_todo = st.text_input("", placeholder="할일을 입력하세요...", label_visibility="collapsed", key="todo_input")
    with cb:
        if st.button("+ 추가", use_container_width=True, key="add_todo_btn"):
            if new_todo.strip():
                st.session_state.todos.append({"id": st.session_state.next_id, "text": new_todo.strip(), "done": False})
                st.session_state.next_id += 1
                st.rerun()

    st.divider()

    for i, todo in enumerate(st.session_state.todos):
        c1, c2, c3 = st.columns([1, 8, 1])
        with c1:
            if not todo["done"]:
                if st.button("⬜", key=f"check_{todo['id']}"):
                    st.session_state.todos[i]["done"] = True
                    st.session_state.coins += 2
                    st.toast("✅ 완료! +2 코인 획득 🎉")
                    st.rerun()
            else:
                st.button("✅", key=f"checked_{todo['id']}", disabled=True)
        with c2:
            style = f"text-decoration:line-through;color:{T['muted']};" if todo["done"] else f"color:{T['text']};"
            st.markdown(f"<div style='{style}font-size:15px;padding-top:8px'>{todo['text']}</div>", unsafe_allow_html=True)
        with c3:
            if st.button("✕", key=f"del_{todo['id']}"):
                st.session_state.todos = [td for td in st.session_state.todos if td["id"] != todo["id"]]
                st.rerun()


# ════════════════════════════════
# TAB 2 — 뽀모도로
# ════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">뽀모도로 타이머</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">공부 완료 시 🪙 5 코인 획득!</div>', unsafe_allow_html=True)

    STUDY_SEC = 25 * 60
    REST_SEC  = 5 * 60
    ss = st.session_state

    if ss.pomo_running and ss.pomo_start_time:
        elapsed   = time.time() - ss.pomo_start_time + ss.pomo_elapsed
        total_s   = STUDY_SEC if ss.pomo_is_study else REST_SEC
        remaining = max(0, total_s - elapsed)
        if remaining <= 0:
            ss.pomo_running = False; ss.pomo_start_time = None; ss.pomo_elapsed = 0
            if ss.pomo_is_study:
                ss.study_sessions += 1; ss.total_minutes += 25; ss.coins += 5
                st.toast("🍅 뽀모도로 완료! +5 코인 획득!")
            else:
                st.toast("⏰ 휴식 끝! 다시 집중해봐요 💪")
            ss.pomo_is_study = not ss.pomo_is_study
            ss.pomo_seconds  = STUDY_SEC if ss.pomo_is_study else REST_SEC
            remaining = ss.pomo_seconds
    else:
        remaining = ss.pomo_seconds

    mins = int(remaining) // 60
    secs = int(remaining) % 60
    mode_label = "공부 중 📚" if ss.pomo_is_study else "휴식 중 ☕"
    mode_class = "mode-study" if ss.pomo_is_study else "mode-rest"
    ring_color = "#4e7fff" if ss.pomo_is_study else "#22c984"
    prog = 1 - (remaining / (STUDY_SEC if ss.pomo_is_study else REST_SEC))

    _, ct, _ = st.columns([1, 2, 1])
    with ct:
        st.markdown(f"""
        <div style="background:{T['surface']};border:1.5px solid {T['border']};
                    border-radius:20px;padding:32px 24px;text-align:center;margin-bottom:16px;">
          <div class="timer-big">{mins:02d}:{secs:02d}</div>
          <div class="timer-mode {mode_class}">{mode_label}</div>
        </div>
        <div style="background:{T['surface2']};border-radius:999px;height:8px;margin-bottom:20px;overflow:hidden;">
          <div style="background:{ring_color};height:100%;width:{prog*100:.1f}%;border-radius:999px;transition:width .5s;"></div>
        </div>
        """, unsafe_allow_html=True)

        dots = "".join(
            f'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;'
            f'background:{"#f5a623" if i < ss.study_sessions % 4 else T["border"]};margin:0 4px;'
            f'box-shadow:{"0 0 6px #f5a62360" if i < ss.study_sessions % 4 else "none"}"></span>'
            for i in range(4)
        )
        st.markdown(f'<div style="text-align:center;margin-bottom:20px">{dots}</div>', unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("↺ 리셋", use_container_width=True, key="pomo_reset"):
                ss.pomo_running=False; ss.pomo_is_study=True
                ss.pomo_seconds=STUDY_SEC; ss.pomo_start_time=None; ss.pomo_elapsed=0
                st.rerun()
        with b2:
            if ss.pomo_running:
                if st.button("⏸ 일시정지", use_container_width=True, key="pomo_pause"):
                    ss.pomo_elapsed += time.time() - ss.pomo_start_time
                    ss.pomo_seconds=remaining; ss.pomo_running=False; ss.pomo_start_time=None
                    st.rerun()
            else:
                if st.button("▶ 시작", use_container_width=True, key="pomo_start"):
                    ss.pomo_running=True; ss.pomo_start_time=time.time(); ss.pomo_elapsed=0
                    st.rerun()
        with b3:
            if st.button("⏭ 건너뛰기", use_container_width=True, key="pomo_skip"):
                ss.pomo_running=False; ss.pomo_is_study=not ss.pomo_is_study
                ss.pomo_seconds=STUDY_SEC if ss.pomo_is_study else REST_SEC
                ss.pomo_start_time=None; ss.pomo_elapsed=0
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("🍅 완료 세션", ss.study_sessions)
    m2.metric("⏱ 공부 시간", f"{ss.total_minutes}분")
    m3.metric("🪙 획득 코인", ss.study_sessions * 5)

    if ss.pomo_running:
        time.sleep(1)
        st.rerun()


# ════════════════════════════════
# TAB 3 — 상점
# ════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">상점</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">코인으로 아이템과 펫을 구매해요!</div>', unsafe_allow_html=True)
    st.info(f"💡 현재 보유 코인: **{st.session_state.coins} 🪙**  |  할일 완료 **+2**, 뽀모도로 1세션 **+5**")

    st.markdown("#### 🎁 아이템")
    cols = st.columns(4)
    for i, item in enumerate(SHOP_ITEMS):
        with cols[i % 4]:
            owned = item["id"] in st.session_state.owned_items
            st.markdown(f"""
            <div class="card {'card-done' if owned else ''}">
              <div style="font-size:36px;text-align:center">{item['icon']}</div>
              <div style="font-weight:700;text-align:center;color:{T['text']};margin:8px 0 4px">{item['name']}</div>
              <div style="font-size:12px;color:{T['muted']};text-align:center;margin-bottom:12px">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if owned:
                st.markdown("<div style='text-align:center;color:#22c984;font-size:12px'>✓ 보유 중</div>", unsafe_allow_html=True)
            else:
                if st.button(f"🪙 {item['price']}", key=f"buy_item_{item['id']}", use_container_width=True):
                    if st.session_state.coins >= item["price"]:
                        st.session_state.coins -= item["price"]
                        st.session_state.owned_items.append(item["id"])
                        st.toast(f"✨ {item['name']} 구매 완료!"); st.rerun()
                    else:
                        st.toast("❌ 코인이 부족해요!")

    st.markdown("<br>#### 🐾 펫", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, pet in enumerate(ALL_PETS):
        with cols[i % 4]:
            owned = pet["id"] in st.session_state.owned_pets
            st.markdown(f"""
            <div class="card {'card-done' if owned else ''}">
              <div style="font-size:44px;text-align:center">{pet['emoji']}</div>
              <div style="font-weight:700;text-align:center;color:{T['text']};margin:8px 0 4px">{pet['name']}</div>
              <div style="font-size:11px;color:{T['muted']};text-align:center;margin-bottom:12px">{pet['trait']}</div>
            </div>
            """, unsafe_allow_html=True)
            if owned:
                st.markdown("<div style='text-align:center;color:#22c984;font-size:12px'>✓ 보유 중</div>", unsafe_allow_html=True)
            else:
                if st.button(f"🪙 {pet['price']}", key=f"buy_pet_{pet['id']}", use_container_width=True):
                    if st.session_state.coins >= pet["price"]:
                        st.session_state.coins -= pet["price"]
                        st.session_state.owned_pets.append(pet["id"])
                        if not st.session_state.active_pet:
                            st.session_state.active_pet = pet["id"]
                        st.toast(f"🎉 {pet['emoji']} {pet['name']} 구매 완료!"); st.rerun()
                    else:
                        st.toast("❌ 코인이 부족해요!")


# ════════════════════════════════
# TAB 4 — 펫
# ════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">내 펫</div>', unsafe_allow_html=True)

    if st.session_state.active_pet:
        pet = next(p for p in ALL_PETS if p["id"] == st.session_state.active_pet)
        st.markdown(f"""
        <div style="background:{T['surface']};border:1.5px solid #f5a623;border-radius:16px;
                    padding:24px 28px;display:flex;align-items:center;gap:20px;
                    box-shadow:0 0 30px #f5a62318;margin-bottom:28px;">
          <span style="font-size:72px">{pet['emoji']}</span>
          <div>
            <div style="font-size:22px;font-weight:800;color:#f5a623">{pet['name']}</div>
            <div style="color:{T['muted']};margin-top:4px">{pet['trait']}</div>
            <span style="display:inline-block;background:#f5a62320;color:#f5a623;
                         padding:3px 12px;border-radius:999px;font-size:12px;font-weight:600;margin-top:10px">
              현재 선택된 펫
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("🐾 아직 펫이 없어요! 상점 탭에서 펫을 구매해보세요.")

    st.markdown("#### 보유 중인 펫")
    owned_list = [p for p in ALL_PETS if p["id"] in st.session_state.owned_pets]
    if not owned_list:
        st.markdown(f"<div style='color:{T['muted']};font-size:14px'>보유한 펫이 없어요. 상점에서 구매해보세요!</div>", unsafe_allow_html=True)
    else:
        cols = st.columns(min(len(owned_list), 4))
        for i, pet in enumerate(owned_list):
            with cols[i % 4]:
                is_active = st.session_state.active_pet == pet["id"]
                border = "#f5a623" if is_active else T['border']
                shadow = "0 0 20px #f5a62320" if is_active else "none"
                st.markdown(f"""
                <div style="background:{T['surface']};border:1.5px solid {border};border-radius:16px;
                            padding:20px;text-align:center;margin-bottom:8px;box-shadow:{shadow};">
                  <div style="font-size:52px">{pet['emoji']}</div>
                  <div style="font-weight:700;font-size:16px;color:{T['text']};margin:8px 0 4px">{pet['name']}</div>
                  <div style="font-size:12px;color:{T['muted']};margin-bottom:12px">{pet['trait']}</div>
                </div>
                """, unsafe_allow_html=True)
                if is_active:
                    st.markdown("<div style='text-align:center;color:#f5a623;font-size:12px;font-weight:600'>✓ 선택됨</div>", unsafe_allow_html=True)
                else:
                    if st.button("선택하기", key=f"sel_{pet['id']}", use_container_width=True):
                        st.session_state.active_pet = pet["id"]
                        st.toast(f"{pet['emoji']} {pet['name']}을(를) 선택했어요!")
                        st.rerun()
