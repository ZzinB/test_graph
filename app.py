import streamlit as st
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
        st.pyplot(fig)
