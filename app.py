# -*- coding: utf-8 -*-
import streamlit as st
import requests

API_URL = "http://43.134.26.196/predict"

# (label, default) per feature, grouped the way the model expects them (mean, error, worst).
# Defaults are the per-feature averages of the Breast Cancer Wisconsin (Diagnostic) dataset,
# see the DATA_SOURCES links below for where these 30 features come from.
FEATURE_GROUPS = {
    "mean": [
        ("Radius", 14.13),
        ("Texture", 19.29),
        ("Perimeter", 91.97),
        ("Area", 654.89),
        ("Smoothness", 0.0964),
        ("Compactness", 0.1043),
        ("Concavity", 0.0888),
        ("Concave Points", 0.0489),
        ("Symmetry", 0.1812),
        ("Fractal Dimension", 0.0628),
    ],
    "error": [
        ("Radius Error", 0.4052),
        ("Texture Error", 1.2169),
        ("Perimeter Error", 2.8661),
        ("Area Error", 40.34),
        ("Smoothness Error", 0.0070),
        ("Compactness Error", 0.0255),
        ("Concavity Error", 0.0319),
        ("Concave Points Error", 0.0118),
        ("Symmetry Error", 0.0205),
        ("Fractal Dimension Error", 0.0038),
    ],
    "worst": [
        ("Worst Radius", 16.27),
        ("Worst Texture", 25.68),
        ("Worst Perimeter", 107.26),
        ("Worst Area", 880.58),
        ("Worst Smoothness", 0.1324),
        ("Worst Compactness", 0.2543),
        ("Worst Concavity", 0.2722),
        ("Worst Concave Points", 0.1146),
        ("Worst Symmetry", 0.2901),
        ("Worst Fractal Dimension", 0.0839),
    ],
}

DATA_SOURCES = [
    (
        "scikit-learn: Breast Cancer Wisconsin (Diagnostic) Dataset",
        "https://scikit-learn.org/stable/datasets/toy_dataset.html#breast-cancer-wisconsin-diagnostic-dataset",
    ),
    (
        "UCI Machine Learning Repository: Breast Cancer Wisconsin (Diagnostic)",
        "https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic",
    ),
]

TEXTS = {
    "id": {
        "page_title": "Prediksi Kanker Payudara",
        "language_label": "🌐 Bahasa",
        "about_header": "🩺 Tentang",
        "about_body1": (
            "Aplikasi ini memprediksi apakah tumor payudara **jinak (benign)** "
            "atau **ganas (malignant)** menggunakan model SVM yang dilatih "
            "dengan dataset Wisconsin Diagnostic Breast Cancer."
        ),
        "about_body2": (
            "Isi 30 pengukuran (dikelompokkan sebagai Mean / Error / Worst), "
            "lalu klik **Predict**. Kolom sudah terisi nilai rata-rata dataset "
            "sebagai contoh awal."
        ),
        "api_caption": "Endpoint API: `{url}`",
        "data_source_header": "📚 Sumber Data",
        "data_source_body": (
            "30 fitur beserta artinya (mean / error / worst "
            "dari tiap pengukuran) berasal dari:"
        ),
        "title": "🩺 Prediksi Kanker Payudara",
        "subtitle": "Isi 30 hasil pengukuran tumor di bawah ini, lalu klik **Predict**.",
        "tab_mean": "Mean",
        "tab_error": "Error",
        "tab_worst": "Worst",
        "predict_button": "🔍 Predict",
        "reset_button": "↺ Reset",
        "spinner_text": "Menghubungi API model...",
        "error_connection": "Tidak dapat terhubung ke API prediksi: {e}",
        "error_response": "API mengembalikan respons yang tidak terduga.",
        "result_header": "Hasil",
        "prediction_label": "Prediksi: **{label}**",
        "benign_label": "Jinak",
        "malignant_label": "Ganas",
        "confidence_label": "Tingkat Keyakinan",
    },
    "en": {
        "page_title": "Breast Cancer Prediction",
        "language_label": "🌐 Language",
        "about_header": "🩺 About",
        "about_body1": (
            "This app predicts whether a breast tumor is **benign** or "
            "**malignant** using an SVM model trained on the Wisconsin "
            "Diagnostic Breast Cancer dataset."
        ),
        "about_body2": (
            "Fill in the 30 measurements (grouped as Mean / Error / Worst), "
            "then click **Predict**. Fields are pre-filled with dataset "
            "averages as a starting point."
        ),
        "api_caption": "API endpoint: `{url}`",
        "data_source_header": "📚 Data Source",
        "data_source_body": (
            "The 30 features and their meaning (mean / error / "
            "worst of each measurement) come from:"
        ),
        "title": "🩺 Breast Cancer Prediction",
        "subtitle": "Enter the 30 tumor measurements below, then click **Predict**.",
        "tab_mean": "Mean",
        "tab_error": "Error",
        "tab_worst": "Worst",
        "predict_button": "🔍 Predict",
        "reset_button": "↺ Reset",
        "spinner_text": "Contacting model API...",
        "error_connection": "Could not reach the prediction API: {e}",
        "error_response": "The API returned an unexpected response.",
        "result_header": "Result",
        "prediction_label": "Prediction: **{label}**",
        "benign_label": "Benign",
        "malignant_label": "Malignant",
        "confidence_label": "Confidence",
    },
}

st.set_page_config(
    page_title="Breast Cancer Prediction",
    page_icon="🩺",
    layout="wide",
)

with st.sidebar:
    lang_choice = st.selectbox("🌐 Bahasa / Language", ["Indonesia", "English"])
    lang = "id" if lang_choice == "Indonesia" else "en"
    t = TEXTS[lang]

    st.header(t["about_header"])
    st.write(t["about_body1"])
    st.write(t["about_body2"])
    st.caption(t["api_caption"].format(url=API_URL))

    st.divider()
    st.subheader(t["data_source_header"])
    st.write(t["data_source_body"])
    for name, url in DATA_SOURCES:
        st.markdown(f"- [{name}]({url})")

st.title(t["title"])
st.write(t["subtitle"])

inputs = []
group_keys = list(FEATURE_GROUPS.keys())
tab_labels = [t[f"tab_{key}"] for key in group_keys]
tabs = st.tabs(tab_labels)

for tab, group_key in zip(tabs, group_keys):
    with tab:
        cols = st.columns(2)
        for i, (label, default) in enumerate(FEATURE_GROUPS[group_key]):
            with cols[i % 2]:
                value = st.number_input(
                    label,
                    min_value=0.0,
                    value=float(default),
                    format="%.4f",
                    key=f"{group_key}_{label}",
                )
                inputs.append(value)

st.divider()

col1, col2, col3 = st.columns([1, 1, 3])
predict_clicked = col1.button(t["predict_button"], type="primary", use_container_width=True)
reset_clicked = col2.button(t["reset_button"], use_container_width=True)

if reset_clicked:
    for group_key, features in FEATURE_GROUPS.items():
        for label, default in features:
            st.session_state[f"{group_key}_{label}"] = float(default)
    st.rerun()

if predict_clicked:
    with st.spinner(t["spinner_text"]):
        try:
            response = requests.post(API_URL, json={"features": inputs}, timeout=15)
            response.raise_for_status()
            hasil = response.json()
        except requests.exceptions.RequestException as e:
            st.error(t["error_connection"].format(e=e))
        except (KeyError, ValueError):
            st.error(t["error_response"])
        else:
            prediction = hasil["prediction"]
            probability = hasil["probability"]
            label = t["benign_label"] if prediction == 1 else t["malignant_label"]

            st.subheader(t["result_header"])
            res_col1, res_col2 = st.columns(2)

            with res_col1:
                if prediction == 1:
                    st.success(t["prediction_label"].format(label=label))
                else:
                    st.error(t["prediction_label"].format(label=label))

            with res_col2:
                st.metric(t["confidence_label"], f"{probability:.2%}")
                st.progress(min(max(probability, 0.0), 1.0))
