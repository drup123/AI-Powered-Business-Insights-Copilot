import React from 'react';
import { Cpu, BookOpen, AlertTriangle } from 'lucide-react';
import ConfidenceBadge from './ConfidenceBadge';

const INTENT_LABELS = {
  SALES_TREND:      'Sales Trend Analysis',
  MARKETING_IMPACT: 'Marketing Impact Analysis',
  ROI_ANALYSIS:     'ROI Analysis',
  REGION_ANALYSIS:  'Regional Analysis',
  CHANNEL_ANALYSIS: 'Channel Analysis',
  CAMPAIGN_ANALYSIS:'Campaign Analysis',
  GENERAL_INSIGHTS: 'General Business Insights',
  TIME_TREND:       'Time Trend Analysis',
  OUT_OF_SCOPE:     'Out of Scope',
};

// Render markdown-lite **bold** in strings
function BoldText({ text }) {
  if (!text) return null;
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((part, i) =>
        part.startsWith('**') && part.endsWith('**')
          ? <strong key={i} style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
              {part.slice(2, -2)}
            </strong>
          : <span key={i}>{part}</span>
      )}
    </>
  );
}

export default function InsightPanel({ result }) {
  if (!result) return null;
  const { intent, confidence, validation, base_insight, llm_explanation, query } = result;

  return (
    <div className="animate-fade-up" style={{
      background: 'var(--bg-card)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-xl)',
      overflow: 'hidden',
    }}>
      {/* Header strip */}
      <div style={{
        padding: '12px 20px',
        borderBottom: '1px solid var(--border)',
        background: 'rgba(0,212,255,0.03)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            color: 'var(--cyan)',
            letterSpacing: '0.12em',
          }}>
            {INTENT_LABELS[intent] || intent}
          </span>
          <span style={{ color: 'var(--border)', fontSize: '0.7rem' }}>│</span>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            color: 'var(--text-dim)',
            fontStyle: 'italic',
          }}>
            "{query}"
          </span>
        </div>
        <ConfidenceBadge confidence={confidence} />
      </div>

      <div style={{ padding: '20px' }}>
        {/* Validation flags */}
        {validation?.flags?.length > 0 && (
          <div style={{
            marginBottom: 16,
            padding: '10px 14px',
            background: 'rgba(245,158,11,0.07)',
            border: '1px solid rgba(245,158,11,0.25)',
            borderRadius: 'var(--radius-md)',
            display: 'flex', gap: 10,
          }}>
            <AlertTriangle size={14} color="var(--amber)" style={{ flexShrink: 0, marginTop: 2 }} />
            <div>
              {validation.flags.map((f, i) => (
                <p key={i} style={{
                  fontSize: '0.78rem',
                  color: 'var(--amber)',
                  lineHeight: 1.6,
                  marginBottom: i < validation.flags.length - 1 ? 4 : 0,
                }}>
                  {f.replace(/^⚠️\s*/, '')}
                </p>
              ))}
            </div>
          </div>
        )}

        {/* Base insight */}
        <div style={{ marginBottom: 16 }}>
          <div style={{
            display: 'flex', alignItems: 'center', gap: 6,
            marginBottom: 8,
          }}>
            <BookOpen size={12} color="var(--text-dim)" />
            <span style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.6rem',
              color: 'var(--text-dim)',
              letterSpacing: '0.1em',
            }}>
              DATA ANALYSIS
            </span>
          </div>
          <p style={{
            fontSize: '0.92rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.7,
          }}>
            <BoldText text={base_insight} />
          </p>
        </div>

        {/* LLM explanation */}
        {llm_explanation && !validation?.blocked && (
          <div style={{
            paddingTop: 16,
            borderTop: '1px solid var(--border)',
          }}>
            <div style={{
              display: 'flex', alignItems: 'center', gap: 6,
              marginBottom: 8,
            }}>
              <Cpu size={12} color="var(--cyan)" />
              <span style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.6rem',
                color: 'var(--cyan)',
                letterSpacing: '0.1em',
              }}>
                AI EXPLANATION
              </span>
            </div>
            <p style={{
              fontSize: '0.92rem',
              color: 'var(--text-primary)',
              lineHeight: 1.75,
              borderLeft: '2px solid var(--cyan-dim)',
              paddingLeft: 14,
            }}>
              {llm_explanation}
            </p>
          </div>
        )}

        {/* Blocked message */}
        {validation?.blocked && validation?.block_reason && (
          <div style={{
            paddingTop: 16,
            borderTop: '1px solid var(--border)',
            color: 'var(--text-secondary)',
            fontSize: '0.88rem',
            fontStyle: 'italic',
          }}>
            {validation.block_reason}
          </div>
        )}
      </div>
    </div>
  );
}
