import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Reading Dashboard", layout="wide")
st.title("📚 Reading Data Dashboard (Interactive Plotly Version)")

# ----------------------------------------------------------
# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Overall Reading Average",
    "Weekday & Weekend Reading",
    "Reading Barriers",
    "Reading Share of Leisure Time"
])
# ----------------------------------------------------------


# ==========================================================
# ① Overall Reading Average (2.csv)
# ==========================================================
with tab1:
    st.header("Overall Reading Average by Age Group")

    df = pd.read_csv("2.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age = df_age["통계분류(2)"]
    v19 = df_age["전체 평균"]
    v21 = df_age["전체 평균.1"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=age, y=v19,
        mode="lines+markers",
        name="2019",
    ))

    fig.add_trace(go.Scatter(
        x=age, y=v21,
        mode="lines+markers",
        name="2021",
    ))

    # 그래프 내부 텍스트 제거 (y축 글자 제거)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=True,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)




# ==========================================================
# ② Weekday & Weekend Reading (8.csv)
# ==========================================================
with tab2:
    st.header("Weekday & Weekend Reading by Age Group")

    df = pd.read_csv("8.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age = df_age["통계분류(2)"]
    weekday = df_age["평일"]
    weekend = df_age["휴일"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=age, y=weekday,
        mode="lines+markers",
        name="Weekday",
    ))

    fig.add_trace(go.Scatter(
        x=age, y=weekend,
        mode="lines+markers",
        name="Weekend",
    ))

    # 감소 그래프처럼 보이기 위해 y축 반전
    fig.update_yaxes(autorange="reversed", showticklabels=False)

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        hovermode="x unified",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)




# ==========================================================
# ③ Reading Barriers (Donut Chart, 7.csv)
# ==========================================================
with tab3:
    st.header("Reading Barriers (Donut Chart)")

    df = pd.read_csv("7.csv", header=1)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age_options = df_age["통계분류(2)"].unique()
    selected_age = st.selectbox("Select Age Group", age_options)

    row = df_age[df_age["통계분류(2)"] == selected_age].iloc[0]
    factor_cols = df.columns[3:]
    sizes = row[factor_cols].values

    fig = go.Figure(data=[
        go.Pie(
            labels=factor_cols,
            values=sizes,
            hole=0.5,
            textinfo="none"  # 텍스트 제거
        )
    ])

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)




# ==========================================================
# ④ Reading Share of Leisure Time (6.csv)
# ==========================================================
with tab4:
    st.header("Reading Share of Leisure Time")

    df = pd.read_csv("6.csv", header=2)
    df_age = df[df["통계분류(1)"] == "연령별"]

    age = df_age["통계분류(2)"]
    w = df_age["여가시간 중 독서시간이 차지하는 비율"]
    h = df_age["여가시간 중 독서시간이 차지하는 비율.1"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=age, y=w,
        mode="lines+markers",
        name="Weekday Ratio",
    ))

    fig.add_trace(go.Scatter(
        x=age, y=h,
        mode="lines+markers",
        name="Weekend Ratio",
    ))

    # y축 반전 적용 → 감소 그래프처럼 보이기
    fig.update_yaxes(autorange="reversed", showticklabels=False)

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        hovermode="x unified",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
