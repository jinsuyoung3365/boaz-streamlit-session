# [실습] STEP 1 · 필터  (빈 화면에서 시작)
# ▶ 실행:  streamlit run starter/step1.py
# ▶ TODO 블록: 주석 처리된 코드를 드래그 → Cmd+/ (윈도우 Ctrl+/) 로 주석 해제 → ____ 채우기 → 저장하면 브라우저에 [Rerun] 버튼 뜸

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="세계 발전 대시보드", page_icon="🌍", layout="wide")

# 차트 축·범례에 쓸 한글 이름
LABELS = {
    "gdpPercap": "1인당 GDP ($)",
    "lifeExp": "기대수명 (세)",
    "pop": "인구",
    "continent": "대륙",
    "country": "국가",
    "year": "연도",
}
# 대륙별 색 고정 (모든 차트에서 같은 색)
COLORS = {"Africa": "#F4A261", "Americas": "#E76F51", "Asia": "#4C7BF4", "Europe": "#2A9D8F", "Oceania": "#B388EB"}


# 버튼 하나 누를 때마다 코드가 위에서부터 다시 실행됨(rerun)
# → 데이터 로딩은 캐시해 두고 처음 한 번만 실행
@st.cache_data
def load_data():
    return px.data.gapminder()


df = load_data()

st.title("🌍 세계 발전 대시보드")
st.caption("1952–2007 · 142개국 · 5년 단위 · 데이터: Gapminder (plotly 내장)")

# ───────── STEP 1. 필터 ─────────
# TODO 1-1. 사이드바에 대륙 선택(multiselect) + 연도 선택(select_slider) 만들기
# with st.sidebar:
#     st.header("필터")
#     all_continents = sorted(df["____"].unique())
#     continents = st.multiselect("대륙", options=all_continents, default=all_continents)
#     year = st.select_slider("연도", options=sorted(df["____"].unique()), value=2007)

# TODO 1-2. 고른 값으로 데이터 거르기
# filtered = df[df["continent"].isin(____)]        # 대륙 필터만 적용 (전체 연도)
# df_year = filtered[filtered["year"] == ____]       # 대륙 + 연도 필터 적용
#
# if df_year.empty:
#     st.warning("대륙을 하나 이상 선택해 주세요.")
#     st.stop()

# TODO 1-3. 잘 걸러졌는지 확인 (STEP 2부터는 지워도 됨)
# st.write(f"선택한 데이터: {len(df_year)}개국")
# st.dataframe(df_year, hide_index=True)
