import { useState, useEffect, Component } from "react";
import SearchBar from "./components/SearchBar";
import ReportView from "./components/ReportView";
import ChatInterface from "./components/ChatInterface";
import api from "./api";

// ── Error Boundary ─────────────────────────────────────────────────────────────

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) { return { hasError: true, error }; }
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl p-8 max-w-md w-full text-center">
            <h2 className="text-xl font-bold text-slate-800 mb-2">Something went wrong</h2>
            <p className="text-sm text-slate-500 mb-6">{this.state.error?.message}</p>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm
                font-medium transition-all duration-200 hover:scale-105 active:scale-100"
            >
              Try Again
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

// ── Loading screen ─────────────────────────────────────────────────────────────

const STAGES = [
  "Searching news articles...",
  "Searching company culture...",
  "Searching tech stack...",
  "Searching interview data...",
  "Searching financials...",
  "Generating report...",
];
const ESTIMATED_SECONDS = 60;
const STAGE_INTERVAL_MS = 8000;

function SkeletonBlock({ lines = 2 }) {
  return (
    <div className="bg-white/10 rounded-xl p-4 lg:p-5">
      <div className="h-2.5 bg-white/40 rounded w-28 mb-4 animate-pulse" />
      <div className="space-y-2.5">
        {Array.from({ length: lines }).map((_, i) => (
          <div key={i} className="h-2 bg-white/25 rounded animate-pulse"
            style={{ width: i === lines - 1 ? "60%" : "100%" }} />
        ))}
      </div>
    </div>
  );
}

function ReportSkeleton() {
  return (
    <div className="flex flex-col gap-3">
      <SkeletonBlock lines={4} />
      <SkeletonBlock lines={2} />
      <div className="grid grid-cols-2 gap-3">
        <SkeletonBlock lines={3} />
        <SkeletonBlock lines={3} />
      </div>
      <SkeletonBlock lines={3} />
      <div className="grid grid-cols-2 gap-3">
        <SkeletonBlock lines={2} />
        <SkeletonBlock lines={3} />
      </div>
      <SkeletonBlock lines={4} />
      <div className="grid grid-cols-2 gap-3">
        <SkeletonBlock lines={2} />
        <SkeletonBlock lines={3} />
      </div>
    </div>
  );
}

function LoadingScreen({ companyName }) {
  const [stageIndex, setStageIndex] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const stageTimer = setInterval(() => setStageIndex((i) => Math.min(i + 1, STAGES.length - 1)), STAGE_INTERVAL_MS);
    const elapsedTimer = setInterval(() => setElapsed((s) => s + 1), 1000);
    return () => { clearInterval(stageTimer); clearInterval(elapsedTimer); };
  }, []);

  const remaining = Math.max(0, ESTIMATED_SECONDS - elapsed);
  const countdownLabel = remaining <= 5 ? "Almost there\u2026" : `~${remaining}s remaining`;
  const progress = Math.round((stageIndex / (STAGES.length - 1)) * 100);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500
                    flex flex-col items-center py-12 px-4 overflow-y-auto
                    md:flex-row md:h-screen md:overflow-hidden md:p-0 md:items-stretch">

      {/* ── Spinner panel ── */}
      <div className="w-full max-w-sm bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl
                      p-8 text-center shadow-2xl
                      md:max-w-none md:w-[42%] lg:w-[38%] xl:w-[34%]
                      md:h-full md:rounded-none md:flex md:flex-col md:justify-center
                      md:text-left md:border-0 md:border-r md:border-white/20
                      md:px-10 lg:px-14 xl:px-20">

        <div className="w-14 h-14 lg:w-16 lg:h-16 rounded-full border-4 border-white/20
                        border-t-blue-300 animate-spin mx-auto md:mx-0" />

        <h2 className="text-xl lg:text-2xl font-bold text-white mt-5 mb-1">
          Researching {companyName}
        </h2>
        <p className="text-white/60 text-xs mb-5">{countdownLabel}</p>

        {/* Stage steps — visible on md+ */}
        <div className="hidden md:flex flex-col gap-2 mb-5">
          {STAGES.map((stage, i) => (
            <div key={i} className="flex items-center gap-2.5">
              <div className={`w-1.5 h-1.5 rounded-full shrink-0 transition-all duration-500
                ${i < stageIndex ? "bg-blue-300" : i === stageIndex ? "bg-white animate-pulse" : "bg-white/20"}`} />
              <span className={`text-xs transition-colors duration-300
                ${i < stageIndex ? "text-blue-300/70 line-through" : i === stageIndex ? "text-white font-medium" : "text-white/30"}`}>
                {stage}
              </span>
            </div>
          ))}
        </div>

        {/* Mobile stage label */}
        <p className="text-blue-200 text-sm font-medium mb-4 min-h-[1.25rem] md:hidden">
          {STAGES[stageIndex]}
        </p>

        {/* Progress bar */}
        <div className="h-1.5 bg-white/20 rounded-full overflow-hidden">
          <div className="h-full bg-blue-300 rounded-full transition-all duration-1000"
            style={{ width: `${progress}%` }} />
        </div>
        <div className="flex justify-between text-xs text-white/40 mt-1.5">
          <span>Starting</span><span>Done</span>
        </div>
      </div>

      {/* ── Skeleton preview panel ── */}
      <div className="w-full max-w-3xl mt-8 opacity-30 pointer-events-none select-none
                      md:flex-1 md:max-w-none md:mt-0 md:overflow-y-auto
                      md:px-8 md:py-10 lg:px-12 lg:py-12">
        <p className="text-center text-white/60 text-xs uppercase tracking-widest mb-4">
          Report preview
        </p>
        <ReportSkeleton />
      </div>
    </div>
  );
}

// ── App ────────────────────────────────────────────────────────────────────────

function App() {
  const [view, setView] = useState("search");
  const [companyName, setCompanyName] = useState("");
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState("");

  async function handleSearch(name) {
    setCompanyName(name);
    setError("");
    setView("loading");
    try {
      const { data } = await api.post("/generate-report", { company_name: name });
      setReportData(data.report);
      setView("report");
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        (err.code === "ECONNABORTED"
          ? "Request timed out. The server may be starting up — please try again in a moment."
          : err.message || "An unexpected error occurred.");
      setError(msg);
      setView("search");
    }
  }

  function handleNewSearch() {
    setView("search"); setReportData(null); setCompanyName(""); setError("");
  }

  return (
    <ErrorBoundary>
      {view === "search" && (
        <SearchBar onSearch={handleSearch} loading={false} apiError={error} />
      )}

      {view === "loading" && <LoadingScreen companyName={companyName} />}

      {view === "report" && reportData && (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900
                        lg:h-screen lg:overflow-hidden lg:flex">

          {/* Left — scrollable report */}
          <div className="lg:flex-1 lg:overflow-y-auto">
            <ReportView report={reportData} onNewSearch={handleNewSearch} />
          </div>

          {/* Right — chat panel: fluid width, 28–32% of viewport */}
          <div className="border-t border-white/10 px-4 pb-12
                          lg:p-0 lg:border-t-0 lg:border-l lg:border-white/10
                          lg:w-[30%] lg:min-w-[300px] lg:max-w-[460px]
                          lg:h-full lg:flex lg:flex-col lg:overflow-hidden">
            <ChatInterface companyName={companyName} />
          </div>

        </div>
      )}
    </ErrorBoundary>
  );
}

export default App;
