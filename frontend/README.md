# Company Research Assistant — Frontend

React + Vite frontend for the Company Research Assistant.

## Requirements

- Node.js 18+
- Backend running (see `../backend/`)

## Environment Setup

Copy the example env file and configure as needed:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `VITE_API_URL` | Backend base URL. Leave empty in dev to use the Vite proxy. | `` (empty) |

### Development (local)

Leave `VITE_API_URL` empty. The Vite dev server proxies `/api/*` → `http://localhost:8000`.

```
# .env
VITE_API_URL=
```

### Production (Render)

Set `VITE_API_URL` to your deployed backend URL in `.env.production` (gitignored — set at build time or in CI):

```
# .env.production
VITE_API_URL=https://your-backend.onrender.com
```

## Running

```bash
npm install

# Development (hot reload, proxy to localhost:8000)
npm run dev

# Production build
npm run build        # outputs to dist/
npm run preview      # serves dist/ locally on port 4173
```

## Project Structure

```
src/
├── App.jsx              # Root component — routing between search/report/chat views
├── api.js               # Axios instance + generateReport() / chat() helpers
├── index.css            # Tailwind base styles
└── components/
    ├── SearchBar.jsx    # Company name input + submit
    ├── ReportView.jsx   # Structured report display (11 fields, responsive grid)
    └── ChatInterface.jsx # Follow-up Q&A chat panel
```
