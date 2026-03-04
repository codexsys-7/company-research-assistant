import { useState, useRef, useEffect } from "react";
import api from "../api";

const EXAMPLE_QUESTIONS = [
  "What's the interview process like?",
  "What technologies do they use?",
  "What are the biggest red flags?",
  "How should I prepare for the interview?",
  "What is the company culture like?",
];

// ── Typing indicator (3 animated dots) ────────────────────────────────────────

function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 px-4 py-3 bg-gray-100 rounded-xl rounded-tl-none max-w-fit">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </div>
  );
}

// ── Send icon ──────────────────────────────────────────────────────────────────

function SendIcon() {
  return (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
    </svg>
  );
}

// ── Main component ─────────────────────────────────────────────────────────────

export default function ChatInterface({ companyName }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: `Hi! I've researched ${companyName}. Ask me anything about the company, their interview process, culture, tech stack, or how to prepare.`,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom whenever messages change or loading changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(question) {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    setInput("");
    setError("");
    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setLoading(true);

    try {
      const { data } = await api.post("/chat", {
        company_name: companyName,
        question: trimmed,
      });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer },
      ]);
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        (err.code === "ECONNABORTED"
          ? "Request timed out. Please try again."
          : "Something went wrong. Please try again.");
      setError(msg);
      // Remove the user message that failed so they can retry
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage(input);
  }

  function handleExample(question) {
    sendMessage(question);
  }

  return (
    <div className="bg-white rounded-xl lg:rounded-none shadow-md overflow-hidden flex flex-col lg:h-full">

      {/* Header */}
      <div className="px-5 py-3 border-b border-slate-100 bg-slate-50">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-blue-600">
          Follow-up Chat
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Ask anything about {companyName}
        </p>
      </div>

      {/* Message list */}
      <div className="h-72 sm:h-96 lg:h-auto lg:flex-1 lg:min-h-0 overflow-y-auto px-4 py-4 flex flex-col gap-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`px-4 py-2.5 text-sm leading-relaxed rounded-xl max-w-[78%] sm:max-w-xs
                ${
                  msg.role === "user"
                    ? "bg-blue-100 text-blue-900 rounded-tr-none ml-auto"
                    : "bg-gray-100 text-slate-800 rounded-tl-none mr-auto"
                }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <TypingIndicator />
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={bottomRef} />
      </div>

      {/* Error banner */}
      {error && (
        <div className="mx-4 mb-2 px-3 py-2 bg-red-50 border border-red-200 rounded-lg text-xs text-red-600">
          {error}
        </div>
      )}

      {/* Example questions */}
      <div className="px-4 pb-2 border-t border-slate-100 pt-3">
        <p className="text-xs text-slate-400 mb-2">Quick questions</p>
        <div className="flex flex-wrap gap-1.5">
          {EXAMPLE_QUESTIONS.map((q) => (
            <button
              key={q}
              type="button"
              onClick={() => handleExample(q)}
              disabled={loading}
              className="px-3 py-1 rounded-full text-xs font-medium
                bg-slate-100 hover:bg-blue-100 text-slate-600 hover:text-blue-700
                border border-slate-200 hover:border-blue-300
                transition-all duration-150 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Input bar */}
      <form onSubmit={handleSubmit} className="px-4 py-3 border-t border-slate-100 flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            if (error) setError("");
          }}
          placeholder="Ask a follow-up question..."
          disabled={loading}
          className="flex-1 px-4 py-2 rounded-lg border border-slate-200 bg-slate-50
            text-sm text-slate-800 placeholder-slate-400
            focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent
            disabled:opacity-50 disabled:cursor-not-allowed
            transition-all duration-150"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white
            disabled:opacity-50 disabled:cursor-not-allowed
            hover:scale-105 active:scale-100
            transition-all duration-150 shadow-sm"
          aria-label="Send message"
        >
          <SendIcon />
        </button>
      </form>
    </div>
  );
}
