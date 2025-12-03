import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")
st.title("📚 연령대별 독서량 분석 (연도 선택 → 연령대 선 그래프)")


# ---------------------------------------
# 1) 파일 업로드
# ---------------------------------------
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:

    # ---------------------------------------
    # 2) 데이터 로드 & 전처리
    # ---------------------------------------
    df = pd.read_csv(uploaded_file)

    # 첫 두 컬럼 이름 정리
    df = df.rename(columns={df.columns[0]: "구분1", df.columns[1]: "연령대"})

    # '연령'만 포함된 행 선택
    age_df = df[df["구분1"].str.contains("연령", na=False)].copy()

    # melt: wide → long
    tidy = age_df.melt(
        id_vars="연령대",
        var_name="year",
        value_name="read_amount"
    )

    # 연도 숫자형 변환
    tidy["year"] = tidy["year"].astype(int)

    # 독서량 숫자형 변환
    tidy["read_amount"] = pd.to_numeric(tidy["read_amount"], errors="coerce")

    # 정렬
    tidy = tidy.sort_values(["year", "연령대"])

    st.subheader("📊 데이터 미리보기")
    st.dataframe(tidy)


    # ---------------------------------------
    # 3) 연도 선택 selectbox
    # ---------------------------------------
    years = sorted(tidy["year"].unique())
    selected_year = st.selectbox("연도를 선택하세요", years, index=len(years)-1)

    # 선택된 연도 데이터 필터링
    filtered = tidy[tidy["year"] == selected_year]


    # ---------------------------------------
    # 4) 선 그래프 생성
    # ---------------------------------------
    st.subheader(f"📈 {selected_year}년 연령대별 독서량 (선 그래프)")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(filtered["연령대"], filtered["read_amount"], marker='o', linewidth=2)

    ax.set_xlabel("연령대")
    ax.set_ylabel("독서량")
    ax.set_title(f"{selected_year}년 연령대별 독서량")
    plt.xticks(rotation=45)

    st.pyplot(fig)

else:
    st.info("CSV 파일을 업로드하면 분석이 시작됩니다.")
