# Employee Manager

REST API для системи обліку працівників. Проєкт розроблено в рамках курсу «Професійний Python» (Лабораторні роботи №1–10).

## Features
- CRUD для працівників
- Статистика відділів (середня/максимальна зарплата, фонд оплати праці)
- SQLite persistence
- FastAPI + Pydantic
- Docker + CI/CD
- Оптимізації (NumPy, ThreadPool, caching)

## Requirements
- Python 3.11+
- Docker

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"