import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="연령대별 독서 데이터 대시보드",
    layout="wide"
)

# ----------------------------------------------------
# CSV 자동 인코딩 로더
# ----------------------------------------------------
def load_csv_auto(path):
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp949")

# ----------------------------------------------------
# 데이터 로드
# ----------------------------------------------------
@st.cache_data
def load_barrier():
    return pd.read_excel("1.xlsx")

@st.cache_data
def load_read_amount():
    df = load_csv_auto("2.csv")
    # 연령별 데이터만 남기기
    df = df[df["통계분류(1)"] == "연령별"].copy()
    # 컬럼명 정리
    df = df.rename(columns={
        "통계분류(2)": "연령대",
        "2019 전체 평균": "2019",
        "2021 전체 평균": "2021"
    })
    # Long 형태로 변환 (line plot 편하게)
    tidy = df.melt(
        id_vars=["연령대"],
        value_vars=["2019", "2021"],
        var_name="연도",
        value_name="독서량"
    )
    tidy["연도"] = tidy["연도"].astype(int)
    return tidy

@st.cache_data
def load_genre():
    return load_csv_auto("4.csv")

# ----------------------------------------------------
# 데이터 불러오기
# ----------------------------------------------------
barrier = load_barrier()
read_amount = load_read_amount()
genre_df = load_genre()

# ----------------------------------------------------
# Page Title
# ----------------------------------------------------
st.title("📚 연령대별 독서 데이터 대시보드")
st.markdown("""
이 대시보드는 **연령대별 독서량**, **독서 장애요인**, **독서 선호도** 데이터를 바탕으로  
특히 **20대 독서의 의미**를 분석하기 위해 제작되었습니다.
""")

# ----------------------------------------------------
# 연령대 선택
# ----------------------------------------------------
age_list = sorted(read_amount["연령대"].unique())
selected_age = st.sidebar.selectbox("연령대를 선택하세요", age_list)

# ----------------------------------------------------
# Tabs 구성
# ----------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "연령대별 독서량",
    "독서 장애요인",
    "독서 선호도",
    "요약 인사이트"
])

# ----------------------------------------------------
# TAB 1: 독서량
# ----------------------------------------------------
with tab1:
    st.subheader("📘 연령대별 연간 독서량 변화 (전체 평균 기준)")

    fig1 = px.line(
        read_amount,
        x="연도",
        y="독서량",
        color="연령대",
        markers=True,
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(f"### 👉 {selected_age}의 독서량 변화")

    sub = read_amount[read_amount["연령대"] == selected_age]

    fig2 = px.bar(
        sub,
        x="연도",
        y="독서량",
        title=f"{selected_age} 독서량 변화"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------
# TAB 2: 장애요인
# ----------------------------------------------------
with tab2:
    st.subheader("🚫 연령대별 독서 장애요인")

    if "연령대" not in barrier.columns:
        st.error("❌ 1.xlsx에 '연령대' 컬럼이 없습니다.")
    else:
        sub = barrier[barrier["연령대"] == selected_age]

        if sub.empty:
            st.warning("해당 연령대의 장애요인 데이터가 없습니다.")
        else:
            melted = sub.melt(
                id_vars=["연령대"],
                var_name="장애요인",
                value_name="비율"
            )

            fig = px.bar(
                melted,
                x="비율",
                y="장애요인",
                orientation="h",
                title=f"{selected_age} 독서 장애요인"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.info("📌 가장 높은 장애요인이 그 연령대에서 독서를 막는 핵심 이유입니다.")

# ----------------------------------------------------
# TAB 3: 선호도
# ----------------------------------------------------
with tab3:
    st.subheader("💛 연령대별 독서 선호도")

    if "연령대" not in genre_df.columns:
        st.error("❌ 4.csv에 '연령대' 컬럼이 없습니다.")
    else:
        sub = genre_df[genre_df["연령대"] == selected_age]

        if sub.empty:
            st.warning("해당 연령대의 선호도 데이터가 없습니다.")
        else:
            melted = sub.melt(
                id_vars=["연령대"],
                var_name="구분",
                value_name="비율"
            )

            fig = px.pie(
                melted,
                names="구분",
                values="비율",
                hole=0.4,
                title=f"{selected_age} 독서 선호도"
            )
            st.plotly_chart(fig, use_container_width=True)
