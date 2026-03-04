import axios from "axios";

const api = axios.create({
  // In dev: VITE_API_URL is empty → requests go to /api → Vite proxies to localhost:8000
  // In production: VITE_API_URL is the full Render URL
  baseURL: import.meta.env.VITE_API_URL || "/api",
  timeout: 120000, // 2 min — accounts for Render cold starts
});

export default api;
