import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")
st.title("📚 연령대별 독서량 분석 대시보드")

# ---------------------------------------
# 1. 파일 업로드
# ---------------------------------------
uploaded = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded, encoding="latin1")

    # 컬럼명 정리
    df = df.rename(columns={df.columns[0]: "구분1", df.columns[1]: "연령대"})

    # 연령만 선택
    age_df = df[df["구분1"].str.contains("연령", na=False)].copy()

    # Tidy 변환
    tidy = age_df.melt(
        id_vars="연령대",
        var_name="year",
        value_name="read_amount"
    )

    # 결측치 제거
    tidy = tidy[tidy["read_amount"] != "-"]

    # 숫자로 변환
    tidy["read_amount"] = tidy["read_amount"].astype(float)

    st.subheader("원본 데이터 미리보기")
    st.dataframe(tidy.head())

    # ---------------------------------------
    # 2. 시각화
    # ---------------------------------------
    st.subheader("연령대별 독서량 변화 추이")

    plt.figure(figsize=(12,6))
    sns.lineplot(data=tidy, x="year", y="read_amount", hue="연령대", marker="o")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

else:
    st.info("CSV 파일을 업로드하면 분석이 시작됩니다.")
