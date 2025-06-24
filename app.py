"""import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    df = df[df['Status'] == 'Finished'][['Full Name', 'Score']]
    df['Full Name'] = df['Full Name'].astype(str).str[-3:]
    return df.reset_index(drop=True)

df = load_data()

st.title("나의 현재 위치")
st.write("수강생 전체 점수에서 본인의 위치를 확인하세요!")

target_name = st.text_input("본인의 전체 이름을 입력하세요 (예: 김오즈)")

if target_name:
    user_row = df[df['Full Name'].str.contains(target_name, case=False)]

    if user_row.empty:
        st.warning("입력한 이름을 찾을 수 없습니다.")
    else:
        user_score = user_row['Score'].values[0]
        average_score = round(df['Score'].mean(), 1)

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 5))

        # 히스토그램
        ax.hist(df['Score'], bins=10, alpha=0.5, label='전체 점수 분포', color='skyblue', edgecolor='black')

        # 평균선
        ax.axvline(average_score, color='gray', linestyle='--', label=f'평균 점수: {average_score}')

        # 본인 점수
        ax.axvline(user_score, color='orange', linestyle='-', linewidth=3, label=f'내 점수: {user_score}')
        ax.scatter(user_score, 0, color='red', s=100, label='👤 나', zorder=5)

        ax.set_xlabel("점수")
        ax.set_ylabel("수강생 수")
        ax.set_title("수강생 점수 분포도")
        ax.legend()
        st.pyplot(fig)"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    df = df[df['Status'] == 'Finished'][['Full Name', 'Score']]
    df['Full Name'] = df['Full Name'].astype(str).str[-3:]
    return df.reset_index(drop=True)

def get_quantile(score):
    if score <= q1: return '하위 25% 입니다.'
    elif score <= q2 : return '25~50% 입니다.'
    elif score <= q3 : return '50~75% 입니다.'
    else : return '상위 25% 입니다.'

df = load_data()

st.title("나의 파이썬 성취도")
st.write("수강생 전체 점수에서 본인의 파이썬 위치를 확인하세요!")

target_name = st.text_input("본인의 전체 이름을 입력하세요 (예: 김오즈)")

if target_name:
    user_row = df[df['Full Name'].str.contains(target_name, case=False)]

    if user_row.empty:
        st.warning("입력한 이름을 찾을 수 없습니다.")
    else:
        user_score = user_row['Score'].values[0]
        average_score = round(df['Score'].mean(), 1)

        # 사분위수
        q1 = df['Score'].quantile(0.25)
        q2 = df['Score'].quantile(0.50)
        q3 = df['Score'].quantile(0.75)


        user_quartile = get_quantile(user_score)

        st.success(f"{target_name}님의 점수는 **{user_score}점**이며, **{user_quartile}**입니다.")
        st.info(f"전체 수강생 평균 점수는 **{average_score}점**입니다.\n\n")

        # Plotly 히스토그램 생성
        fig = px.histogram(df, x='Score', nbins=10, opacity=0.5,
                           labels={'Score':'점수'}, title='수강생 점수 분포도',
                           color_discrete_sequence=['skyblue'])

        # 평균 점수 수직선 추가
        fig.add_vline(x=average_score, line_dash="dash", line_color="gray",
                      annotation_text=f"평균 점수: {average_score}", annotation_position="top left")

        # 본인 점수 수직선 추가
        fig.add_vline(x=user_score, line_dash="solid", line_color="orange", line_width=3,
                      annotation_text=f"내 점수: {user_score}", annotation_position="top right")

        # 본인 점수 위치에 점 추가 (y 위치는 임의로 0으로 설정)
        fig.add_trace(go.Scatter(x=[user_score], y=[0],
                                 mode='markers+text',
                                 marker=dict(color='red', size=12),
                                 text=['👤 나'],
                                 textposition='top center',
                                 showlegend=False))

        fig.update_layout(yaxis_title='수강생 수')
        st.plotly_chart(fig, use_container_width=True)

