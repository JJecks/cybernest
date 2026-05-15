# 🖥️ CyberNest

A full-stack cyber cafe management system that tracks computer usage across all PCs in real time and displays the data on a centralized dashboard.

Built with Django, Django REST Framework, React, TypeScript, and Tailwind CSS.

---

## 📸 Screenshots

> Dashboard showing live PC activity, app usage charts, browser history and print jobs.

*(Add screenshots here after deployment)*

---

## ✨ Features

- **Real-time app tracking** — records which applications are used and for how long on each PC
- **Browser history sync** — captures visited URLs from Chrome and Edge
- **Print job tracking** — logs every document printed including page count and printer name
- **Live dashboard** — auto-refreshing React dashboard with charts and tables
- **PC management** — server detects which cafe PCs are online or offline in real time
- **Django admin panel** — full data management interface at `/admin/`
- **Packaged installers** — ships as `.exe` files, no Python knowledge needed to deploy

---

## 🏗️ Architecture
cybernest/
├── core/              → Django project settings and URLs
├── tracker/           → Django app: models, views, serializers, URLs
├── frontend/          → React + TypeScript + Tailwind CSS dashboard
├── agent/             → Python tracking agent (runs on each cafe PC)
├── start_server.py    → Server launcher (used for packaging)
└── manage.py
**Two components deploy separately:**

| Component | Runs on | Purpose |
|---|---|---|
| `CyberNest_Server.exe` | Server PC | Django API + React dashboard |
| `CyberNest_Agent.exe` | Each cafe PC | Tracks usage and reports to server |

---

## 🚀 Getting Started (Development)

### Prerequisites
- Python 3.12
- Node.js 24+
- Git

### Backend setup

```bash
git clone https://github.com/JJecks/cybernest.git
cd cybernest

py -3.12 -m venv venv
venv\Scripts\activate

pip install django djangorestframework django-cors-headers whitenoise
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Dashboard runs at **http://localhost:5173**

### Running the agent

```bash
cd ..
python agent/agent.py
```

On first run it will ask for a PC name. This is saved and never asked again.

> ⚠️ Run as Administrator for print tracking to work.

---

## 🖥️ Deployment (Cafe Setup)

### Server PC
1. Copy `dist/CyberNest_Server.exe` to the server PC
2. Copy `dist/staticfiles/` folder next to the exe
3. Double-click to run — opens the dashboard in your browser automatically

### Each Cafe PC
1. Copy `dist/CyberNest_Agent.exe` to the PC
2. Right-click → Run as Administrator
3. Enter the PC name when prompted (e.g. `PC-01`)
4. The agent will register itself with the server and start tracking

### Finding the server IP
Run `ipconfig` on the server PC and note the IPv4 address (e.g. `192.168.1.5`).
Update `SERVER_URL` in `agent/agent.py` before packaging:

```python
SERVER_URL = "http://192.168.1.5:8000/api"
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/machines/all/` | List all registered PCs |
| POST | `/api/machines/` | Register a new PC |
| POST | `/api/machines/<id>/heartbeat/` | PC heartbeat (online status) |
| POST | `/api/logs/app/` | Submit app usage log |
| GET | `/api/logs/app/list/` | Retrieve app usage logs |
| POST | `/api/logs/browser/` | Submit browser visit |
| GET | `/api/logs/browser/list/` | Retrieve browser logs |
| POST | `/api/logs/print/` | Submit print job |
| GET | `/api/logs/print/list/` | Retrieve print logs |

---

## 🛠️ Tech Stack

**Backend**
- Python 3.12
- Django 6.0
- Django REST Framework
- Whitenoise
- SQLite (development) → PostgreSQL (production)

**Frontend**
- React 19 + TypeScript
- Vite
- Tailwind CSS
- Recharts
- Axios

**Agent**
- Python 3.12
- pywin32 (Windows API)
- PowerShell (print event log)
- PyInstaller (packaging)

---

## 🔮 Roadmap

- [ ] Per-session billing (start/end time + cost calculation)
- [ ] PostgreSQL for multi-PC production use
- [ ] Cloudflare Tunnel for remote owner access
- [ ] Per-machine dashboard view
- [ ] Export reports to PDF/Excel

---

## 👤 Author

**JJecks**
GitHub: [@JJecks](https://github.com/JJecks)

---

## 📄 License

MIT
