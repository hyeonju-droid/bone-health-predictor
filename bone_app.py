import streamlit as st
import math

st.set_page_config(
    page_title="골 건강 예측",
    page_icon="🦴",
    layout="centered"
)

# -----------------------------
# 예측모델 상수
# -----------------------------
MEAN_SEX = 0.26785714
MEAN_AGE = 33.83035714
MEAN_HEIGHT = 162.36383929
MEAN_WEIGHT = 60.515625

SCALE_SEX = 0.44284274
SCALE_AGE = 22.02783888
SCALE_HEIGHT = 9.65495041
SCALE_WEIGHT = 14.20182102

COEF_SEX = 0.52353434
COEF_AGE = 1.17801891
COEF_HEIGHT = -0.49525420
COEF_WEIGHT = 0.02770572
INTERCEPT = -1.86125566


def predict_probability(male_value, age_value, height_value, weight_value):
    z_sex = (male_value - MEAN_SEX) / SCALE_SEX
    z_age = (age_value - MEAN_AGE) / SCALE_AGE
    z_height = (height_value - MEAN_HEIGHT) / SCALE_HEIGHT
    z_weight = (weight_value - MEAN_WEIGHT) / SCALE_WEIGHT

    logit = (
        INTERCEPT
        + COEF_SEX * z_sex
        + COEF_AGE * z_age
        + COEF_HEIGHT * z_height
        + COEF_WEIGHT * z_weight
    )

    return 1 / (1 + math.exp(-logit))


# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .sub-text {
        font-size: 1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }

    .result-card {
        padding: 1.4rem;
        border-radius: 18px;
        border: 1px solid #ddd;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .result-number {
        font-size: 4.2rem;
        font-weight: 900;
        line-height: 1.05;
        margin: 0.35rem 0 0.6rem 0;
        text-align: center;
    }

    .result-title {
        font-size: 1rem;
        text-align: center;
        color: #555;
        margin-bottom: 0.2rem;
    }

    .risk-row {
        display: flex;
        gap: 8px;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }

    .risk-box {
        flex: 1;
        text-align: center;
        padding: 0.8rem 0.3rem;
        border-radius: 12px;
        border: 1px solid #ddd;
        font-weight: 700;
        opacity: 0.45;
    }

    .risk-active {
        opacity: 1;
        border: 2px solid #333;
        transform: scale(1.02);
    }

    .risk-low {
        background: #e9f7ef;
    }

    .risk-mid {
        background: #fff6db;
    }

    .risk-high {
        background: #fdeaea;
    }

    .small-note {
        font-size: 0.88rem;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 헤더
# -----------------------------
st.markdown('<div class="main-title">🦴 골 건강 예측</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">성별, 나이, 키, 몸무게만으로 낮은 골 상태 가능성을 예측합니다.</div>',
    unsafe_allow_html=True
)

st.info(
    "2021~2026년 연구자료를 기반으로 만든 교육·연구용 스크리닝 프로그램입니다."
)

st.divider()

# -----------------------------
# 입력
# -----------------------------
st.subheader("1️⃣ 기본 정보")

col1, col2 = st.columns(2)

with col1:
    sex_label = st.selectbox("성별", ["여성", "남성"])
    age_input = st.number_input(
        "나이",
        min_value=20,
        max_value=102,
        value=20,
        step=1
    )

with col2:
    height_input = st.number_input(
        "키 (cm)",
        min_value=130.0,
        max_value=200.0,
        value=165.0,
        step=0.1
    )

    weight_input = st.number_input(
        "몸무게 (kg)",
        min_value=30.0,
        max_value=150.0,
        value=60.0,
        step=0.1
    )

bmi = weight_input / ((height_input / 100) ** 2)

if bmi < 18.5:
    bmi_group = "저체중"
elif bmi < 23:
    bmi_group = "정상"
elif bmi < 25:
    bmi_group = "과체중"
else:
    bmi_group = "비만"

st.metric("BMI", f"{bmi:.1f} kg/m²", bmi_group)

st.divider()

# -----------------------------
# 결과
# -----------------------------
if st.button("🔍 골 상태 예측하기", use_container_width=True):

    male_value = 1 if sex_label == "남성" else 0

    probability = predict_probability(
        male_value,
        age_input,
        height_input,
        weight_input
    )

    percent = probability * 100

    if percent < 25:
        result_label = "저위험"
        result_text = (
            "현재 입력정보에서는 낮은 골 상태에 해당할 가능성이 "
            "상대적으로 낮게 예측되었습니다."
        )
        low_class = "risk-active"
        mid_class = ""
        high_class = ""
    elif percent < 50:
        result_label = "주의"
        result_text = (
            "현재 입력정보에서는 낮은 골 상태 가능성이 다소 높게 예측되었습니다."
        )
        low_class = ""
        mid_class = "risk-active"
        high_class = ""
    else:
        result_label = "고위험"
        result_text = (
            "현재 입력정보에서는 낮은 골 상태 가능성이 높게 예측되었습니다."
        )
        low_class = ""
        mid_class = ""
        high_class = "risk-active"

    st.subheader("2️⃣ 예측 결과")

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">낮은 골 상태 추정 가능성</div>
            <div class="result-number">{percent:.1f}%</div>

            <div class="risk-row">
                <div class="risk-box risk-low {low_class}">저위험<br><span style="font-size:0.78rem;">25% 미만</span></div>
                <div class="risk-box risk-mid {mid_class}">주의<br><span style="font-size:0.78rem;">25~49.9%</span></div>
                <div class="risk-box risk-high {high_class}">고위험<br><span style="font-size:0.78rem;">50% 이상</span></div>
            </div>

            <div style="text-align:center; font-size:1.15rem; font-weight:800;">
                현재 단계: {result_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(probability)

    if percent < 25:
        st.success(result_text)
    elif percent < 50:
        st.warning(result_text)
    else:
        st.error(result_text)

    st.caption(
        "※ 25%와 50%는 임상 진단 기준이 아니라, "
        "연구자료 기반 예측값을 이해하기 쉽게 나누기 위한 표시 기준입니다."
    )

    st.divider()

    # -----------------------------
    # 입력정보 요약
    # -----------------------------
    st.subheader("📋 입력정보 요약")

    c1, c2 = st.columns(2)

    with c1:
        st.write(f"**성별:** {sex_label}")
        st.write(f"**나이:** {age_input}세")

    with c2:
        st.write(f"**키:** {height_input:.1f} cm")
        st.write(f"**몸무게:** {weight_input:.1f} kg")

    st.write(f"**BMI:** {bmi:.1f} kg/m² ({bmi_group})")

    st.divider()

    # -----------------------------
    # 결과 해석
    # -----------------------------
    st.subheader("💡 결과 해석")

    st.write(
        """
        이 예측값은 실제 골밀도를 직접 측정한 값이 아닙니다.

        입력된 성별, 나이, 키, 몸무게의 조합이
        기존 연구자료에서 **낮은 골 상태로 분류된 사람들의 패턴과 얼마나 유사한지**
        통계적으로 계산한 결과입니다.
        """
    )

    st.write(
        "따라서 **예측값이 높더라도 실제 골밀도 검사 결과와 반드시 일치하는 것은 아닙니다.**"
    )

    st.divider()

    # -----------------------------
    # 연구기준
    # -----------------------------
    with st.expander("📚 연구 및 모델 정보 보기"):
        st.write(
            """
            **연구자료**
            - 2021~2026년 골밀도 연구자료
            - 정제 후 성인 20~102세 448건 사용

            **입력변수**
            - 성별
            - 나이
            - 키
            - 몸무게

            **낮은 골 상태 분류 기준**
            - 20~49세: Z-score ≤ -2.0
            - 50세 이상: T-score ≤ -2.5

            **모델**
            - 로지스틱 회귀
            - 내부 교차검증 AUC 약 0.80

            동일인이 여러 해 반복 측정된 경우,
            학습자료와 검증자료에 동시에 들어가지 않도록 분리하여 평가했습니다.
            """
        )

    st.divider()

    # -----------------------------
    # 생활관리
    # -----------------------------
    st.subheader("🌱 골 건강 관리")

    st.write(
        """
        - 걷기, 계단 오르기 등 체중부하 운동을 꾸준히 하기
        - 근력운동을 함께 하기
        - 칼슘과 비타민 D를 충분히 섭취하기
        - 흡연과 과도한 음주 피하기
        - 위험요인이 있거나 결과가 걱정된다면 실제 골밀도 검사 받기
        """
    )

    st.warning(
        "이 프로그램은 질병을 진단하거나 의료진의 진료를 대신하지 않습니다."
    )
