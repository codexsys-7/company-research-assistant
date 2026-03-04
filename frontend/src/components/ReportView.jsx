import { useState } from "react";

// ── Icons ──────────────────────────────────────────────────────────────────────

function ChevronDown() {
  return (
    <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
    </svg>
  );
}

function ChevronUp() {
  return (
    <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 15l7-7 7 7" />
    </svg>
  );
}

function WarningIcon() {
  return (
    <svg className="w-4 h-4 text-red-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
    </svg>
  );
}

function ArrowLeftIcon() {
  return (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
    </svg>
  );
}

// ── Section wrapper ────────────────────────────────────────────────────────────

function Section({ title, defaultOpen = true, children, accent = "blue" }) {
  const [open, setOpen] = useState(defaultOpen);

  const accentMap = {
    blue: "text-blue-600",
    red: "text-red-500",
    green: "text-green-600",
    amber: "text-amber-600",
    purple: "text-purple-600",
    teal: "text-teal-600",
  };

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200 overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-4 py-3 sm:px-6 sm:py-4 cursor-pointer text-left
          active:bg-slate-50 transition-colors duration-100"
      >
        <h2 className={`text-xs sm:text-sm font-semibold uppercase tracking-wider ${accentMap[accent] ?? accentMap.blue}`}>
          {title}
        </h2>
        <span className="text-slate-400 ml-2">
          {open ? <ChevronUp /> : <ChevronDown />}
        </span>
      </button>

      {open && (
        <div className="px-4 pb-4 sm:px-6 sm:pb-5 border-t border-slate-100">
          {children}
        </div>
      )}
    </div>
  );
}

// ── Badge (tech stack) ─────────────────────────────────────────────────────────

const BADGE_COLORS = [
  "bg-blue-100 text-blue-700",
  "bg-purple-100 text-purple-700",
  "bg-teal-100 text-teal-700",
  "bg-green-100 text-green-700",
  "bg-amber-100 text-amber-700",
  "bg-pink-100 text-pink-700",
  "bg-indigo-100 text-indigo-700",
  "bg-orange-100 text-orange-700",
];

function Badge({ text, index }) {
  const color = BADGE_COLORS[index % BADGE_COLORS.length];
  return (
    <span className={`inline-block px-2.5 py-0.5 sm:px-3 sm:py-1 rounded-full text-xs font-medium ${color}`}>
      {text}
    </span>
  );
}

// ── Empty state ────────────────────────────────────────────────────────────────

function Empty({ message = "No information available." }) {
  return <p className="text-sm text-slate-400 italic pt-3">{message}</p>;
}

// ── Main component ─────────────────────────────────────────────────────────────

export default function ReportView({ report, onNewSearch }) {
  if (!report) return null;

  const {
    company_name,
    overview,
    products_and_services,
    tech_stack,
    culture_and_values,
    recent_news,
    financials,
    interview_process,
    common_interview_questions,
    red_flags,
    preparation_tips,
  } = report;

  return (
    <div className="py-6 sm:py-10 px-4">
      <div className="max-w-4xl mx-auto">

        {/* Page header */}
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between mb-6 sm:mb-8">
          <div>
            <p className="text-blue-400 text-xs uppercase tracking-widest mb-1">Research Report</p>
            <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">{company_name}</h1>
          </div>
          <button
            type="button"
            onClick={onNewSearch}
            className="self-start sm:self-auto flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium
              bg-white/10 hover:bg-white/20 text-white border border-white/20 hover:border-white/40
              hover:scale-105 active:scale-100 transition-all duration-150"
          >
            <ArrowLeftIcon />
            New Search
          </button>
        </div>

        {/* Sections */}
        <div className="flex flex-col gap-4">

          {/* 1 · Overview — full width */}
          <Section title="Overview" accent="blue">
            <p className="text-sm text-slate-700 leading-relaxed pt-3">
              {overview || <Empty />}
            </p>
          </Section>

          {/* 2 · Products & Services — full width */}
          <Section title="Products & Services" accent="purple">
            <p className="text-sm text-slate-700 leading-relaxed pt-3">
              {products_and_services || <Empty />}
            </p>
          </Section>

          {/* 3 + 4 · Tech Stack + Culture — 2-col on md+ */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Section title="Tech Stack" accent="teal">
              {tech_stack && tech_stack.length > 0 ? (
                <div className="flex flex-wrap gap-2 pt-3">
                  {tech_stack.map((tech, i) => (
                    <Badge key={tech} text={tech} index={i} />
                  ))}
                </div>
              ) : (
                <Empty />
              )}
            </Section>

            <Section title="Culture & Values" accent="green">
              <p className="text-sm text-slate-700 leading-relaxed pt-3">
                {culture_and_values || <Empty />}
              </p>
            </Section>
          </div>

          {/* 5 · Recent News — full width */}
          <Section title="Recent News" accent="amber">
            {recent_news && recent_news.length > 0 ? (
              <ul className="mt-3 space-y-2">
                {recent_news.map((item, i) => (
                  <li key={i} className="flex gap-2 text-sm text-slate-700">
                    <span className="text-amber-500 mt-0.5 shrink-0">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty />
            )}
          </Section>

          {/* 6 + 7 · Financials + Interview Process — 2-col on md+ */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Section title="Financials" accent="green">
              <p className="text-sm text-slate-700 leading-relaxed pt-3">
                {financials || <Empty />}
              </p>
            </Section>

            <Section title="Interview Process" accent="blue">
              <p className="text-sm text-slate-700 leading-relaxed pt-3">
                {interview_process || <Empty />}
              </p>
            </Section>
          </div>

          {/* 8 · Common Interview Questions — full width */}
          <Section title="Common Interview Questions" accent="purple">
            {common_interview_questions && common_interview_questions.length > 0 ? (
              <ol className="mt-3 space-y-2 list-none">
                {common_interview_questions.map((q, i) => (
                  <li key={i} className="flex gap-3 text-sm text-slate-700">
                    <span className="text-purple-500 font-semibold shrink-0 w-5">{i + 1}.</span>
                    <span>{q}</span>
                  </li>
                ))}
              </ol>
            ) : (
              <Empty message="No interview questions found for this company." />
            )}
          </Section>

          {/* 9 + 10 · Red Flags + Preparation Tips — 2-col on md+ */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Section title="Red Flags" accent="red">
              {red_flags && red_flags.length > 0 ? (
                <ul className="mt-3 space-y-2">
                  {red_flags.map((flag, i) => (
                    <li key={i} className="flex gap-2 text-sm text-red-700 bg-red-50 rounded-lg px-3 py-2 border border-red-100">
                      <WarningIcon />
                      <span>{flag}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <Empty message="No red flags identified." />
              )}
            </Section>

            <Section title="Preparation Tips" accent="teal">
              <p className="text-sm text-slate-700 leading-relaxed pt-3">
                {preparation_tips || <Empty />}
              </p>
            </Section>
          </div>

        </div>

        {/* Footer button */}
        <div className="mt-8 flex justify-center">
          <button
            type="button"
            onClick={onNewSearch}
            className="flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-semibold
              bg-blue-600 hover:bg-blue-700 text-white
              hover:scale-105 active:scale-100
              transition-all duration-200 shadow-lg shadow-blue-900/40"
          >
            <ArrowLeftIcon />
            Research Another Company
          </button>
        </div>

        <p className="text-center text-white/25 text-xs mt-6 pb-4">
          Powered by GPT-4o mini + DuckDuckGo
        </p>
      </div>
    </div>
  );
}
