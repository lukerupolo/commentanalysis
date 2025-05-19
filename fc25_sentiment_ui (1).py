
import streamlit as st
import pandas as pd

# Title
st.title("🧠 FC25 Sentiment Correction UI")

# Upload original batch
uploaded_file = st.file_uploader("Upload model predictions CSV (with blank 'Corrected Sentiment')", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Corrected Sentiment" not in df.columns:
        st.error("CSV must include a 'Corrected Sentiment' column.")
    else:
        st.write("### Step 1: Review and Correct Predictions")
        for i in range(len(df)):
            st.markdown("---")
            st.write(f"**Comment {i+1}:** {df.loc[i, 'Comment']}")
            st.write(f"Model Prediction: `{df.loc[i, 'Model Prediction']}`")
            corrected = st.radio("Corrected Sentiment:",
                                 ["", "Positive", "Negative", "Neutral"],
                                 index=["", "Positive", "Negative", "Neutral"].index(df.loc[i, "Corrected Sentiment"]) if df.loc[i, "Corrected Sentiment"] in ["Positive", "Negative", "Neutral"] else 0,
                                 key=i)
            df.loc[i, "Corrected Sentiment"] = corrected

        # Download final corrected CSV
        st.markdown("### Step 2: Export Corrected File")
        corrected_df = df[df["Corrected Sentiment"] != ""]
        st.write(f"✅ You have corrected {len(corrected_df)} comments.")

        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df_to_csv(corrected_df)
        st.download_button("📥 Download Corrected CSV", csv, "corrected_sentiment_batch.csv", "text/csv")
