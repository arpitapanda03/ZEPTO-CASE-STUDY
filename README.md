# 🛒 Zepto Customer Analytics Dashboard

An interactive Streamlit dashboard for analysing Zepto's customer dataset (10,000 records, 2023–2024).

## 📊 Features
- KPI cards: Total Customers, Avg Age, Cities & States covered
- Gender distribution (donut chart)
- Age group distribution (bar chart)
- Top 10 States & Cities
- Monthly signup trend (line chart)
- Gender × Age Group heatmap
- Year-wise customer growth by gender
- Sidebar filters: Year, State, Gender, Age Range
- Download filtered data as CSV

## 🗂️ Project Structure
```
zepto_dashboard/
├── app.py                 # Main Streamlit app
├── Zepto_Dataset.xlsx     # Dataset
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

## 🚀 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy on Streamlit Cloud
1. Push this repo to GitHub
2. Go to https://share.streamlit.io
3. Click **New app** → select your repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

## 🛠️ Tech Stack
- Python, Streamlit, Plotly, Pandas, OpenPyXL
