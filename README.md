# 🧠 Mental Health in Tech Dashboard

![Banner](https://img.shields.io/badge/Built%20With-Streamlit-blue?style=flat&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A professional, interactive dashboard that visualizes the complex relationship between mental health and careers in tech or the pursuit of a CS degree.  
Developed by **Reda HEDDAD**, this project merges technical insight with human-centered design to offer a data-driven narrative around burnout, treatment, and stress in the industry.

---

## 🧩 Project Overview

This dashboard was created for a course evaluation focused on data visualization, design thinking, and interaction design. It pulls real-world survey data from:

- 📄 OSMI Mental Health in Tech Survey
- 📄 Stack Overflow Developer Survey
- 🌐 Public mental health APIs (optional)

Users can explore patterns in stress, treatment-seeking, and job satisfaction based on age, gender, job role, country, and more.

---

## 🧭 Dashboard Pages

| Page | Description |
|------|-------------|
| **About Me** | Brief profile page for the author with image, bio, and contact links |
| **Mental Health Trends** | Timelines and breakdowns of stress, burnout, and treatment outcomes across age and org size |
| **CS vs Mental Health** | Comparison of mental health indicators across tech roles and CS degrees |
| **Global Perspective** | Choropleth and bar charts showing support systems and awareness by country |
| **Deep Dive Visuals** | Advanced correlation charts and sentiment-based trend analysis (WIP) |

---

## 🎨 Design Sketches & Visual Choices

### ✅ Design Justification

- **Colors**: Calming blues, greens, and teals chosen to reflect a mental health tone.
- **Chart Types**:
  - Line charts for time-series insights (burnout over age)
  - Area/stacks for distribution clarity (org size vs treatment)
  - Stacked bar charts for remote work vs interference
  - Choropleth for global support comparison

### 🖍 Sketch Screenshot (Design Phase)
> ![Sketch](assets/sketch_placeholder.png)

### 🖥️ Prototype Screenshot (Current Stage)
> ![Prototype](assets/prototype_placeholder.png)

---

## 🔁 Interactions

- Sidebar filters (country, gender, age group, org size)
- Animated hover tooltips with exact stats
- Downloadable charts and data
- Responsive layout (desktop/mobile)
- Future: sentiment engine to explain text-based feedback

---

## 📈 Technologies Used

- Python
- Streamlit
- Plotly (Plotly Express)
- Pandas
- Altair (optional)
- PIL (for images)

---

## 💻 Run It Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/mental_health_dashboard.git
cd mental_health_dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py

```

✍️ Reflection
🤔 Challenges Faced
Dataset cleaning and alignment across two large surveys

Handling missing values while preserving user interactivity

Configuring Streamlit pages with custom modules and CSS

🧠 What I Learned
Building multi-page, modular Streamlit apps with custom visual theming

Designing dashboards for storytelling, not just raw data display

Importance of filters, interactivity, and layout hierarchy in UX

🔍 Group Meeting Takeaways
Feedback led to improved layout on smaller screens

Added hover explanations and cleaner metric boxes

Peers liked the “About Me” section for personalization

🔗 Resources & References
Streamlit Docs

Plotly Express

OSMI Survey

Stack Overflow Developer Survey


### Link to the demo
https://mentalhealthwebappbyreda.streamlit.app/
