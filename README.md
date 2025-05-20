# Solar Challenge Week 1

A project starter template for data science and machine learning tasks, featuring a Streamlit dashboard for solar data analysis.

## 📦 Getting Started

Follow these steps to get your environment up and running.

### ✅ Prerequisites

Before you begin, make sure you have the following installed:

- 🐍 [Python 3.8+](https://www.python.org/)
- 🧰 [Git](https://git-scm.com/)
- 📁 [VS Code](https://code.visualstudio.com/) (recommended)

### ⚙️ Setup

1. **Clone the repository:**
```bash
git clone https://github.com/sentayhu19/solar-challenge-week1.git
cd solar-challenge-week1
```

2. **Create and activate a virtual environment:**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Running the Dashboard

1. **Prepare your data:**
   - Place cleaned CSV files in the `data/` directory:
     - `benin_clean.csv`
     - `sierraleone_clean.csv`
     - `togo_clean.csv`

2. **Launch the dashboard:**
```bash
cd app
streamlit run main.py
```

## 📊 Dashboard Features

- **Country Selection:** Choose countries to analyze
- **Metric Analysis:** Interactive visualizations for:
  - GHI (Global Horizontal Irradiance)
  - DNI (Direct Normal Irradiance)
  - DHI (Diffuse Horizontal Irradiance)
- **Visualizations:**
  - Distribution boxplots
  - Correlation heatmaps
  - Country rankings
- **Statistics:**
  - Summary tables
  - Statistical significance tests
- **Data Export:** Download analyzed data

## 👤 Contributor

**Sentayhu Berhanu**
- GitHub: [@sentayhu19](https://github.com/sentayhu19)
- Twitter: [@VoltageBerhanu](https://twitter.com/VoltageBerhanu)
- LinkedIn: [sentayhu-berhanu](https://www.linkedin.com/in/sentayhu-berhanu-6376579a/)
