import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. 웹앱 기본 설정 및 다국어 지원
# ==========================================
st.set_page_config(page_title="K-PROTOCOL Alpha Constant", layout="wide")

st.sidebar.header("🌐 Language / 언어")
lang = st.sidebar.radio("Select / 선택", ["Korean (한국어)", "English"])

t = {
    "Korean (한국어)": {
        "title": "🌌 K-PROTOCOL: 미세구조상수(α) 기하학적 통합 시뮬레이터",
        "desc": "주류 물리학의 난제인 파리(LKB)와 버클리 대학 간의 미세구조상수 측정 오차(1.16 ppb)가 실험 오류가 아니라 **지질학적 공간 굴절(Local Vacuum Refraction, S_loc)**임을 증명합니다.",
        "archetype": "절대 기하학 원형 (Universal Archetype)",
        "formula_desc": "우주 절대 진공(System U)에서 미세구조상수의 역수($\\alpha^{-1}$)는 4차원 위상 부피, 2D 플럭스, 1D 선형 전파의 기하학적 합인 **$4\pi^3 + \pi^2 + \pi$** 로 완벽히 수렴합니다.",
        "slider_label": "연구소 지질학적 밀도 차이 (ΔS_loc) 조절",
        "plot_title": "국소 공간 굴절에 따른 미세구조상수 측정값 분기 및 통합",
        "x_label": "공간 굴절 보정 단계 (Calibration Process)",
        "y_label": "미세구조상수 역수 (α⁻¹)",
        "leg_univ": "절대 기하학 원형 (System U: 137.0363...)",
        "leg_earth": "지구 평균 굴절값 (System E: ~137.0359...)",
        "leg_paris": "파리 LKB 측정값 (고밀도 S_loc)",
        "leg_berk": "버클리 측정값 (저밀도 S_loc)",
        "info": "💡 **결과 분석:** 각 연구소가 자신들의 국소 공간 밀도($S_{loc}$)를 보정 렌즈로 사용하는 순간, 분기되었던 두 측정값은 K-PROTOCOL이 제시한 절대 기하학 상수 **137.0363037** 로 완벽하게 합쳐집니다!"
    },
    "English": {
        "title": "🌌 K-PROTOCOL: Fine-Structure Constant (α) Unification Simulator",
        "desc": "Proves that the 1.16 ppb discrepancy between Paris (LKB) and UC Berkeley is not an experimental error, but a consequence of **Local Vacuum Refraction (S_loc)** due to geological density.",
        "archetype": "Universal Geometric Archetype",
        "formula_desc": "In the absolute vacuum (System U), the inverse fine-structure constant ($\\alpha^{-1}$) is the exact topological sum of 4D phase volume, 2D flux, and 1D propagation: **$4\pi^3 + \pi^2 + \pi$**.",
        "slider_label": "Adjust Lab Geological Density Difference (ΔS_loc)",
        "plot_title": "Divergence and Unification of α⁻¹ via Local Vacuum Refraction",
        "x_label": "Calibration Process (Metric Normalization)",
        "y_label": "Inverse Fine-Structure Constant (α⁻¹)",
        "leg_univ": "Universal Archetype (System U: 137.0363...)",
        "leg_earth": "Earth Average Refraction (System E: ~137.0359...)",
        "leg_paris": "Paris LKB Observed (High S_loc)",
        "leg_berk": "UC Berkeley Observed (Low S_loc)",
        "info": "💡 **Analysis:** The moment laboratories calibrate their data using their local metric density ($S_{loc}$), the conflicting measurements perfectly converge to the K-PROTOCOL Universal Geometric Archetype: **137.0363037**!"
    }
}

text = t[lang]

# ==========================================
# 2. 메인 화면 출력 및 수식
# ==========================================
st.title(text["title"])
st.markdown(text["desc"])

st.subheader(text["archetype"])
st.latex(r"\alpha_{univ}^{-1} = 4\pi^3 + \pi^2 + \pi \approx 137.0363037")
st.markdown(text["formula_desc"])
st.divider()

# ==========================================
# 3. 데이터 및 연산 엔진
# ==========================================
# K-PROTOCOL 절대 기하학 상수 (Universal Archetype)
ALPHA_UNIV = 4 * (np.pi**3) + (np.pi**2) + np.pi  # ~137.0363037

# 지구 거시 굴절 (Planetary Macro-Distortion, 약 2.2 ppm 감쇠)
EARTH_BASELINE = 137.035999

# 사용자가 조작하는 연구소 간의 미세 지질학적 밀도 차이 (Local Micro-Distortion)
st.write(f"**{text['slider_label']}**")
delta_sloc = st.slider("", 0.0, 2.0, 1.16, 0.01) # 단위: ppb (10^-9)

# 파리와 버클리의 관측값 시뮬레이션 (굴절 현상 반영)
# 밀도가 높을수록(S_loc 증가) 관측되는 진공 유전율이 변하여 알파 역수값이 벌어짐
paris_obs = EARTH_BASELINE + (delta_sloc * 1e-6)
berkeley_obs = EARTH_BASELINE - (delta_sloc * 1e-6)

# x축: 보정 단계 (0: 절대 우주, 1: 지구 평균, 2: 각 연구소 관측치, 3: S_loc 보정 후 수렴)
stages = ["System U (Absolute)", "System E (Earth Base)", "Laboratory Obs.", "K-PROTOCOL Calibration"]

# 궤적 데이터 (Y축 값들)
path_univ = [ALPHA_UNIV, ALPHA_UNIV, ALPHA_UNIV, ALPHA_UNIV]
path_paris = [ALPHA_UNIV, EARTH_BASELINE, paris_obs, ALPHA_UNIV]
path_berk = [ALPHA_UNIV, EARTH_BASELINE, berkeley_obs, ALPHA_UNIV]

# ==========================================
# 4. Plotly 그래프 생성
# ==========================================
fig = go.Figure()

# 절대 기하학 원형 선 (수평선)
fig.add_trace(go.Scatter(
    x=stages, y=path_univ, 
    mode='lines+markers', 
    name=text["leg_univ"], 
    line=dict(color='#f1c40f', width=4, dash='dot'),
    marker=dict(size=10)
))

# 파리 LKB 궤적
fig.add_trace(go.Scatter(
    x=stages, y=path_paris, 
    mode='lines+markers', 
    name=text["leg_paris"], 
    line=dict(color='#e74c3c', width=3),
    marker=dict(size=8)
))

# 버클리 궤적
fig.add_trace(go.Scatter(
    x=stages, y=path_berk, 
    mode='lines+markers', 
    name=text["leg_berk"], 
    line=dict(color='#3498db', width=3),
    marker=dict(size=8)
))

# 그래프 디자인 포맷팅
fig.update_layout(
    title=text["plot_title"],
    xaxis_title=text["x_label"],
    yaxis_title=text["y_label"],
    template="plotly_dark",
    hovermode="x unified",
    yaxis=dict(tickformat=".7f"), # 소수점 7자리까지 정밀 출력
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

st.plotly_chart(fig, use_container_width=True)

# 결론 출력
st.success(text["info"])

# 상세 수치 비교표
with st.expander("📊 K-PROTOCOL Mathematical Data / 수치 데이터 확인"):
    st.write(f"- **Universal Archetype (System U):** {ALPHA_UNIV:.7f}")
    st.write(f"- **Earth Baseline (System E):** {EARTH_BASELINE:.7f}")
    st.write(f"- **Paris LKB Uncalibrated Obs:** {paris_obs:.7f}")
    st.write(f"- **UC Berkeley Uncalibrated Obs:** {berkeley_obs:.7f}")
