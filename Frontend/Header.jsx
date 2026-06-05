import React from 'react';
import { Activity, Cpu, Wifi, WifiOff } from 'lucide-react';

export default function Header({ health }) {
  const online = health?.dataset_loaded;

  return (
    <header style={{
      borderBottom: '1px solid var(--border)',
      background: 'rgba(8,14,26,0.95)',
      backdropFilter: 'blur(12px)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '0 2rem',
    }}>
      <div style={{
        maxWidth: 1400,
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: 56,
      }}>
        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{
            width: 32, height: 32,
            background: 'linear-gradient(135deg, var(--cyan) 0%, var(--purple) 100%)',
            borderRadius: 'var(--radius-md)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 0 16px var(--cyan-glow)',
          }}>
            <Activity size={16} color="#fff" strokeWidth={2.5} />
          </div>
          <div>
            <span style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.85rem',
              fontWeight: 700,
              color: 'var(--text-primary)',
              letterSpacing: '0.05em',
            }}>
              INSIGHTS<span style={{ color: 'var(--cyan)' }}>_</span>COPILOT
            </span>
            <div style={{
              fontSize: '0.65rem',
              color: 'var(--text-dim)',
              fontFamily: 'var(--font-mono)',
              letterSpacing: '0.08em',
            }}>
              AI-POWERED ANALYTICS
            </div>
          </div>
        </div>

        {/* Status bar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
          {health && (
            <span style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.65rem',
              color: 'var(--text-dim)',
              letterSpacing: '0.05em',
            }}>
              {health.row_count?.toLocaleString()} ROWS
            </span>
          )}

          <div style={{
            display: 'flex', alignItems: 'center', gap: 6,
            padding: '4px 10px',
            border: `1px solid ${online ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)'}`,
            borderRadius: 'var(--radius-sm)',
            background: online ? 'rgba(16,185,129,0.06)' : 'rgba(239,68,68,0.06)',
          }}>
            <span style={{
              width: 6, height: 6,
              borderRadius: '50%',
              background: online ? 'var(--green)' : 'var(--red)',
              display: 'inline-block',
              animation: online ? 'pulse-dot 2s ease infinite' : 'none',
              boxShadow: online ? '0 0 6px var(--green)' : 'none',
            }} />
            <span style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.65rem',
              color: online ? 'var(--green)' : 'var(--red)',
              letterSpacing: '0.08em',
            }}>
              {online ? 'BACKEND ONLINE' : 'OFFLINE'}
            </span>
          </div>

          <div style={{
            display: 'flex', alignItems: 'center', gap: 6,
            color: 'var(--text-dim)',
          }}>
            <Cpu size={14} />
            <span style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.65rem',
              letterSpacing: '0.08em',
            }}>
              GROQ / LLAMA-3.1
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
