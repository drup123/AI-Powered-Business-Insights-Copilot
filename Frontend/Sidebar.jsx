import React from 'react';
import { Database, Layers, Map, Radio, Target } from 'lucide-react';

function Section({ icon: Icon, label, items, loading }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <div style={{
        display: 'flex', alignItems: 'center', gap: 6,
        marginBottom: 8,
      }}>
        <Icon size={11} color="var(--text-dim)" />
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.6rem',
          color: 'var(--text-dim)',
          letterSpacing: '0.1em',
        }}>
          {label}
        </span>
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
        {loading
          ? Array(4).fill(0).map((_, i) => (
              <div key={i} style={{
                height: 22, width: 60 + i * 10,
                background: 'var(--bg-card)',
                borderRadius: 'var(--radius-sm)',
                animation: 'shimmer 1.5s infinite',
                backgroundSize: '200% 100%',
                backgroundImage: 'linear-gradient(90deg, var(--bg-card) 25%, var(--bg-card-hover) 50%, var(--bg-card) 75%)',
              }} />
            ))
          : (items || []).map(item => (
              <span key={item} style={{
                padding: '2px 8px',
                background: 'var(--bg-input)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.72rem',
                color: 'var(--text-secondary)',
                fontFamily: 'var(--font-mono)',
              }}>
                {item}
              </span>
            ))
        }
      </div>
    </div>
  );
}

export default function Sidebar({ meta, loading }) {
  return (
    <aside style={{
      width: 220,
      flexShrink: 0,
      display: 'flex',
      flexDirection: 'column',
      gap: 0,
    }}>
      {/* Dataset info card */}
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-xl)',
        padding: '16px',
        marginBottom: 12,
      }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 6,
          marginBottom: 12,
          paddingBottom: 12,
          borderBottom: '1px solid var(--border)',
        }}>
          <Database size={12} color="var(--cyan)" />
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            color: 'var(--cyan)',
            letterSpacing: '0.1em',
          }}>
            DATASET
          </span>
        </div>
        <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', lineHeight: 1.8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
            <span style={{ color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', fontSize: '0.65rem' }}>FILE</span>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem' }}>business.csv</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', fontSize: '0.65rem' }}>COLUMNS</span>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--green)' }}>9</span>
          </div>
        </div>
      </div>

      {/* Metadata sections */}
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-xl)',
        padding: '16px',
        flex: 1,
      }}>
        <Section icon={Layers}   label="CATEGORIES" items={meta?.categories} loading={loading} />
        <Section icon={Map}      label="REGIONS"    items={meta?.regions}    loading={loading} />
        <Section icon={Radio}    label="CHANNELS"   items={meta?.channels}   loading={loading} />
        <Section icon={Target}   label="CAMPAIGNS"  items={meta?.campaigns}  loading={loading} />
      </div>

      {/* Footer hint */}
      <div style={{
        marginTop: 12,
        padding: '10px',
        textAlign: 'center',
      }}>
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.6rem',
          color: 'var(--text-dim)',
          letterSpacing: '0.06em',
        }}>
          PRESS ⏎ TO ANALYZE
        </span>
      </div>
    </aside>
  );
}
