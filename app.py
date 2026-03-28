import streamlit as st
import time

# ── 페이지 설정 ──
st.set_page_config(
    page_title="마이타임",
    page_icon="⏱",
    layout="wide",
)

# ── 스타일 ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* 전체 배경 */
.stApp { background: #0e0f18; color: #e8eaf0; }
[data-testid="stSidebar"] { background: #161824; border-right: 1px solid #2a2e50; }

/* 헤더 */
.app-header {
    display: flex; align-items: center; justify-content: space-between;
    background: #161824;
    border: 1px solid #2a2e50;
    border-radius: 16px;
    padding: 16px 24px;
    margin-bottom: 28px;
}
.app-logo { display: flex; align-items: center; gap: 12px; }
.logo-icon {
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, #e06b3a, #f5a623);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.logo-text { font-size: 24px; font-weight: 900; color: #f5a623; letter-spacing: -0.5px; }
.coin-badge {
    display: flex; align-items: center; gap: 8px;
    background: #1e2035; border: 1px solid #2a2e50;
    padding: 8px 18px; border-radius: 999px;
    font-size: 18px; font-weight: 700; color: #f5c842;
    box-shadow: 0 0 12px #f5c84220;
}

/* 카드 */
.card {
    background: #161824;
    border: 1.5px solid #2a2e50;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    transition: border-color .2s;
}
.card:hover { border-color: #3a3e60; }
.card-done { opacity: .5; }

/* 체크 아이템 */
.todo-row {
    display: flex; align-items: center; gap: 12px;
    background: #161824; border: 1.5px solid #2a2e50;
    border-radius: 10px; padding: 12px 16px;
    margin-bottom: 8px;
}
.todo-row.done { opacity: .5; }
.done-text { text-decoration: line-through; color: #6b7090; }

/* 섹션 타이틀 */
.section-title {
    font-size: 22px; font-weight: 800;
    margin-bottom: 6px; color: #e8eaf0;
}
.section-sub { font-size: 13px; color: #6b7090; margin-bottom: 20px; }

/* 타이머 디스플레이 */
.timer-big {
    font-size: 80px; font-weight: 900;
    letter-spacing: -4px; color: #e8eaf0;
    text-align: center; line-height: 1;
    font-variant-numeric: tabular-nums;
}
.timer-mode {
    text-align: center; font-size: 16px; font-weight: 500;
    margin-top: 8px; margin-bottom: 24px;
}
.mode-study { color: #4e7fff; }
.mode-rest  { color: #22c984; }

/* 상점 아이템 */
.shop-card {
    background: #161824; border: 1.5px solid #2a2e50;
    border-radius: 14px; padding: 20px 16px;
    text-align: center; cursor: pointer;
    transition: all .2s;
}
.shop-card:hover { border-color: #f5a623; }
.shop-card.owned { border-color: #22c984; opacity: .7; }

/* 펫 카드 */
.pet-card {
    background: #161824; border: 1.5px solid #2a2e50;
    border-radius: 16px; padding: 24px 20px;
    text-align: center;
}
.pet-card.active { border-color: #f5a623; box-shadow: 0 0 20px #f5a62320; }

/* 통계 카드 */
.stat-card {
    background: #161824; border: 1px solid #2a2e50;
    border-radius: 12px; padding: 16px 20px; text-align: center;
}
.stat-num { font-size: 32px; font-weight: 800; color: #f5a623; }
.stat-label { font-size: 12px; color: #6b7090; margin-top: 2px; }

/* Streamlit 기본 요소 덮어쓰기 */
.stButton > button {
    background: #1e2035 !important; color: #e8eaf0 !important;
    border: 1.5px solid #2a2e50 !important;
    border-radius: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 600 !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    border-color: #4e7fff !important;
    background: #252a45 !important;
}
.stTextInput > div > div > input {
    background: #161824 !important; color: #e8eaf0 !important;
    border: 1.5px solid #2a2e50 !important; border-radius: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4e7fff !important; box-shadow: 0 0 0 1px #4e7fff !important;
}
.stProgress > div > div > div { background: linear-gradient(90deg, #22c984, #a0f0c0) !important; }
div[data-testid="stMetricValue"] { color: #f5a623 !important; font-weight: 800 !important; }
label { color: #e8eaf0 !important; }
</style>
""", unsafe_allow_html=True)

# ── 세션 상태 초기화 ──
def init_state():
    defaults = {
        "coins": 0,
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

# ── 데이터 ──
SHOP_ITEMS = [
    {"id": "bg1",    "icon": "🌙", "name": "다크문 테마",  "desc": "차분한 달빛 배경",      "price": 10},
    {"id": "bg2",    "icon": "🌊", "name": "오션 테마",    "desc": "편안한 파도 배경",      "price": 15},
    {"id": "boost1", "icon": "⚡", "name": "집중 부스터",  "desc": "다음 뽀모 코인 2배",    "price": 8},
    {"id": "deco1",  "icon": "🎵", "name": "집중 음악",    "desc": "백색소음 활성화",       "price": 12},
]

ALL_PETS = [
    {"id": "cat",    "emoji": "🐱", "name": "고양이", "trait": "호기심이 많고 독립적이에요", "price": 20},
    {"id": "dog",    "emoji": "🐶", "name": "강아지", "trait": "활발하고 충성스러워요",     "price": 20},
    {"id": "rabbit", "emoji": "🐰", "name": "토끼",   "trait": "조용하고 귀여워요",         "price": 25},
    {"id": "dragon", "emoji": "🐲", "name": "드래곤", "trait": "희귀하고 강력해요",         "price": 50},
]

# ── 헤더 ──
st.markdown(f"""
<div class="app-header">
  <div class="app-logo">
    <div class="logo-icon">⏱</div>
    <div class="logo-text">마이타임</div>
  </div>
  <div class="coin-badge">🪙 {st.session_state.coins} 코인</div>
</div>
""", unsafe_allow_html=True)

# ── 탭 ──
tab1, tab2, tab3, tab4 = st.tabs(["✅  할일", "🍅  뽀모도로", "🏪  상점", "🐾  펫"])


# ════════════════════════════════
# TAB 1 — 할일 체크리스트
# ════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">할일 체크리스트</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">완료하면 🪙 2 코인 획득!</div>', unsafe_allow_html=True)

    # 진행률
    todos = st.session_state.todos
    done_count = sum(1 for t in todos if t["done"])
    total_count = len(todos)
    progress = done_count / total_count if total_count else 0
    col_prog, col_label = st.columns([5, 1])
    with col_prog:
        st.progress(progress)
    with col_label:
        st.markdown(f"<div style='color:#6b7090;font-size:14px;padding-top:6px'>{done_count} / {total_count}</div>", unsafe_allow_html=True)

    # 입력
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        new_todo = st.text_input("", placeholder="할일을 입력하세요...", label_visibility="collapsed", key="todo_input")
    with col_btn:
        if st.button("+ 추가", use_container_width=True, key="add_todo_btn"):
            if new_todo.strip():
                st.session_state.todos.append({"id": st.session_state.next_id, "text": new_todo.strip(), "done": False})
                st.session_state.next_id += 1
                st.rerun()

    st.markdown("---", unsafe_allow_html=False)

    # 목록
    for i, todo in enumerate(st.session_state.todos):
        col_check, col_text, col_del = st.columns([1, 8, 1])
        with col_check:
            if not todo["done"]:
                if st.button("⬜", key=f"check_{todo['id']}", help="완료"):
                    st.session_state.todos[i]["done"] = True
                    st.session_state.coins += 2
                    st.toast(f"✅ 완료! +2 코인 획득 🎉")
                    st.rerun()
            else:
                st.button("✅", key=f"checked_{todo['id']}", disabled=True)
        with col_text:
            style = "text-decoration:line-through;color:#6b7090;" if todo["done"] else "color:#e8eaf0;"
            st.markdown(f"<div style='{style}font-size:15px;padding-top:8px'>{todo['text']}</div>", unsafe_allow_html=True)
        with col_del:
            if st.button("✕", key=f"del_{todo['id']}", help="삭제"):
                st.session_state.todos = [t for t in st.session_state.todos if t["id"] != todo["id"]]
                st.rerun()


# ════════════════════════════════
# TAB 2 — 뽀모도로
# ════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">뽀모도로 타이머</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">공부 완료 시 🪙 5 코인 획득!</div>', unsafe_allow_html=True)

    STUDY_SEC = 25 * 60
    REST_SEC  = 5 * 60

    # 현재 남은 시간 계산
    ss = st.session_state
    if ss.pomo_running and ss.pomo_start_time:
        elapsed = time.time() - ss.pomo_start_time + ss.pomo_elapsed
        total = STUDY_SEC if ss.pomo_is_study else REST_SEC
        remaining = max(0, total - elapsed)
        if remaining <= 0:
            # 세션 완료
            ss.pomo_running = False
            ss.pomo_start_time = None
            ss.pomo_elapsed = 0
            if ss.pomo_is_study:
                ss.study_sessions += 1
                ss.total_minutes += 25
                ss.coins += 5
                st.toast("🍅 뽀모도로 완료! +5 코인 획득!")
            else:
                st.toast("⏰ 휴식 끝! 다시 집중해봐요 💪")
            ss.pomo_is_study = not ss.pomo_is_study
            ss.pomo_seconds = STUDY_SEC if ss.pomo_is_study else REST_SEC
            remaining = ss.pomo_seconds
    else:
        remaining = ss.pomo_seconds

    mins = int(remaining) // 60
    secs = int(remaining) % 60
    mode_label = "공부 중 📚" if ss.pomo_is_study else "휴식 중 ☕"
    mode_class  = "mode-study" if ss.pomo_is_study else "mode-rest"
    color = "#4e7fff" if ss.pomo_is_study else "#22c984"

    # 진행 바
    total_sec = STUDY_SEC if ss.pomo_is_study else REST_SEC
    prog = 1 - (remaining / total_sec)

    # 타이머 디스플레이
    _, col_timer, _ = st.columns([1, 2, 1])
    with col_timer:
        st.markdown(f"""
        <div style="background:#161824;border:1.5px solid #2a2e50;border-radius:20px;padding:32px 24px;text-align:center;margin-bottom:16px;">
          <div class="timer-big">{mins:02d}:{secs:02d}</div>
          <div class="timer-mode {mode_class}">{mode_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # 진행 바
        st.markdown(f"""
        <div style="background:#1e2035;border-radius:999px;height:8px;margin-bottom:20px;overflow:hidden;">
          <div style="background:{color};height:100%;width:{prog*100:.1f}%;border-radius:999px;transition:width .5s;"></div>
        </div>
        """, unsafe_allow_html=True)

        # 세션 도트
        dots_html = ""
        for i in range(4):
            filled = i < (ss.study_sessions % 4)
            bg = "#f5a623" if filled else "#2a2e50"
            dots_html += f'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:{bg};margin:0 4px;box-shadow:{"0 0 6px #f5a62360" if filled else "none"}"></span>'
        st.markdown(f'<div style="text-align:center;margin-bottom:20px">{dots_html}</div>', unsafe_allow_html=True)

        # 컨트롤 버튼
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("↺ 리셋", use_container_width=True, key="pomo_reset"):
                ss.pomo_running = False
                ss.pomo_is_study = True
                ss.pomo_seconds = STUDY_SEC
                ss.pomo_start_time = None
                ss.pomo_elapsed = 0
                st.rerun()
        with c2:
            if ss.pomo_running:
                if st.button("⏸ 일시정지", use_container_width=True, key="pomo_pause"):
                    ss.pomo_elapsed += time.time() - ss.pomo_start_time
                    ss.pomo_seconds = remaining
                    ss.pomo_running = False
                    ss.pomo_start_time = None
                    st.rerun()
            else:
                if st.button("▶ 시작", use_container_width=True, key="pomo_start"):
                    ss.pomo_running = True
                    ss.pomo_start_time = time.time()
                    ss.pomo_elapsed = 0
                    st.rerun()
        with c3:
            if st.button("⏭ 건너뛰기", use_container_width=True, key="pomo_skip"):
                ss.pomo_running = False
                ss.pomo_is_study = not ss.pomo_is_study
                ss.pomo_seconds = STUDY_SEC if ss.pomo_is_study else REST_SEC
                ss.pomo_start_time = None
                ss.pomo_elapsed = 0
                st.rerun()

    # 통계
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("🍅 완료 세션", ss.study_sessions)
    c2.metric("⏱ 공부 시간", f"{ss.total_minutes}분")
    c3.metric("🪙 획득 코인", ss.study_sessions * 5)

    # 타이머 자동 새로고침 (실행 중일 때만)
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

    # 아이템
    st.markdown("#### 🎁 아이템")
    cols = st.columns(4)
    for i, item in enumerate(SHOP_ITEMS):
        with cols[i % 4]:
            owned = item["id"] in st.session_state.owned_items
            st.markdown(f"""
            <div class="card {'card-done' if owned else ''}">
              <div style="font-size:36px;text-align:center">{item['icon']}</div>
              <div style="font-weight:700;text-align:center;margin:8px 0 4px">{item['name']}</div>
              <div style="font-size:12px;color:#6b7090;text-align:center;margin-bottom:12px">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if owned:
                st.markdown("<div style='text-align:center;color:#22c984;font-size:12px;margin-top:-4px'>✓ 보유 중</div>", unsafe_allow_html=True)
            else:
                if st.button(f"🪙 {item['price']}", key=f"buy_item_{item['id']}", use_container_width=True):
                    if st.session_state.coins >= item["price"]:
                        st.session_state.coins -= item["price"]
                        st.session_state.owned_items.append(item["id"])
                        st.toast(f"✨ {item['name']} 구매 완료!")
                        st.rerun()
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
              <div style="font-weight:700;text-align:center;margin:8px 0 4px">{pet['name']}</div>
              <div style="font-size:11px;color:#6b7090;text-align:center;margin-bottom:12px">{pet['trait']}</div>
            </div>
            """, unsafe_allow_html=True)
            if owned:
                st.markdown("<div style='text-align:center;color:#22c984;font-size:12px;margin-top:-4px'>✓ 보유 중</div>", unsafe_allow_html=True)
            else:
                if st.button(f"🪙 {pet['price']}", key=f"buy_pet_{pet['id']}", use_container_width=True):
                    if st.session_state.coins >= pet["price"]:
                        st.session_state.coins -= pet["price"]
                        st.session_state.owned_pets.append(pet["id"])
                        if not st.session_state.active_pet:
                            st.session_state.active_pet = pet["id"]
                        st.toast(f"🎉 {pet['emoji']} {pet['name']} 구매 완료!")
                        st.rerun()
                    else:
                        st.toast("❌ 코인이 부족해요!")


# ════════════════════════════════
# TAB 4 — 펫
# ════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">내 펫</div>', unsafe_allow_html=True)

    # 현재 펫 표시
    if st.session_state.active_pet:
        pet = next(p for p in ALL_PETS if p["id"] == st.session_state.active_pet)
        st.markdown(f"""
        <div style="background:#161824;border:1.5px solid #f5a623;border-radius:16px;
                    padding:24px 28px;display:flex;align-items:center;gap:20px;
                    box-shadow:0 0 30px #f5a62318;margin-bottom:28px;">
          <span style="font-size:72px">{pet['emoji']}</span>
          <div>
            <div style="font-size:22px;font-weight:800;color:#f5a623">{pet['name']}</div>
            <div style="color:#6b7090;margin-top:4px">{pet['trait']}</div>
            <span style="display:inline-block;background:#f5a62320;color:#f5a623;
                         padding:3px 12px;border-radius:999px;font-size:12px;font-weight:600;margin-top:10px">
              현재 선택된 펫
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("🐾 아직 펫이 없어요! 상점 탭에서 펫을 구매해보세요.")

    # 보유 펫 목록
    st.markdown("#### 보유 중인 펫")
    owned = [p for p in ALL_PETS if p["id"] in st.session_state.owned_pets]
    if not owned:
        st.markdown("<div style='color:#6b7090;font-size:14px'>보유한 펫이 없어요. 상점에서 구매해보세요!</div>", unsafe_allow_html=True)
    else:
        cols = st.columns(min(len(owned), 4))
        for i, pet in enumerate(owned):
            with cols[i % 4]:
                is_active = st.session_state.active_pet == pet["id"]
                border = "#f5a623" if is_active else "#2a2e50"
                st.markdown(f"""
                <div style="background:#161824;border:1.5px solid {border};border-radius:16px;
                            padding:20px;text-align:center;margin-bottom:8px;
                            box-shadow:{'0 0 20px #f5a62320' if is_active else 'none'}">
                  <div style="font-size:52px">{pet['emoji']}</div>
                  <div style="font-weight:700;font-size:16px;margin:8px 0 4px">{pet['name']}</div>
                  <div style="font-size:12px;color:#6b7090;margin-bottom:12px">{pet['trait']}</div>
                </div>
                """, unsafe_allow_html=True)
                if is_active:
                    st.markdown("<div style='text-align:center;color:#f5a623;font-size:12px;font-weight:600'>✓ 선택됨</div>", unsafe_allow_html=True)
                else:
                    if st.button("선택하기", key=f"sel_{pet['id']}", use_container_width=True):
                        st.session_state.active_pet = pet["id"]
                        st.toast(f"{pet['emoji']} {pet['name']}을(를) 선택했어요!")
                        st.rerun()
