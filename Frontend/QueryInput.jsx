import React, { useState, useRef } from 'react';
import { Send, Sparkles, ChevronRight } from 'lucide-react';

const SUGGESTIONS = [
  'Which marketing channel gives the highest ROI?',
  'Which product category has the best sales?',
  'How does marketing spend affect monthly sales?',
  'Show me ROI analysis by category',
  'Which region performs best in sales?',
  'Compare campaign types by ROI',
  'Give me a general business overview',
];

export default function QueryInput({ onSubmit, loading }) {
  const [query, setQuery] = useState('');
  const [focused, setFocused] = useState(false);
  const textareaRef = useRef(null);

  const handleSubmit = () => {
    const q = query.trim();
    if (!q || loading) return;
    onSubmit(q);
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const pickSuggestion = (s) => {
    setQuery(s);
    textareaRef.current?.focus();
  };

  return (
    <div>
      {/* Input box */}
      <div style={{
        background: 'var(--bg-card)',
        border: `1px solid ${focused ? 'var(--cyan)' : 'var(--border)'}`,
        borderRadius: 'var(--radius-xl)',
        padding: '4px 4px 4px 20px',
        display: 'flex',
        alignItems: 'flex-end',
        gap: 8,
        transition: 'border-color 0.2s, box-shadow 0.2s',
        boxShadow: focused ? 'var(--shadow-glow)' : 'none',
      }}>
        <div style={{ flex: 1, paddingBottom: 4, paddingTop: 4 }}>
          <div style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.65rem',
            color: 'var(--cyan)',
            letterSpacing: '0.1em',
            marginBottom: 4,
          }}>
            ❯ QUERY
          </div>
          <textarea
            ref={textareaRef}
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={handleKey}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            placeholder="Ask anything about your business data…"
            rows={2}
            style={{
              width: '100%',
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: 'var(--text-primary)',
              fontFamily: 'var(--font-sans)',
              fontSize: '1rem',
              fontWeight: 400,
              resize: 'none',
              lineHeight: 1.5,
              '::placeholder': { color: 'var(--text-dim)' },
            }}
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={!query.trim() || loading}
          style={{
            width: 44, height: 44,
            borderRadius: 'var(--radius-lg)',
            background: query.trim() && !loading
              ? 'linear-gradient(135deg, var(--cyan) 0%, #0096b8 100%)'
              : 'var(--bg-input)',
            border: 'none',
            cursor: query.trim() && !loading ? 'pointer' : 'not-allowed',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0,
            marginBottom: 4,
            transition: 'all 0.2s',
            boxShadow: query.trim() && !loading ? '0 0 16px var(--cyan-glow)' : 'none',
          }}
        >
          {loading
            ? <div style={{
                width: 16, height: 16,
                border: '2px solid rgba(255,255,255,0.3)',
                borderTopColor: '#fff',
                borderRadius: '50%',
                animation: 'spin 0.7s linear infinite',
              }} />
            : <Send size={16} color={query.trim() ? '#000' : 'var(--text-dim)'} strokeWidth={2.5} />
          }
        </button>
      </div>

      {/* Suggestions */}
      <div style={{ marginTop: 12, display: 'flex', flexWrap: 'wrap', gap: 6 }}>
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.6rem',
          color: 'var(--text-dim)',
          letterSpacing: '0.08em',
          alignSelf: 'center',
          marginRight: 4,
        }}>
          QUICK QUERIES:
        </span>
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => pickSuggestion(s)}
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              borderRadius: 20,
              padding: '4px 12px',
              color: 'var(--text-secondary)',
              fontFamily: 'var(--font-sans)',
              fontSize: '0.75rem',
              cursor: 'pointer',
              transition: 'all 0.15s',
              display: 'flex', alignItems: 'center', gap: 4,
            }}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = 'var(--cyan-dim)';
              e.currentTarget.style.color = 'var(--cyan)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = 'var(--border)';
              e.currentTarget.style.color = 'var(--text-secondary)';
            }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
