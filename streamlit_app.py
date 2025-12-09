import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="연령대별 독서 행동 대시보드", layout="wide")

# 연분홍(Pastel Pink) 배경 적용
st.markdown("""
<style>
/* 전체 배경색 */
.main {
    background-color: #FDEEEF !important;   /* 연한 분홍 */
}

/* 중앙 컨테이너 */
.block-container {
    background-color: #FDEEEF !important;
}

/* 탭 배경 */
.stTabs [role="tablist"] {
    background-color: #F8DDE5 !important;   /* 조금 더 진한 핑크 */
    border-radius: 10px;
    padding: 6px;
}

/* 탭 내부 영역 */
.stTabs [role="tabpanel"] {
    background-color: #FFF5F7 !important;   /* 거의 하얀-핑크 */
    padding: 25px;
    border-radius: 12px;
}

/* Plotly 차트 배경 투명하게 */
.js-plotly-plot .plotly {
    background-color: transparent !important;
}

/* 글자 색상(검정 유지) */
html, body, [class*="css"] {
    color: #333333 !important;
}
</style>
""", unsafe_allow_html=True)


st.title("📚 연령대별 독서 행동 대시보드")
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="연령대별 독서 행동 대시보드", layout="wide")
st.title("📚 연령대별 독서 행동 대시보드")

# ----------------------------------------------------------
# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs([
    "① 전체 평균 독서량",
    "② 평일·휴일 독서량",
    "③ 독서 방해 요인",
    "④ 여가시간 대비 독서 비율"
])
# ----------------------------------------------------------


# ==========================================================
# ① 전체 평균 독서량
# ==========================================================
with tab1:
    st.header("전체 평균 독서량 (연령대별)")

    df = pd.read_csv("2.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    ages = df_age["통계분류(2)"]
    val_2019 = df_age["전체 평균"]
    val_2021 = df_age["전체 평균.1"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ages, y=val_2019, mode="lines+markers", name="2019년"
    ))
    fig.add_trace(go.Scatter(
        x=ages, y=val_2021, mode="lines+markers", name="2021년"
    ))

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="연령대",
        yaxis_title="독서량(권)"
    )

    st.plotly_chart(fig, use_container_width=True)



# ==========================================================
# ② 평일·휴일 독서량 — 실제 컬럼명 적용
# ==========================================================
with tab2:
    st.header("평일·휴일 독서량 (연령대별)")

    df = pd.read_csv("8.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    ages = df_age["통계분류(2)"]

    weekday_read = df_age["평일"]
    weekend_read = df_age["휴일"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ages, y=weekday_read, mode="lines+markers", name="평일 독서량"
    ))
    fig.add_trace(go.Scatter(
        x=ages, y=weekend_read, mode="lines+markers", name="휴일 독서량"
    ))

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="연령대",
        yaxis_title="독서량(분)"
    )

    st.plotly_chart(fig, use_container_width=True)



# ==========================================================
# ③ 독서 방해 요인 도넛 차트
# ==========================================================
with tab3:
    st.header("독서 방해 요인 (연령대별)")

    df = pd.read_csv("7.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_list = df_age["통계분류(2)"].unique()
    selected_age = st.selectbox("연령대를 선택하세요", age_list)

    row = df_age[df_age["통계분류(2)"] == selected_age].iloc[0]

    factor_cols = df.columns[3:]
    labels = factor_cols
    values = row[factor_cols].values

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5
    )])

    fig.update_layout(
        hovermode="closest",
        title=f"{selected_age} 독서 방해 요인"
    )

    st.plotly_chart(fig, use_container_width=True)



# ==========================================================
# ④ 여가시간 대비 독서 비율
# ==========================================================
with tab4:
    st.header("여가시간 중 독서 비율 (연령대별)")

    df = pd.read_csv("6.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    ages = df_age["통계분류(2)"]

    weekday_ratio = df_age["여가시간 중 독서시간이 차지하는 비율"]
    weekend_ratio = df_age["여가시간 중 독서시간이 차지하는 비율.1"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ages, y=weekday_ratio, mode="lines+markers", name="평일 비율"
    ))
    fig.add_trace(go.Scatter(
        x=ages, y=weekend_ratio, mode="lines+markers", name="주말 비율"
    ))

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="연령대",
        yaxis_title="비율 (%)"
    )

    st.plotly_chart(fig, use_container_width=True)
