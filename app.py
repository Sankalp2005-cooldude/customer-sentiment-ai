import streamlit as st
from transformers import pipeline
import plotly.express as px
import collections

# Set up page styling
st.set_page_config(page_title="AI Sentiment Portal", layout="wide")

# Load the free Hugging Face NLP pipeline (Cached so it only loads once)
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

analyzer = load_sentiment_model()

st.title("📊 AI Customer Feedback Sentiment & Insights Portal")
st.markdown("Analyze raw customer reviews, track satisfaction trends, and extract key insights instantly.")

tab1, tab2 = st.tabs(["📝 Single Review Analysis", "📈 Batch Upload & Analytics"])

with tab1:
    st.subheader("Analyze Individual Feedback")
    user_input = st.text_area("Paste a customer review here:", placeholder="The product arrived late and customer service was unhelpful...")
    
    if st.button("Analyze Review"):
        if user_input.strip():
            result = analyzer(user_input)[0]
            label = result['label']
            score = round(result['score'] * 100, 2)
            
            if label == "POSITIVE":
                st.success(f"😊 **Positive Sentiment Detected!** (Confidence: {score}%)")
            else:
                st.error(f"😡 **Negative Sentiment Detected!** (Confidence: {score}%)")
        else:
            st.warning("Please type or paste some text first.")

with tab2:
    st.subheader("Batch Analysis Simulator")
    st.markdown("Paste multiple reviews (one per line) to simulate an automated enterprise feedback loop.")
    
    sample_data = (
        "The battery life is incredible, easily lasts two days.\n"
        "Terrible experience. The app keeps crashing on startup.\n"
        "Delivery was quick but the packaging was slightly damaged.\n"
        "Absolute waste of money. It stopped working after one week.\n"
        "Great customer support, they resolved my issue in minutes!"
    )
    
    batch_input = st.text_area("Paste batch reviews (One review per line):", value=sample_data, height=150)
    
    if st.button("Generate Dashboard Analytics"):
        reviews = [r.strip() for r in batch_input.split("\n") if r.strip()]
        
        if reviews:
            results = analyzer(reviews)
            labels = [res['label'] for res in results]
            counts = collections.Counter(labels)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric(label="Total Reviews Analyzed", value=len(reviews))
                st.metric(label="Positive Reviews", value=counts.get("POSITIVE", 0))
                st.metric(label="Negative Reviews", value=counts.get("NEGATIVE", 0))
                
            with col2:
                fig = px.pie(
                    names=list(counts.keys()), 
                    values=list(counts.values()), 
                    title="Overall Customer Sentiment Breakdown",
                    color=list(counts.keys()),
                    color_discrete_map={'POSITIVE': '#2ca02c', 'NEGATIVE': '#d62728'}
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please provide valid data.")