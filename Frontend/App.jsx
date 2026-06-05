import React, { useState, useEffect, useCallback, useRef } from 'react';
import Header from './components/Header.jsx';
import KPICards from './components/KPICards.jsx';
import QueryInput from './components/QueryInput.jsx';
import InsightPanel from './components/InsightPanel.jsx';
import ChartPanel from './components/ChartPanel.jsx';
import DataTable from './components/DataTable.jsx';
import Sidebar from './components/Sidebar.jsx';
import ChatHistory from './components/ChatHistory.jsx';
import {
  analyzeQuery, fetchKPIs, fetchHealth,
  fetchCategories, fetchRegions, fetchChannels, fetchCampaigns,
} from './services/api.js';

// ── Loading overlay for analyze ───────────────────────────────
function AnalyzeLoader({ query }) {
  const steps = [
    'Detecting intent…',
    'Running Pandas analysis…',
    'Computing confidence…',
    'Generating base insight…',
    'Calling Groq LLM…',
  ];
  const [step, setStep] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setStep(s => Math.min(s + 1, steps.length - 1)), 600);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="animate-fade-in" style={{
      background: 'var(--bg-card)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-xl)',
      padding: '32px',
      display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16,
    }}>
      <div style={{
        width: 40, height: 40,
        border: '2px solid var(--border)',
        borderTopColor: 'var(--cyan)',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite',
        boxShadow: '0 0 16px var(--cyan-glow)',
      }} />
      <div style={{ textAlign: 'center' }}>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.7rem',
          color: 'var(--cyan)',
          letterSpacing: '0.1em',
          marginBottom: 6,
        }}>
          ANALYZING QUERY
        </div>
        <div style={{
          fontSize: '0.85rem',
          color: 'var(--text-secondary)',
          fontStyle: 'italic',
          maxWidth: 320,
        }}>
          "{query}"
        </div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 4, width: '100%', maxWidth: 280 }}>
        {steps.map((s, i) => (
          <div key={i} style={{
            display: 'flex', alignItems: 'center', gap: 8,
            opacity: i <= step ? 1 : 0.25,
            transition: 'opacity 0.3s',
          }}>
            <span style={{
              width: 6, height: 6, borderRadius: '50%',
              background: i < step ? 'var(--green)' : i === step ? 'var(--cyan)' : 'var(--text-dim)',
              flexShrink: 0,
              boxShadow: i === step ? '0 0 8px var(--cyan)' : 'none',
              animation: i === step ? 'pulse-dot 1s infinite' : 'none',
            }} />
            <span style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.65rem',
              color: i === step ? 'var(--text-primary)' : 'var(--text-dim)',
            }}>
              {s}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Error banner ───────────────────────────────────────────────
function ErrorBanner({ message, onClose }) {
  return (
    <div className="animate-fade-up" style={{
      background: 'rgba(239,68,68,0.08)',
      border: '1px solid rgba(239,68,68,0.3)',
      borderRadius: 'var(--radius-lg)',
      padding: '12px 16px',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      gap: 12,
    }}>
      <span style={{ fontSize: '0.85rem', color: '#fca5a5' }}>
        {message}
      </span>
      <button onClick={onClose} style={{
        background: 'none', border: 'none', cursor: 'pointer',
        color: '#fca5a5', fontSize: '1rem', lineHeight: 1,
      }}>
        ×
      </button>
    </div>
  );
}

// ── Empty state ────────────────────────────────────────────────
function EmptyState() {
  return (
    <div style={{
      textAlign: 'center', padding: '60px 20px',
      border: '1px dashed var(--border)',
      borderRadius: 'var(--radius-xl)',
      background: 'rgba(0,212,255,0.01)',
    }}>
      <div style={{
        fontSize: '2.5rem', marginBottom: 12,
        filter: 'grayscale(0.4)',
      }}>
        📊
      </div>
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: '0.7rem',
        color: 'var(--text-dim)',
        letterSpacing: '0.12em',
        marginBottom: 8,
      }}>
        NO QUERY YET
      </div>
      <p style={{
        fontSize: '0.85rem',
        color: 'var(--text-secondary)',
        maxWidth: 360,
        margin: '0 auto',
        lineHeight: 1.6,
      }}>
        Type a business question above or pick one of the quick-query suggestions.
        The AI will analyze your dataset and return charts, tables, and explanations.
      </p>
    </div>
  );
}

// ── App ────────────────────────────────────────────────────────
export default function App() {
  const [health, setHealth]       = useState(null);
  const [kpis, setKpis]           = useState([]);
  const [kpisLoading, setKpisLoading] = useState(true);
  const [meta, setMeta]           = useState(null);
  const [metaLoading, setMetaLoading] = useState(true);

  const [result, setResult]       = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [activeQuery, setActiveQuery] = useState('');
  const [error, setError]         = useState(null);
  const [history, setHistory]     = useState([]);

  const resultsRef = useRef(null);

  // ── Startup data fetches ─────────────────────────────────────
  useEffect(() => {
    fetchHealth().then(setHealth).catch(() => setHealth({ dataset_loaded: false }));

    setKpisLoading(true);
    fetchKPIs()
      .then(d => setKpis(d.kpis))
      .catch(() => {})
      .finally(() => setKpisLoading(false));

    setMetaLoading(true);
    Promise.all([
      fetchCategories().catch(() => []),
      fetchRegions().catch(() => []),
      fetchChannels().catch(() => []),
      fetchCampaigns().catch(() => []),
    ]).then(([categories, regions, channels, campaigns]) => {
      setMeta({ categories, regions, channels, campaigns });
    }).finally(() => setMetaLoading(false));
  }, []);

  // ── Handle query submit ───────────────────────────────────────
  const handleQuery = useCallback(async (query) => {
    setAnalyzing(true);
    setActiveQuery(query);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeQuery(query);
      setResult(data);
      setHistory(h => [...h.slice(-9), {
        query,
        intent: data.intent,
        confidence: data.confidence,
      }]);
      // Scroll to results
      setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
    } catch (err) {
      const msg = err?.response?.data?.message
        || err?.response?.data?.detail
        || err?.message
        || 'Failed to reach the backend. Is it running on port 8000?';
      setError(msg);
    } finally {
      setAnalyzing(false);
    }
  }, []);

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header health={health} />

      <main style={{
        flex: 1,
        maxWidth: 1400,
        width: '100%',
        margin: '0 auto',
        padding: '24px 24px 60px',
        display: 'flex',
        gap: 20,
      }}>
        {/* ── Left column / sidebar ─────────────────────── */}
        <Sidebar meta={meta} loading={metaLoading} />

        {/* ── Main content ──────────────────────────────── */}
        <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', gap: 20 }}>

          {/* KPI row */}
          <section>
            <div style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.6rem',
              color: 'var(--text-dim)',
              letterSpacing: '0.12em',
              marginBottom: 10,
            }}>
              OVERVIEW KPIs
            </div>
            <KPICards kpis={kpis} loading={kpisLoading} />
          </section>

          {/* Query input */}
          <section>
            <div style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.6rem',
              color: 'var(--text-dim)',
              letterSpacing: '0.12em',
              marginBottom: 10,
            }}>
              NATURAL LANGUAGE QUERY
            </div>
            <QueryInput onSubmit={handleQuery} loading={analyzing} />
          </section>

          {/* Error */}
          {error && (
            <ErrorBanner message={error} onClose={() => setError(null)} />
          )}

          {/* Results area */}
          <div ref={resultsRef}>
            {analyzing && <AnalyzeLoader query={activeQuery} />}

            {!analyzing && !result && !error && <EmptyState />}

            {!analyzing && result && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                <InsightPanel result={result} />
                <ChartPanel charts={result.charts} />
                <DataTable tableData={result.table_data} />
              </div>
            )}
          </div>

          {/* History */}
          {history.length > 0 && !analyzing && (
            <ChatHistory history={history} onSelect={handleQuery} />
          )}
        </div>
      </main>
    </div>
  );
}
