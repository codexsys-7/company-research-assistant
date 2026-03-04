import { useState } from "react";

const EXAMPLE_COMPANIES = ["Tesla", "Stripe", "Google", "Airbnb", "OpenAI", "Shopify"];

const HOW_IT_WORKS = [
  { title: "Enter a company name",    desc: "Any company — public, private, startup, or enterprise." },
  { title: "AI searches the web live", desc: "DuckDuckGo scans news, culture, tech, interviews & financials." },
  { title: "Get a structured report",  desc: "11-field briefing: overview, tech stack, culture, financials & more." },
  { title: "Ask follow-up questions",  desc: "RAG-powered chat to dig deeper into any part of the report." },
];

export default function SearchBar({ onSearch, loading: externalLoading, apiError }) {
  const [companyName, setCompanyName] = useState("");
  const [error, setError] = useState("");
  const loading = externalLoading ?? false;

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = companyName.trim();
    if (!trimmed) { setError("Please enter a company name."); return; }
    setError("");
    onSearch(trimmed);
  }

  function handleExample(name) { setCompanyName(name); setError(""); }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900
                    flex items-center justify-center p-6
                    md:p-0 md:h-screen md:overflow-hidden">

      <div className="w-full max-w-lg md:max-w-none md:h-full md:flex">

        {/* ── Left branding panel — md+ ─────────────────────────────────────── */}
        <div className="hidden md:flex flex-col justify-center
                        md:w-[46%] lg:w-[52%] xl:w-[54%]
                        md:px-10 lg:px-16 xl:px-24
                        border-r border-white/10">

          <p className="text-blue-400 text-xs uppercase tracking-widest mb-3">AI Research Tool</p>

          <h1 className="text-3xl lg:text-4xl xl:text-5xl font-bold text-white mb-3 leading-tight tracking-tight">
            Company Research<br className="hidden lg:block" /> Assistant
          </h1>

          <p className="text-slate-300 text-sm lg:text-base xl:text-lg mb-8 leading-relaxed max-w-xs lg:max-w-md">
            Research any company for your next job interview in under 60 seconds —
            powered by live web search and GPT-4o mini.
          </p>

          {/* How it works — only on lg+ where there is enough room */}
          <div className="hidden lg:flex flex-col gap-4 xl:gap-5">
            {HOW_IT_WORKS.map((step, i) => (
              <div key={i} className="flex items-start gap-3 xl:gap-4">
                <div className="w-7 h-7 xl:w-8 xl:h-8 rounded-full bg-blue-600/30 border border-blue-500/40
                                flex items-center justify-center shrink-0 mt-0.5">
                  <span className="text-blue-300 text-xs font-bold">{i + 1}</span>
                </div>
                <div>
                  <p className="text-white text-sm font-semibold">{step.title}</p>
                  <p className="text-slate-400 text-xs xl:text-sm mt-0.5">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>

          <p className="text-white/20 text-xs mt-auto pt-8">Powered by GPT-4o mini + DuckDuckGo</p>
        </div>

        {/* ── Right form panel ──────────────────────────────────────────────── */}
        <div className="md:flex-1 md:flex md:flex-col md:justify-center md:items-center
                        md:px-8 lg:px-12 xl:px-20">

          {/* Mobile-only header */}
          <div className="text-center mb-6 md:hidden">
            <h1 className="text-3xl sm:text-4xl font-bold text-white mb-2 tracking-tight">
              Company Research
            </h1>
            <p className="text-blue-300 text-sm sm:text-base">
              AI-powered interview prep — research any company in seconds
            </p>
          </div>

          <div className="w-full md:max-w-xs lg:max-w-sm xl:max-w-md">

            {/* Desktop form heading */}
            <div className="hidden md:block mb-5">
              <h2 className="text-xl lg:text-2xl font-bold text-white mb-1">Research a Company</h2>
              <p className="text-slate-400 text-sm">Enter a company name to get your interview briefing.</p>
            </div>

            {/* Card */}
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl shadow-xl p-5 lg:p-8">
              {apiError && (
                <div className="mb-4 px-4 py-3 bg-red-500/20 border border-red-400/40 rounded-lg
                                text-sm text-red-300 leading-relaxed">
                  {apiError}
                </div>
              )}

              <form onSubmit={handleSubmit} noValidate>
                <label htmlFor="company-input" className="block text-sm font-medium text-blue-200 mb-2">
                  Company Name
                </label>
                <input
                  id="company-input"
                  type="text"
                  value={companyName}
                  onChange={(e) => { setCompanyName(e.target.value); if (error) setError(""); }}
                  placeholder="e.g. Tesla, Stripe, Google..."
                  disabled={loading}
                  className={`w-full px-4 py-3 rounded-lg bg-white/10 border text-white placeholder-white/40
                    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                    transition-all duration-200 text-sm disabled:opacity-50 disabled:cursor-not-allowed
                    ${error ? "border-red-400" : "border-white/20 hover:border-white/40"}`}
                />
                {error && <p className="mt-2 text-sm text-red-400">{error}</p>}

                <button
                  type="submit"
                  disabled={loading}
                  className="mt-4 w-full py-3 px-6 rounded-lg font-semibold text-white text-sm
                    bg-blue-600 hover:bg-blue-700 hover:scale-105 active:scale-100
                    transition-all duration-200 shadow-lg shadow-blue-900/40
                    disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:scale-100
                    flex items-center justify-center gap-2"
                >
                  {loading ? <><Spinner />Researching...</> : "Research Company"}
                </button>
              </form>

              <div className="mt-5">
                <p className="text-xs text-white/40 mb-2 uppercase tracking-wider">Try an example</p>
                <div className="flex flex-wrap gap-2">
                  {EXAMPLE_COMPANIES.map((name) => (
                    <button
                      key={name} type="button" onClick={() => handleExample(name)} disabled={loading}
                      className="px-3 py-1 rounded-full text-xs font-medium
                        bg-white/10 hover:bg-white/20 text-blue-200 hover:text-white
                        border border-white/10 hover:border-white/30
                        transition-all duration-150 disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                      {name}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <p className="text-center text-white/25 text-xs mt-5">
              Research takes ~30–60 seconds · Powered by GPT-4o mini + DuckDuckGo
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}

function Spinner() {
  return (
    <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 22 6.477 22 12h-4z" />
    </svg>
  );
}
