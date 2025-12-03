import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")

st.title("📚 연령대별 독서량 분석 대시보드")


# ---------------------------------------
# 1) 파일 업로드
# ---------------------------------------
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # ---------------------------------------
    # 2) 데이터 로드
    # ---------------------------------------
    df = pd.read_csv(uploaded_file, encoding="latin1")

    # 첫 번째/두 번째 컬럼 이름 통일
    df = df.rename(columns={df.columns[0]: "구분1", df.columns[1]: "연령대"})

    # 연령대 데이터만 선택
    age_df = df[df["구분1"].str.contains("연령", na=False)].copy()

    # Tidy 변환
    tidy = age_df.melt(
        id_vars="연령대",
        var_name="year",
        value_name="read_amount"
    )

    # '-' 제거하고 숫자로 변환
    tidy = tidy[tidy["read_amount"] != "-"]
    tidy["read_amount"] = tidy["read_amount"].astype(float)

    st.subheader("📊 데이터 미리보기")
    st.dataframe(tidy)

    # ---------------------------------------
    # 3) 연도 선택 위젯 (Interactive)
    # ---------------------------------------
    years = sorted(tidy["year"].unique())

    selected_year = st.selectbox(
        "연도를 선택하세요", 
        years,
        index=len(years) - 1  # 최신 연도 기본 선택
    )

    # 선택한 연도의 데이터 필터링
    filtered = tidy[tidy["year"] == selected_year]

    # ---------------------------------------
    # 4) 그래프 표시
    # ---------------------------------------
    st.subheader(f"📈 {selected_year}년 연령대별 독서량")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(filtered["연령대"], filtered["read_amount"])
    ax.set_xlabel("연령대")
    ax.set_ylabel("독서량")
    ax.set_title(f"{selected_year}년 연령대별 독서량")
    plt.xticks(rotation=45)

    st.pyplot(fig)

else:
    st.info("왼쪽 상단에서 CSV 파일을 업로드하면 분석이 시작됩니다.")
