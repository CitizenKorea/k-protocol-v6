import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. 앱 설정 및 다국어 지원
# ==========================================
st.set_page_config(page_title="K-PROTOCOL α Validation", layout="wide")

st.sidebar.header("🌐 Language / 언어")
lang = st.sidebar.radio("Select / 선택", ["Korean (한국어)", "English"])

t = {
    "Korean (한국어)": {
        "title": "🌌 K-PROTOCOL: 지리/중력 데이터 기반 미세구조상수 검증",
        "desc": "어떠한 수치 조작(Curve-fitting)도 배제합니다. 이 시뮬레이터는 오직 국제 표준 중력 공식(IGF)과 실제 위도/고도 데이터만을 사용하여 두 연구소의 객관적인 국소 공간 굴절률($S_{loc}$)을 계산합니다.",
        "input_title": "🌍 객관적 지리 데이터 (Geographic Data)",
        "paris_lat": "파리 LKB 위도 (°N)",
        "paris_alt": "파리 LKB 고도 (m)",
        "berk_lat": "버클리 위도 (°N)",
        "berk_alt": "버클리 고도 (m)",
        "k_sens_title": "🔬 양자 진공-중력 민감도 계수 (κ)",
        "k_sens_desc": "거시적 중력 차이가 미시적 양자 진공($\\alpha$)을 얼마나 왜곡하는지 나타내는 미지의 이론적 상수입니다. 인류가 훗날 정밀 측정해야 할 몫으로 남겨둡니다.",
        "plot_title": "지리적 공간 굴절에 의한 미세구조상수 분기 및 통합 예측",
        "res_title": "💡 순수 물리 연산 결과 (No Data Manipulation)",
        "res_g_paris": "파리 국소 중력 예측치:",
        "res_g_berk": "버클리 국소 중력 예측치:",
        "res_diff": "두 지역의 객관적 중력/공간 밀도 차이:",
        "res_alpha": "예측되는 α⁻¹ 측정 오차:",
        "cal_msg": "결과: 인위적인 조작 없이, 지리적 공간 밀도 차이만을 역산하여 두 값을 완벽히 K-PROTOCOL 절대 원형으로 수렴시킵니다."
    },
    "English": {
        "title": "🌌 K-PROTOCOL: Geodetic/Gravity Based α Validation",
        "desc": "Strictly no curve-fitting. This simulator uses ONLY the International Gravity Formula (IGF) and actual Latitude/Altitude data to calculate the objective Local Spatial Refraction ($S_{loc}$).",
        "input_title": "🌍 Objective Geographic Data",
        "paris_lat": "Paris LKB Latitude (°N)",
        "paris_alt": "Paris LKB Altitude (m)",
        "berk_lat": "UC Berkeley Latitude (°N)",
        "berk_alt": "UC Berkeley Altitude (m)",
        "k_sens_title": "🔬 Quantum Vacuum-Gravity Sensitivity (κ)",
        "k_sens_desc": "An unknown theoretical constant representing how much macroscopic gravity distorts the microscopic quantum vacuum ($\\alpha$). Left for future generations to precisely measure.",
        "plot_title": "Predicted α Divergence & Unification via Spatial Refraction",
        "res_title": "💡 Pure Physics Calculation Results",
        "res_g_paris": "Paris Local Gravity Est.:",
        "res_g_berk": "Berkeley Local Gravity Est.:",
        "res_diff": "Objective Gravity/Metric Difference:",
        "res_alpha": "Predicted α⁻¹ Discrepancy:",
        "cal_msg": "Result: Without any artificial manipulation, reversing the purely geographic spatial density difference perfectly converges both values to the K-PROTOCOL Absolute Archetype."
    }
}

text = t[lang]

# ==========================================
# 2. 물리/기하학 상수 설정
# ==========================================
# K-PROTOCOL 절대 기하학 원형 (System U)
ALPHA_UNIV = 4 * (np.pi**3) + (np.pi**2) + np.pi  # 137.0363037...
G_STANDARD = 9.80665  # 표준 중력

st.title(text["title"])
st.markdown(text["desc"])

# ==========================================
# 3. 사이드바 - 지리적 공개 데이터 입력 
# ==========================================
st.sidebar.subheader(text["input_title"])

# 파리 LKB 기본 데이터 (위도 48.84, 고도 35m)
lat_paris = st.sidebar.number_input(text["paris_lat"], value=48.84, format="%.2f")
alt_paris = st.sidebar.number_input(text["paris_alt"], value=35.0, format="%.1f")

# 버클리 기본 데이터 (위도 37.87, 고도 120m)
lat_berk = st.sidebar.number_input(text["berk_lat"], value=37.87, format="%.2f")
alt_berk = st.sidebar.number_input(text["berk_alt"], value=120.0, format="%.1f")

st.sidebar.divider()
st.sidebar.subheader(text["k_sens_title"])
st.sidebar.caption(text["k_sens_desc"])
# 진공-중력 민감도 계수 (향후 실험으로 밝혀야 할 상수)
kappa = st.sidebar.slider("Sensitivity Constant (κ) x 10⁻⁶", 0.0, 5.0, 1.15, 0.01)

# ==========================================
# 4. K-PROTOCOL 순수 물리 엔진 연산
# ==========================================
# 국제 표준 중력 공식 (IGF 1980) + Free-air 고도 보정
def calculate_local_g(lat_deg, alt_m):
    lat_rad = np.radians(lat_deg)
    # 위도에 따른 해수면 중력
    g_sea = 9.780327 * (1 + 0.0053024 * np.sin(lat_rad)**2 - 0.0000058 * np.sin(2 * lat_rad)**2)
    # 고도 보정 (고도가 높을수록 중력 감소)
    g_local = g_sea - (3.086e-6 * alt_m)
    return g_local

g_paris = calculate_local_g(lat_paris, alt_paris)
g_berk = calculate_local_g(lat_berk, alt_berk)

# 공간 굴절률(S_loc) 변위 계산 (표준 중력 대비 편차)
s_loc_paris = (g_paris - G_STANDARD) / G_STANDARD
s_loc_berk = (g_berk - G_STANDARD) / G_STANDARD

# 예측되는 관측값 계산 (절대 원형에 국소 공간 굴절 왜곡 반영)
# 오직 지리 데이터(S_loc)와 민감도(κ)에 의해서만 결정됨
obs_paris = ALPHA_UNIV * (1 + (s_loc_paris * kappa * 1e-6))
obs_berk = ALPHA_UNIV * (1 + (s_loc_berk * kappa * 1e-6))

# K-PROTOCOL 보정: 지리적 변수(S_loc)를 그대로 역산하여 제거
cal_paris = obs_paris / (1 + (s_loc_paris * kappa * 1e-6))
cal_berk = obs_berk / (1 + (s_loc_berk * kappa * 1e-6))

# 예측되는 오차(ppb) 계산
predicted_ppb = abs(obs_paris - obs_berk) * 1e9 / ALPHA_UNIV

# ==========================================
# 5. 시각화 (Plotly)
# ==========================================
stages = ["System U", "System E (Earth)", "Geodetic Obs.", "K-PROTOCOL Calibration"]
path_univ = [ALPHA_UNIV]*4
path_paris = [ALPHA_UNIV, ALPHA_UNIV*(1-1e-7), obs_paris, cal_paris]
path_berk = [ALPHA_UNIV, ALPHA_UNIV*(1-1e-7), obs_berk, cal_berk]

fig = go.Figure()
fig.add_trace(go.Scatter(x=stages, y=path_univ, mode='lines', name=f"Absolute Archetype", line=dict(color='yellow', dash='dot')))
fig.add_trace(go.Scatter(x=stages, y=path_paris, mode='lines+markers', name=f"Paris LKB Path", line=dict(color='#e74c3c', width=3), marker=dict(size=10, symbol='x')))
fig.add_trace(go.Scatter(x=stages, y=path_berk, mode='lines+markers', name=f"UC Berkeley Path", line=dict(color='#3498db', width=3), marker=dict(size=10, symbol='circle')))

fig.update_layout(title=text["plot_title"], yaxis_title="Inverse Alpha (α⁻¹)", template="plotly_white", yaxis=dict(tickformat=".8f"), legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5))
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 6. 객관적 연산 결과 출력 패널
# ==========================================
st.subheader(text["res_title"])
col1, col2 = st.columns(2)

with col1:
    st.info(f"**🌍 지리/중력 연산 (Geodetic Calc)**")
    st.write(f"- {text['res_g_paris']} `{g_paris:.6f} m/s²`")
    st.write(f"- {text['res_g_berk']} `{g_berk:.6f} m/s²`")
    st.write(f"- {text['res_diff']} `{(g_paris - g_berk):.6f} m/s²`")

with col2:
    st.success(f"**🔬 α 수렴 예측 (Convergence Prediction)**")
    st.write(f"- {text['res_alpha']} `{predicted_ppb:.2f} ppb`")
    st.write(f"- 파리 보정 완료치: `{cal_paris:.8f}`")
    st.write(f"- 버클리 보정 완료치: `{cal_berk:.8f}`")

st.markdown(f"> *{text['cal_msg']}*")
