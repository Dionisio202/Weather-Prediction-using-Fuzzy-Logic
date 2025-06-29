# 🌤️ Weather Prediction using Fuzzy Logic & Association Rules

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**A sophisticated web-based system for predicting weather precipitation using AI techniques**

[🚀 Demo](#-demo) • [📋 Features](#-features) • [🛠️ Installation](#️-installation--setup) • [📖 Documentation](#-how-it-works)

</div>

---

## 📖 Overview

This project implements an intelligent weather prediction system that combines **Fuzzy Logic** and **Association Rule Mining** to predict precipitation levels. Built with Flask and powered by real meteorological data from Weatherbit, the system provides accurate precipitation forecasts through an intuitive web interface.

### 🎯 Key Highlights

- 🤖 **AI-Powered**: Uses Fuzzy Inference Systems and Association Rules
- 📊 **Data-Driven**: Based on real weather data from Weatherbit API
- 🌐 **Web Interface**: Interactive Flask application with real-time predictions
- 📈 **Visualizations**: Dynamic charts for membership functions and defuzzification
- ⚡ **Optimized**: Genetic algorithm for feature selection

---

## 🚀 Demo

### 🖥️ Main Interface
<div align="center">
  <img src="./main.png" alt="Main View" />
</div>

### 📊 Prediction Results
<table>
<tr>
<td width="50%">

![Prediction Result](./result.png)
**Prediction Output**
- Precipitation level interpretation
- Numerical defuzzified value
- Confidence degree

</td>
<td width="50%">

![Aggregation Graph](./grafico_aggregacion.png)
**Defuzzification Process**
- Aggregated membership visualization
- Centroid calculation display

</td>
</tr>
</table>

### 📈 Membership Functions
![Membership Functions](./grafico.png)

> **Visual representation of triangular membership functions for all meteorological variables**

---

## ✨ Features

<table>
<tr>
<td>

### 🎯 **Core Features**
- ✅ Interactive web application (Flask)
- ✅ Real-time weather prediction
- ✅ Fuzzy logic inference system
- ✅ Association rule mining
- ✅ Dynamic visualization graphs

</td>
<td>

### 🔬 **AI Techniques**
- ✅ Genetic algorithm optimization
- ✅ Apriori-style rule mining
- ✅ Triangular membership functions
- ✅ Centroid defuzzification
- ✅ Feature correlation analysis

</td>
</tr>
</table>

---

## 🧠 AI Algorithms

<details>
<summary><b>🔍 Association Rule Mining</b></summary>

```python
# Implemented in priori.py
- Purpose: Extract relevant patterns from discretized weather data
- Metrics: Support, Confidence, Lift
- Output: High-confidence rules (lift > 1)
- Example: If (Clouds=High AND Wind_Gust=High) → Precipitation=High
```

**Key Benefits:**
- Automatic rule discovery from data
- Statistical significance validation
- Interpretable weather patterns

</details>

<details>
<summary><b>🧬 Genetic Algorithm</b></summary>

```python
# Implemented in genetico.py  
- Purpose: Optimize meteorological feature selection
- Objective: Minimize inter-feature correlation
- Process: Selection → Crossover → Mutation
- Output: Best subset of predictive variables
```

**Optimization Process:**
- Population-based search
- Fitness function based on correlation
- Multi-generational evolution

</details>

<details>
<summary><b>🌐 Fuzzy Inference System</b></summary>

```python
# Implemented in fuzzy.py + api.py
- Engine: scikit-fuzzy
- Variables: 7 inputs + 1 output  
- Functions: Triangular membership
- Method: Centroid defuzzification
```

**System Architecture:**
- Dynamic rule base construction
- Real-time inference processing
- Uncertainty quantification

</details>

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### 🚀 Quick Start

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Dionisio202/Weather-Prediction-using-Fuzzy-Logic
cd weather-prediction

# 2️⃣ Create virtual environment
python -m venv venv

# 3️⃣ Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4️⃣ Install dependencies
pip install -r requirements.txt

# 5️⃣ Run the application
python api.py
```

### 🌐 Access the Application
Navigate to `http://localhost:5000` in your web browser

---

## 📁 Project Structure

```
WEATHER-PREDICTION/
│
├── 📱 Frontend
│   ├── templates/           # HTML templates
│   │   ├── index.html      # Main interface
│   │   └── resultado.html  # Results page
│   └── static/             # Static assets
│       └── precipitacion.jpg
│
├── 🧠 AI Core
│   ├── api.py              # Flask web application
│   ├── fuzzy.py            # Fuzzy logic engine
│   ├── priori.py           # Association rule mining
│   └── genetico.py         # Genetic algorithm
│
├── 📊 Data Processing
│   ├── discretizacion.py   # Data discretization
│   ├── datos_weatherbit_diarios.csv    # Raw dataset
│   ├── datos_discretizados.csv         # Processed dataset
│   └── reglas_generadas.txt           # Generated rules
│
├── 🔧 Utilities
│   ├── comprobar_reglas.py # Rule validation
│   └── a_difuso.py         # Legacy fuzzy version
│
└── 📋 Configuration
    ├── requirements.txt    # Dependencies
    └── README.md          # Documentation
```

---

## 📈 How It Works

<table>
<tr>
<td width="25%" align="center">

### 1️⃣ 
![Data Icon](https://img.shields.io/badge/-DATA-blue?style=for-the-badge&logo=database)
**Data Preparation**

Raw weather data from Weatherbit API is discretized using scientific binning thresholds

</td>
<td width="25%" align="center">

### 2️⃣
![Rules Icon](https://img.shields.io/badge/-RULES-green?style=for-the-badge&logo=sitemap)
**Rule Mining**

Association rules are extracted using support, confidence, and lift metrics

</td>
<td width="25%" align="center">

### 3️⃣
![Fuzzy Icon](https://img.shields.io/badge/-FUZZY-orange?style=for-the-badge&logo=shuffle)
**Fuzzy System**

Membership functions and inference rules create the prediction model

</td>
<td width="25%" align="center">

### 4️⃣
![Web Icon](https://img.shields.io/badge/-WEB-red?style=for-the-badge&logo=globe)
**Web Interface**

Users interact through sliders and receive visual predictions

</td>
</tr>
</table>

### 📊 Input Variables
| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| Horizontal Irradiation | Continuous | 0-1000 W/m² | Solar energy received |
| Wind Gust Speed | Continuous | 0-50 m/s | Maximum wind speed |
| Solar Radiation | Continuous | 0-1000 W/m² | Direct solar energy |
| Direct Radiation | Continuous | 0-800 W/m² | Beam solar radiation |
| Cloudiness | Discrete | Low/Medium/High | Cloud cover percentage |
| Atmospheric Pressure | Continuous | 950-1050 hPa | Air pressure |
| Wind Direction | Categorical | N/S/E/W | Cardinal directions |

### 🎯 Output
- **Precipitation Level**: Low, Medium, High
- **Numerical Value**: Exact defuzzified output
- **Confidence**: Membership degree in predicted category

---

## 🛡️ Technologies Used

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![Scikit](https://img.shields.io/badge/scikit--fuzzy-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

</div>

### 🔧 Core Dependencies
- **Flask**: Web framework for the user interface
- **scikit-fuzzy**: Fuzzy logic computation engine
- **matplotlib**: Visualization and plotting
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing foundation

---

## 📊 Dataset Information

<div align="center">

### 🌍 Data Source: [Weatherbit.io](https://www.weatherbit.io/)

</div>

| **Attribute** | **Details** |
|---------------|-------------|
| **Source** | Professional weather data API |
| **Coverage** | Daily meteorological observations |
| **Variables** | Temperature, Pressure, Wind, Clouds, Solar Radiation, Precipitation |
| **Processing** | Scientific binning based on meteorological standards |
| **Format** | CSV files with discretized categorical values |

> **Note**: The dataset has been preprocessed and discretized for optimal fuzzy inference performance

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌱 **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 **Push** to the branch (`git push origin feature/AmazingFeature`)
5. 🔄 **Open** a Pull Request

### 💡 Ideas for Contributions
- Additional weather variables integration
- Alternative defuzzification methods
- Performance optimization
- Mobile-responsive design improvements
- API endpoint extensions

---





---

## 🙏 Acknowledgments

- **Weatherbit.io** for providing high-quality meteorological data
- **scikit-fuzzy** team for the excellent fuzzy logic library
- **Flask** community for the robust web framework
- Weather prediction research community for inspiration and methodological guidance

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

**Made with ❤️ and ☕ for the weather prediction community**

</div>