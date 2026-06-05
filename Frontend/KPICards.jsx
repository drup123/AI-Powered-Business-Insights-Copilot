import React from 'react';
import { TrendingUp, DollarSign, BarChart2, Target, Star, Zap } from 'lucide-react';

const ICONS = [DollarSign, TrendingUp, Target, DollarSign, Star, Zap];
const COLORS = ['var(--cyan)', 'var(--green)', 'var(--amber)', 'var(--purple)', 'var(--cyan)', 'var(--amber)'];

function Skeleton() {
  return (
    <div style={{
      background: 'linear-gradient(90deg, var(--bg-card) 25%, var(--bg-card-hover) 50%, var(--bg-card) 75%)',
      backgroundSize: '200% 100%',
      animation: 'shimmer 1.5s infinite',
      borderRadius: 'var(--radius-lg)',
      height: 110,
      border: '1px solid var(--border)',
    }} />
  );
}

export default function KPICards({ kpis, loading }) {
  if (loading) {
    return (
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: 12,
      }}>
        {Array(6).fill(0).map((_, i) => <Skeleton key={i} />)}
      </div>
    );
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
      gap: 12,
    }}>
      {(kpis || []).map((kpi, i) => {
        const Icon = ICONS[i] || BarChart2;
        const color = COLORS[i] || 'var(--cyan)';
        const isNumeric = typeof kpi.value === 'number';

        return (
          <div
            key={kpi.label}
            className="animate-fade-up"
            style={{
              '--delay': `${i * 0.05}s`,
              animationDelay: `${i * 0.05}s`,
              background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-lg)',
              padding: '16px 20px',
              position: 'relative',
              overflow: 'hidden',
              cursor: 'default',
              transition: 'border-color 0.2s, transform 0.2s',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = color;
              e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = 'var(--border)';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            {/* Glow accent */}
            <div style={{
              position: 'absolute',
              top: 0, left: 0,
              width: '100%', height: 2,
              background: `linear-gradient(90deg, transparent, ${color}, transparent)`,
              opacity: 0.6,
            }} />

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
              <span style={{
                fontSize: '0.65rem',
                fontFamily: 'var(--font-mono)',
                color: 'var(--text-dim)',
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
              }}>
                {kpi.label}
              </span>
              <div style={{
                width: 28, height: 28,
                borderRadius: 'var(--radius-sm)',
                background: `color-mix(in srgb, ${color} 12%, transparent)`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>
                <Icon size={14} color={color} />
              </div>
            </div>

            <div style={{
              fontFamily: isNumeric ? 'var(--font-mono)' : 'var(--font-sans)',
              fontSize: isNumeric ? '1.35rem' : '1rem',
              fontWeight: isNumeric ? 700 : 600,
              color: 'var(--text-primary)',
              lineHeight: 1.2,
            }}>
              {kpi.unit === '$' && isNumeric
                ? `$${Number(kpi.value).toLocaleString(undefined, { maximumFractionDigits: 0 })}`
                : isNumeric
                  ? Number(kpi.value).toLocaleString(undefined, { maximumFractionDigits: 4 })
                  : kpi.value
              }
            </div>
          </div>
        );
      })}
    </div>
  );
}
