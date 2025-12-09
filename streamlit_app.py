import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령대별 독서 데이터 대시보드", layout="wide")


# ===========================
# 자동 인코딩 CSV 로더
# ===========================
def load_csv_auto(path):
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp949")


# ===========================
# 데이터 로드
# ===========================
@st.cache_data
def load_barrier():
    return pd.read_excel("1.xlsx")

@st.cache_data
def load_year():
    return load_csv_auto("2.csv")

@st.cache_data
def load_age_avg():
    return load_csv_auto("3.csv")


barrier = load_barrier()
year_df = load_year()
age_avg = load_age_avg()


# ===========================
# 헤더
# ===========================
st.title("📚 연령대별 독서 데이터 분석 대시보드")
st.markdown("원하는 분석을 탭에서 선택해 확인하세요.")


# ===========================
# 탭 구성
# ===========================
tab1, tab2, tab3 = st.tabs([
    "① 연령별 독서 장애요인",
    "② 연도별 독서량 변화 (2.csv)",
    "③ 연령대별 전체평균 분석 (3.csv)"
])


# ============================================================
# TAB 1 — 1.xlsx 연령별 독서 장애요인 파이 차트
# ============================================================
with tab1:
    st.header("🚫 연령별 독서 장애요인")

    if "연령대" not in barrier.columns:
        st.error("❌ 1.xlsx 안에 '연령대' 컬럼이 없습니다.")
        st.stop()

    age_list = sorted(barrier["연령대"].unique())
    selected_age = st.selectbox("연령대를 선택하세요", age_list, key="age1")

    df_sub = barrier[barrier["연령대"] == selected_age]

    melted = df_sub.melt(
        id_vars=["연령대"],
        var_name="장애요인",
        value_name="비율"
    )

    fig = px.pie(
        melted,
        names="장애요인",
        values="비율",
        hole=0.4,
        title=f"{selected_age}의 독서 장애요인 비율"
    )

    st.plotly_chart(fig, use_container_width=True)



# ============================================================
# TAB 2 — 2.csv 연도별 독서량 변화 (Line Chart)
# ============================================================
with tab2:
    st.header("📈 연도별 독서량 변화 (전체평균 기준)")

    # 연령별만 가져오기
    year_df = year_df[year_df["통계분류(1)"] == "연령별"].copy()

    # 컬럼 정리
    year_df = year_df.rename(columns={
        "통계분류(2)": "연령대",
        "2019 전체 평균": "2019",
        "2021 전체 평균": "2021"
    })

    tidy = year_df.melt(
        id_vars=["연령대"],
        value_vars=["2019", "2021"],
        var_name="연도",
        value_name="전체평균"
    )

    fig2 = px.line(
        tidy,
        x="연령대",
        y="전체평균",
        color="연도",
        markers=True,
        title="연령대별 전체평균 독서량 변화 (2019 vs 2021)"
    )

    st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# TAB 3 — 3.csv 연령대별 전체평균 (Bar Chart)
# ============================================================
with tab3:
    st.header("📊 연령대별 전체평균 독서량 분석 (3.csv)")

    if "연령대" not in age_avg.columns:
        st.error("3.csv 안에 '연령대' 컬럼이 없습니다.")
        st.stop()

    if "전체평균" not in age_avg.columns:
        st.error("3.csv 안에 '전체평균' 컬럼이 없습니다.")
        st.stop()

    fig3 = px.bar(
        age_avg,
        x="연령대",
        y="전체평균",
        title="연령별 전체 평균 독서량"
    )

    st.plotly_chart(fig3, use_container_width=True)
