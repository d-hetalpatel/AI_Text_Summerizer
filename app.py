# app.py
import streamlit as st
from summarizer_robust import summarize_text

st.set_page_config(page_title="AI Text Summarizer", layout="centered")

# App title and intro
st.title("🧠 AI Text Summarizer")
st.write("""
This app uses a **Transformer-based model (BART)** to generate concise summaries of long texts.  
Enter any article, paragraph, or report below, and click **Summarize** to get the key points instantly.
""")

# User input area
user_input = st.text_area("✍️ Enter your text here:", height=250)

# Slider for max summary length
max_words = st.slider("🔧 Summary Length (approx. words):", 50, 200, 130)

# Summarize button
if st.button("✨ Summarize"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some text first.")
    else:
        with st.spinner("⏳ Generating summary... please wait."):
            try:
                result = summarize_text(user_input, max_words=max_words)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("✅ Summary generated successfully!")
                    st.subheader("🧾 Summary:")
                    st.write(result["summary"])

                    st.markdown("---")
                    st.markdown(f"**📊 Original Length:** {result['original_length']} words")
                    st.markdown(f"**✂️ Summary Length:** {result['summary_length']} words")
                    st.markdown(f"**📖 Readability Score:** {result['readability']} (Flesch Reading Ease)")

                    # Option to download summary
                    st.download_button(
                        label="💾 Download Summary",
                        data=result["summary"],
                        file_name="summary.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error: {e}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Hugging Face Transformers and Streamlit.")
