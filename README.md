# 🚗 VehicleConnect Cloud Platform

Cloud-based DevOps platform that simulates **connected vehicle backend services** and provides **real-time operational, security, and delivery KPIs** via an interactive dashboard.

Built as a one-week, end-to-end project to demonstrate **cloud, DevOps, monitoring, and analytics** skills.

---

## 🌐 Live Components

- API status: `http://63.178.201.188:8000/api/status`
- Dashboard: `http://63.178.201.188:8000/dashboard/`
- API docs (Swagger): `http://63.178.201.188:8000/docs`
- Prometheus: `http://63.178.201.188:9090` (restricted to my IP)

_(Replace `63.178.201.188` with your actual IP when sharing.)_

---

## 🧱 Architecture Overview

**High-level flow:**

1. Vehicle simulator sends realistic API requests (status, location, diagnostics, etc.)
2. FastAPI backend receives requests, stores events in PostgreSQL, exposes Prometheus metrics
3. Analytics engine (pandas/numpy) calculates KPIs (latency, error rate, availability, security signals)
4. Dashboard (HTML + Chart.js) visualizes KPIs for operations and management
5. Everything runs in Docker on **AWS EC2**, with deployments automated by **GitHub Actions**

---

## 🛠 Tech Stack

**Backend:**

- Python 3.11, FastAPI
- SQLAlchemy ORM
- PostgreSQL (Docker container)

**Analytics:**

- pandas, numpy
- Custom KPI calculator

**Frontend:**

- HTML5, CSS3
- Vanilla JavaScript
- Chart.js for charts

**DevOps / Cloud:**

- Docker & Docker Compose
- AWS EC2 (Ubuntu 22.04, free tier)
- Prometheus for metrics
- GitHub Actions for CI/CD over SSH

---

## 📊 KPIs Tracked

**Operational KPIs:**

- Average latency
- P95 / P99 latency
- Error rate %
- Availability %
- Requests per minute
- Total requests

**Security KPIs:**

- Failed authentication attempts (4xx codes)
- Potential rate-limit violations
- “Suspicious clients” (high error counts)

**Delivery KPIs (simulated):**

- Deployments per week
- Deployment frequency per day
- MTTR (Mean Time To Recovery)
- Change failure rate %

Full definitions in [`docs/kpi-definition.md`](docs/kpi-definition.md).

---

## 🏗 Project Structure

````text
vehicleconnect-cloud-platform/
├── backend/              # FastAPI backend + tests + Dockerfile
├── analytics/            # KPI calculator (pandas/numpy)
├── dashboard/            # HTML/CSS/JS dashboard (Chart.js)
├── docker/               # Prometheus configuration
├── docs/                 # Architecture, KPIs, deployment, interview notes
├── .github/workflows/    # GitHub Actions CI/CD for EC2 deployment
├── docker-compose.yml    # Multi-container stack: backend + DB + Prometheus
└── README.md


**[Agile Backlog](docs/agile-backlog.md)** - 7 Day Sprint ✅

## 🚀 Quick Start (Local)
```bash
git clone https://github.com/dketas/vehicleconnect-cloud-platform

cd vehicleconnect-cloud-platform
docker compose up -d
cd backend && python app/simulator.py  # 2min traffic

Dashboard: http://localhost:8000/dashboard/



````
