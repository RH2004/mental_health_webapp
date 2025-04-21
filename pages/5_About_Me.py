import streamlit as st
from PIL import Image

# --- Page config ---
st.set_page_config(page_title="About Me", page_icon="👤", layout="centered")

# --- Load Image ---
# Get the path to the current file and build relative path to image
image_path = os.path.join(os.path.dirname(__file__), '..', 'assests', 'reda.jpg')
image = Image.open(image_path)

# --- Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.image(image, caption="Reda HEDDAD", width=220)

with col2:
    st.markdown("## 👋 Hello, I'm Reda HEDDAD")
    st.markdown("""
    I'm a **Computer Science student** with a minor in **Business Administration**, currently completing an exchange semester at the **University of Helsinki**.

    I'm passionate about:
    - 🤖 Artificial Intelligence & Data Science  
    - 🧱 Full-Stack Development  
    - 📊 Building meaningful, data-driven applications like this dashboard

    My work blends empathy, tech, and storytelling — from predicting real-world events using ML to building community-centered platforms like **DevConnect**.

    ---  
    🔗 **Connect with me:**

    - [![GitHub](https://img.shields.io/badge/GitHub-%2312100E.svg?style=flat&logo=github&logoColor=white)](https://github.com/RH2004)
    - [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/reda-heddad-7bb686258)
    """)

st.markdown("---")
st.markdown("© 2025 Reda HEDDAD — Powered by Streamlit")
