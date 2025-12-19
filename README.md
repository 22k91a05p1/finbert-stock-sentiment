# 📈 Real-Time Stock Sentiment Analysis (FinBERT)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Postgres](https://img.shields.io/badge/PostgreSQL-13-blue)
![Model](https://img.shields.io/badge/AI-FinBERT-orange)

## 🚀 Overview
This project is a real-time data pipeline that quantifies market sentiment from unstructured financial discussions on Reddit (e.g., r/wallstreetbets). 

Unlike generic NLP models, this system utilizes **FinBERT**, a Transformer model fine-tuned specifically on financial text. This allows the system to correctly interpret domain-specific terms (e.g., "Rate Cut" as Positive/Bullish rather than Negative).

The application is fully containerized using **Docker** and visualizes live trends via a **Streamlit** dashboard.

---

## 🏗️ Architecture
The system follows a **Producer-Consumer** architecture decoupled by a persistent database layer.

![Architecture Diagram](./assets/architecture_diagram.png)

1.  **Ingestion Layer:** Python script uses **PRAW** to stream comments from Reddit in real-time.
2.  **Processing Layer:** **FinBERT** (Hugging Face) performs inference to classify sentiment (Positive, Negative, Neutral).
3.  **Persistence Layer:** Results are stored in **PostgreSQL** to ensure data integrity and historical analysis.
4.  **Presentation Layer:** **Streamlit** fetches data from the DB to render live charts.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **ML Model:** FinBERT (ProsusAI/finbert)
* **Data Source:** Reddit API (PRAW)
* **Database:** PostgreSQL
* **Containerization:** Docker & Docker Compose
* **Frontend:** Streamlit

---

## ⚙️ Setup & Installation

### Prerequisites
* Docker & Docker Compose installed
* Reddit API Credentials (client_id, client_secret)

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/stock-sentiment-finbert.git](https://github.com/22k91a05p1/stock-sentiment-finbert.git)
cd stock-sentiment-finbert
