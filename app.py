import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

# App Header
st.title("✍️ AI Content Assistant")
st.write("Generate custom posts, captions, and hashtags instantly powered by Groq.")

# Sidebar for API Key input
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    help="Get a free key from https://console.groq.com/keys"
)

# Use key from sidebar input or fallback to Streamlit Secrets
groq_api_key = api_key_input or st.secrets.get("GROQ_API_KEY", "")

# Form Inputs
st.subheader("Post Parameters")

col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox(
        "Content Type",
        ["LinkedIn Post", "Instagram Post", "Twitter/X Thread", "Facebook Post", "Blog Intro"]
    )
    
    tone = st.selectbox(
        "Tone",
        ["Professional", "Casual & Friendly", "Persuasive", "Witty & Funny", "Educational", "Inspirational"]
    )

with col2:
    target_audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Software Engineers, Marketing Managers, Students"
    )
    
    selected_model = st.selectbox(
        "Groq Model",
        ["openai/gpt-oss-120b"]
    )

topic = st.text_area(
    "Topic / Core Message",
    placeholder="Describe what your post should be about..."
)

# Generate Button
if st.button("Generate Content", type="primary", use_container_width=True):
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar or set it in Streamlit Secrets!")
    elif not topic:
        st.warning("Please enter a topic or core message.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=groq_api_key)

            # Construct Prompt
            prompt = f"""
            You are an expert social media content creator and copywriter.
            Generate a high-engaging post based on the following requirements:

            - Content Type: {content_type}
            - Topic/Core Message: {topic}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Tone: {tone}

            Structure your response clearly with these sections:
            1. Main Post Body
            2. Catchy Caption (if applicable for social platforms)
            3. 5 to 10 Relevant Hashtags
            """

            with st.spinner("Generating content with Groq..."):
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "You are a professional AI marketing assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

            # Display Output
            generated_text = response.choices[0].message.content
            
            st.success("Content Generated Successfully!")
            st.markdown("---")
            st.markdown(generated_text)
            
            # Download option for the generated output
            st.download_button(
                label="Download Generated Content",
                data=generated_text,
                file_name="generated_content.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
