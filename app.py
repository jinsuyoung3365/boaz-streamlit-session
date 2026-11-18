# 완성본 (배포·시연용) — solutions/step4.py 와 같은 코드
# ▶ 실행:  streamlit run app.py

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
with st.sidebar:
    st.header("필터")
    all_continents = sorted(df["continent"].unique())
    continents = st.multiselect("대륙", options=all_continents, default=all_continents)
    year = st.select_slider("연도", options=sorted(df["year"].unique()), value=2007)

filtered = df[df["continent"].isin(continents)]   # 대륙 필터만 적용 (전체 연도)
df_year = filtered[filtered["year"] == year]       # 대륙 + 연도 필터 적용

if df_year.empty:
    st.warning("대륙을 하나 이상 선택해 주세요.")
    st.stop()

# ───────── STEP 2. KPI 카드 ─────────
prev = filtered[filtered["year"] == year - 5]      # 5년 전 데이터 (증감 표시용)

life = df_year["lifeExp"].mean()
pop = df_year["pop"].sum()
gdp = df_year["gdpPercap"].median()
long = (df_year["lifeExp"] >= 70).sum()            # 기대수명 70세 이상 국가 수

if prev.empty:   # 1952년은 5년 전 데이터가 없음
    long_d = life_d = pop_d = gdp_d = None
else:
    long_d = f"{long - (prev['lifeExp'] >= 70).sum():+d}개국"
    life_d = f"{life - prev['lifeExp'].mean():+.1f}세"
    pop_d = f"{(pop - prev['pop'].sum()) / 1e8:+.1f}억"
    gdp_d = f"{gdp - prev['gdpPercap'].median():+,.0f} 달러"

k1, k2, k3, k4 = st.columns(4)
k1.metric("기대수명 70세 이상", f"{long}개국", delta=long_d, border=True)
k2.metric("평균 기대수명", f"{life:.1f}세", delta=life_d, border=True)
k3.metric("총인구", f"{pop / 1e8:.1f}억", delta=pop_d, border=True)
k4.metric("1인당 GDP 중앙값", f"${gdp:,.0f}", delta=gdp_d, border=True)
st.caption("▲▼ 증감은 5년 전 대비")

# ───────── STEP 3. 차트 ─────────
left, right = st.columns([3, 2])

with left:
    tab1, tab2 = st.tabs(["📍 선택 연도", "▶️ 1952→2007 애니메이션"])

    with tab1:
        # 3-1. 버블 차트: 소득 vs 기대수명 (버블 크기 = 인구)
        fig = px.scatter(
            df_year,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            color_discrete_map=COLORS,
            hover_name="country",
            custom_data=["country"],   # STEP 4 클릭 연동에서 국가 이름을 꺼낼 때 사용
            log_x=True,
            size_max=55,
            range_y=[20, 90],
            labels=LABELS,
        )
        # 4-1. on_select="rerun" → 버블을 클릭하면 앱이 다시 실행되고, 선택 정보가 event에 담김
        event = st.plotly_chart(fig, key="bubble", on_select="rerun", selection_mode="points")

    with tab2:
        # 3-2. 애니메이션: animation_frame에 연도를 넣으면 재생 버튼이 생김
        anim = px.scatter(
            filtered,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            color_discrete_map=COLORS,
            hover_name="country",
            animation_frame="year",
            animation_group="country",
            log_x=True,
            size_max=55,
            range_x=[100, 100000],
            range_y=[20, 90],
            labels=LABELS,
        )
        st.plotly_chart(anim, key="anim")

with right:
    # 3-3. 지구본 지도: projection="orthographic" 한 줄이면 둥근 지구본
    st.markdown(f"**{year}년 국가별 기대수명**")
    globe = px.choropleth(
        df_year,
        locations="iso_alpha",
        color="lifeExp",
        hover_name="country",
        projection="orthographic",
        color_continuous_scale="Viridis",
        range_color=[30, 85],
        labels=LABELS,
    )
    globe.update_geos(bgcolor="rgba(0,0,0,0)", showocean=True, oceancolor="#15233B", showframe=False)
    globe.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=430)
    st.plotly_chart(globe, key="globe")

# ───────── STEP 4. 클릭 연동 ─────────
# 4-2. 클릭한 버블의 국가 이름 꺼내기 (아무것도 안 눌렀으면 기본값)
points = event.selection.points
if points:
    selected = points[0]["customdata"][0]
elif "Korea, Rep." in df_year["country"].values:
    selected = "Korea, Rep."
else:
    selected = df_year.sort_values("pop", ascending=False)["country"].iloc[0]

# 4-3. 선택한 국가의 연도별 추이 차트
st.subheader(f"🔎 {selected} 한눈에 보기")
st.caption("위 버블 차트에서 다른 나라를 클릭해 보세요. (빈 곳을 더블클릭하면 선택 해제)")

hist = df[df["country"] == selected]
c1, c2 = st.columns(2)
with c1:
    line1 = px.line(hist, x="year", y="lifeExp", markers=True, labels=LABELS, title="기대수명 추이")
    line1.add_vline(x=year, line_dash="dot")
    st.plotly_chart(line1, key="line_life")
with c2:
    line2 = px.line(hist, x="year", y="gdpPercap", markers=True, labels=LABELS, title="1인당 GDP 추이")
    line2.add_vline(x=year, line_dash="dot")
    st.plotly_chart(line2, key="line_gdp")

# 3-4. 표 안에 미니 추이 차트: 국가별 기대수명을 리스트로 묶어서 LineChartColumn에 넣기
st.subheader(f"{year}년 국가 순위 (기대수명 순)")
trend = (
    filtered.sort_values("year")
    .groupby("country")["lifeExp"]
    .apply(list)
    .rename("trend")
    .reset_index()
)
table = (
    df_year[["country", "continent", "lifeExp", "gdpPercap", "pop"]]
    .round({"gdpPercap": 0})
    .merge(trend, on="country")
    .sort_values("lifeExp", ascending=False)
)
st.dataframe(
    table,
    hide_index=True,
    height=400,
    column_config={
        "country": "국가",
        "continent": "대륙",
        "lifeExp": st.column_config.NumberColumn("기대수명", format="%.1f세"),
        "gdpPercap": st.column_config.NumberColumn("1인당 GDP ($)", format="localized"),
        "pop": st.column_config.NumberColumn("인구", format="localized"),
        "trend": st.column_config.LineChartColumn("기대수명 추이 (1952→2007)"),
    },
)
