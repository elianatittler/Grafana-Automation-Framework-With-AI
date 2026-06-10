# Grafana API & Web Automation Framework with AI-Driven Diagnostics

An advanced, production-ready automation framework designed for comprehensive testing of Grafana's API and Web UI layers. Built using **Python**, **Pytest**, and **Playwright**, this project demonstrates modern QA engineering patterns, including Data-Driven Testing (DDT), structured layers, and a custom **AI Error Handler** integrated directly into the test life cycle.

---

## 🚀 Key Features

- **Hybrid Automation Architecture:** Complete test coverage managing both REST API endpoints (Grafana Teams, Folders, Service Accounts) and Web UI application flows.
- **AI-Powered Diagnostics Framework:** Custom integration hooks inside `conftest.py` intercept failures dynamically and route them to an AI diagnostics engine (**Anthropic Claude 3.5 Sonnet**) for automated runtime root-cause analysis.
- **Built-in Mock Simulation Engine:** Safe fallbacks are engineered into the core AI handler to simulate and display dynamic contextual engineering hints if an active external API key is omitted.
- **Robust Multi-Layer Design:** Organized separation of test components (`tests/`), automation utilities (`utils/`), configurations, and data layers (`data/`).
- **Advanced Dynamic Reporting:** Ready integration with Allure Results for rich visual execution history and trace logs.

---

## 🛠️ Tech Stack & Dependencies

- **Core Language:** Python 3.14+
- **Test Runner:** Pytest 9.0.2
- **Web Automation Engine:** Playwright (Sync API)
- **AI Orchestration:** Anthropic API SDK
- **Reporting System:** Allure Pytest Plugin

---

## 🚀 Quick Start & Directory Structure

Get the framework up and running locally in less than 2 minutes:

```text
1. Clone the repository:
   git clone [https://github.com/elianatittler/Grafana-Hybrid-Automation-API-and-Web-With-AI.git](https://github.com/elianatittler/Grafana-Hybrid-Automation-API-and-Web-With-AI.git)
   cd Grafana-Hybrid-Automation-API-and-Web-With-AI

2. Set up the virtual environment & install dependencies:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

3. Install Playwright Browsers:
   playwright install

4. Run the test suite:
   pytest -s -v

5. Directory Structure:
   Grafana-Hybrid-Automation-API-and-Web-With-AI/
   ├── config.json               # Native environment keys (Excluded via .gitignore)
   ├── config.example.json       # Structural boilerplate blueprint for configuration
   ├── conftest.py               # Root automation runner configuration & AI interceptor hooks
   ├── utils/
   │   ├── common_ops.py         # Global ecosystem dynamic loaders
   │   └── fixture_helpers.py    # Request Context factories
   ├── data/
   │   └── login_data.csv        # Dynamic datasets for Data-Driven Testing (DDT)
   └── tests/
       ├── api/                  # Direct Grafana Service Account backend tests
       └── web/                  # Browser testing suites with integrated ai_handler.py
