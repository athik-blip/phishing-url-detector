import pandas as pd
import joblib
import streamlit as st
from urllib.parse import urlparse
from features import extract_features

st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🛡️"
)

st.title("🛡️ Phishing URL Detector")

st.caption(
    "Educational machine-learning demo. "
    "Predictions are not a security guarantee."
)

@st.cache_resource
def load_model():
    return joblib.load("phishing_model.joblib")

try:
    saved = load_model()
except FileNotFoundError:
    st.error("Model file not found: phishing_model.joblib")
    st.stop()
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()

url = st.text_input(
    "Enter a URL",
    placeholder="https://www.microsoft.com/"
)

if st.button("Analyze URL"):
    candidate = url.strip()

    if not candidate:
        st.warning("Please enter a URL.")
        st.stop()

    if "://" not in candidate:
        candidate = "https://" + candidate

    parsed = urlparse(candidate)

    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or "." not in parsed.hostname
    ):
        st.error("Please enter a valid URL, such as https://example.com")
        st.stop()

    try:
        features = pd.DataFrame(
            [extract_features(candidate)]
        )[saved["columns"]]

        model = saved["model"]
        prediction = int(model.predict(features)[0])

        st.subheader("Analysis Result")

        if prediction == 1:
            st.error(
                "⚠️ The model flags this URL as potentially phishing."
            )
        else:
            st.success(
                "✅ The model classifies this URL as likely legitimate."
            )

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)[0]
            confidence = max(probabilities)

            st.write(
                f"Model confidence score: {confidence:.1%}"
            )

        st.warning(
            "This is a machine-learning prediction, "
            "not a guarantee of safety. Do not rely on it alone."
        )

        with st.expander("URL features"):
            st.dataframe(features.T.rename(columns={0: "Value"}))

    except Exception as e:
        st.error(f"Analysis failed: {e}")
        st.info(
            "Check features.py, the saved model, "
            "and the feature columns used during training."
        )