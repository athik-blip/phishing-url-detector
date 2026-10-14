import pandas as pd
import joblib
import streamlit as st
from features import extract_features

st.set_page_config(page_title='Phishing URL Detector',page_icon='🛡️')
st.title('🛡️ Phishing URL Detector')
st.caption('Educational machine-learning demo — a prediction is not a security guarantee.')
@st.cache_resource
def load_model():
    return joblib.load('phishing_model.joblib')
try:
    saved = load_model()
except FileNotFoundError:
    st.error('Train the model first: python train.py')
    st.stop()
url = st.text_input('Enter a URL',placeholder='https://example.com/login')
if st.button('Analyze URL'):
    if not url.strip() or '.' not in url:
        st.warning('Please enter a valid-looking URL.')
    else:
        features = pd.DataFrame([extract_features(url)])[saved['columns']]
        prediction = int(saved['model'].predict(features)[0])
        confidence = max(saved['model'].predict_proba(features)[0])
        if prediction == 1:
            st.error(f'Potential phishing URL (model confidence: {confidence:.0%})')
        else:
            st.success(f'Likely legitimate URL (model confidence: {confidence:.0%})')
        st.warning('Do not enter passwords or sensitive information based only on this result.')
        with st.expander('URL features'):
            st.dataframe(features.T.rename(columns={0:'Value'}))
