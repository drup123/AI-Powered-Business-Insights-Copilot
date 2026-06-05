import React from 'react';
import { MessageSquare, Clock } from 'lucide-react';

export default function ChatHistory({ history, onSelect }) {
  if (!history?.length) return null;

  return (
    <div style={{
      background: 'var(--bg-card)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-xl)',
      overflow: 'hidden',
    }}>
      <div style={{
        padding: '10px 16px',
        borderBottom: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', gap: 6,
        background: 'rgba(0,0,0,0.2)',
      }}>
        <Clock size={11} color="var(--text-dim)" />
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.6rem',
          color: 'var(--text-dim)',
          letterSpacing: '0.1em',
        }}>
          QUERY HISTORY
        </span>
      </div>
      <div style={{ padding: '6px' }}>
        {[...history].reverse().map((item, i) => (
          <button
            key={i}
            onClick={() => onSelect(item.query)}
            style={{
              display: 'flex', alignItems: 'center', gap: 8,
              width: '100%', textAlign: 'left',
              padding: '7px 10px',
              background: 'transparent',
              border: 'none',
              borderRadius: 'var(--radius-md)',
              cursor: 'pointer',
              transition: 'background 0.15s',
            }}
            onMouseEnter={e => e.currentTarget.style.background = 'rgba(0,212,255,0.04)'}
            onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
          >
            <MessageSquare size={11} color="var(--text-dim)" style={{ flexShrink: 0 }} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{
                fontSize: '0.75rem',
                color: 'var(--text-secondary)',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}>
                {item.query}
              </div>
              <div style={{
                fontSize: '0.62rem',
                fontFamily: 'var(--font-mono)',
                color: 'var(--text-dim)',
                marginTop: 1,
              }}>
                {item.intent?.replace('_', ' ')} · {item.confidence?.level}
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
