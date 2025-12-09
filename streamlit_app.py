import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="연령대별 독서 데이터 대시보드",
    layout="wide"
)

# ----------------------------------------------------
# 인코딩 자동 인식용 CSV 로더
# ----------------------------------------------------
def load_csv_auto(path):
    """UTF-8 → 실패 시 CP949로 자동 재시도"""
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp949")


# ----------------------------------------------------
# 1. 데이터 로드 (파일명: 1.xlsx, 2.csv, 4.csv)
# ----------------------------------------------------
@st.cache_data
def load_barrier():
    return pd.read_excel("1.xlsx")

@st.cache_data
def load_read_amount():
    return load_csv_auto("2.csv")

@st.cache_data
def load_genre():
    return load_csv_auto("4.csv")


# ----------------------------------------------------
# 2. 데이터 불러오기
# ----------------------------------------------------
barrier = load_barrier()
read_amount = load_read_amount()
genre_df = load_genre()


# ----------------------------------------------------
# 3. 페이지 제목
# ----------------------------------------------------
st.title("📚 연령대별 독서 데이터 대시보드")

st.markdown("""
이 대시보드는 **연령대별 독서량**, **독서 장애요인**, **독서 선호도** 데이터를 바탕으로  
특히 **20대 독서의 의미를 분석**하기 위해 제작되었습니다.  
""")


# ----------------------------------------------------
# 4. 연령대 선택 (사이드바)
# ----------------------------------------------------
if "연령대" not in read_amount.columns:
    st.error("❌ 2.csv 안에 '연령대' 컬럼이 없습니다. 파일을 확인해주세요.")
    st.stop()

age_list = sorted(read_amount["연령대"].unique())
selected_age = st.sidebar.selectbox("분석할 연령대를 선택하세요", age_list)


# ----------------------------------------------------
# 5. 탭 구성
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
    st.subheader("📘 연령대별 연간 독서량 변화")

    # 전체 라인 그래프
    if "연도" in read_amount.columns and "독서량" in read_amount.columns:
        fig1 = px.line(
            read_amount,
            x="연도",
            y="독서량",
            color="연령대",
            markers=True,
            title=""
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.error("❌ 2.csv에 '연도' 또는 '독서량' 컬럼이 없습니다.")

    # 선택 연령대 바 그래프
    st.markdown(f"### 👉 {selected_age} 독서량 변화")
    filtered_amt = read_amount[read_amount["연령대"] == selected_age]

    if not filtered_amt.empty:
        fig_amt = px.bar(
            filtered_amt,
            x="연도",
            y="독서량",
            title=f"{selected_age} 연간 독서량"
        )
        st.plotly_chart(fig_amt, use_container_width=True)
    else:
        st.warning("해당 연령대의 독서량 데이터가 없습니다.")


# ----------------------------------------------------
# TAB 2: 독서 장애요인
# ----------------------------------------------------
with tab2:
    st.subheader("🚫 연령대별 독서 장애요인")

    if "연령대" not in barrier.columns:
        st.error("❌ 1.xlsx 안에 '연령대' 컬럼이 없습니다.")
    else:
        filtered_barrier = barrier[barrier["연령대"] == selected_age]

        if not filtered_barrier.empty:
            melted = filtered_barrier.melt(
                id_vars=["연령대"],
                var_name="장애요인",
                value_name="비율"
            )

            fig2 = px.bar(
                melted,
                x="비율",
                y="장애요인",
                orientation="h",
                title=f"{selected_age} 독서 장애요인"
            )
            st.plotly_chart(fig2, use_container_width=True)

            st.info("""
            📌 **가장 비율이 높은 장애요인 = 그 연령대가 책을 읽기 어려운 핵심 이유**
            """)
        else:
            st.warning("해당 연령대의 장애요인 데이터가 없습니다.")


# ----------------------------------------------------
# TAB 3: 독서 선호도
# ----------------------------------------------------
with tab3:
    st.subheader("💛 연령대별 독서 선호도")

    if "연령대" not in genre_df.columns:
        st.error("❌ 4.csv 안에 '연령대' 컬럼이 없습니다.")
    else:
        filtered_genre = genre_df[genre_df["연령대"] == selected_age]

        if not filtered_genre.empty:
            melted_genre = filtered_genre.melt(
                id_vars=["연령대"],
                var_name="구분",
                value_name="비율"
            )

            fig3 = px.pie(
                melted_genre,
                names="구분",
                values="비율",
                hole=0.4,
                title=f"{selected_age} 독서 선호도"
            )
            st.plotly_chart(fig3, use_container_width=True)

            st.info("""
            📌 선호도가 높은 항목 = 해당 연령대의 독서 성향을 의미합니다.
            """)
        else:
            st.warning("해당 연령대의 선호도 데이터가 없습니다.")




