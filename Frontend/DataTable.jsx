import React, { useState } from 'react';
import { Table, ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';

function formatCell(value) {
  if (value === null || value === undefined) return '—';
  if (typeof value === 'number') {
    if (value >= 1000) return `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
    if (value < 1)    return value.toFixed(4);
    return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }
  return String(value);
}

function isNumericCol(rows, col) {
  return rows.some(r => typeof r[col] === 'number');
}

export default function DataTable({ tableData }) {
  const [sortCol, setSortCol] = useState(null);
  const [sortDir, setSortDir] = useState('desc');

  if (!tableData?.length) return null;

  const columns = Object.keys(tableData[0]);

  const sorted = sortCol
    ? [...tableData].sort((a, b) => {
        const av = a[sortCol], bv = b[sortCol];
        if (typeof av === 'number' && typeof bv === 'number') {
          return sortDir === 'asc' ? av - bv : bv - av;
        }
        return sortDir === 'asc'
          ? String(av).localeCompare(String(bv))
          : String(bv).localeCompare(String(av));
      })
    : tableData;

  const handleSort = (col) => {
    if (sortCol === col) setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    else { setSortCol(col); setSortDir('desc'); }
  };

  const maxVals = {};
  columns.forEach(col => {
    if (isNumericCol(tableData, col)) {
      maxVals[col] = Math.max(...tableData.map(r => r[col] ?? -Infinity));
    }
  });

  return (
    <div className="animate-fade-up delay-4" style={{
      background: 'var(--bg-card)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-xl)',
      overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        padding: '12px 20px',
        borderBottom: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', gap: 8,
        background: 'rgba(0,0,0,0.2)',
      }}>
        <Table size={12} color="var(--text-dim)" />
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.6rem',
          color: 'var(--text-dim)',
          letterSpacing: '0.1em',
        }}>
          RESULTS TABLE — {tableData.length} ROWS
        </span>
      </div>

      {/* Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          fontFamily: 'var(--font-mono)',
          fontSize: '0.75rem',
        }}>
          <thead>
            <tr>
              <th style={{
                padding: '8px 20px', width: 36,
                borderBottom: '1px solid var(--border)',
                color: 'var(--text-dim)',
                textAlign: 'left',
                fontWeight: 400,
              }}>
                #
              </th>
              {columns.map(col => (
                <th key={col}
                  onClick={() => handleSort(col)}
                  style={{
                    padding: '8px 16px',
                    borderBottom: '1px solid var(--border)',
                    textAlign: isNumericCol(tableData, col) ? 'right' : 'left',
                    cursor: 'pointer',
                    color: sortCol === col ? 'var(--cyan)' : 'var(--text-dim)',
                    fontWeight: 400,
                    letterSpacing: '0.06em',
                    whiteSpace: 'nowrap',
                    userSelect: 'none',
                    transition: 'color 0.15s',
                  }}
                >
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                    {col.replace(/_/g, ' ')}
                    {sortCol === col
                      ? sortDir === 'asc'
                        ? <ArrowUp size={10} />
                        : <ArrowDown size={10} />
                      : <ArrowUpDown size={10} color="var(--text-dim)" />
                    }
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((row, ri) => (
              <tr key={ri}
                style={{
                  borderBottom: ri < sorted.length - 1 ? '1px solid rgba(26,39,64,0.5)' : 'none',
                  transition: 'background 0.15s',
                }}
                onMouseEnter={e => e.currentTarget.style.background = 'rgba(0,212,255,0.03)'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
              >
                <td style={{
                  padding: '10px 20px',
                  color: 'var(--text-dim)',
                  fontSize: '0.65rem',
                }}>
                  {ri + 1}
                </td>
                {columns.map(col => {
                  const val = row[col];
                  const isNum = typeof val === 'number';
                  const isTop = isNum && maxVals[col] !== undefined && val === maxVals[col];
                  const barPct = isNum && maxVals[col]
                    ? (val / maxVals[col]) * 100
                    : 0;

                  return (
                    <td key={col} style={{
                      padding: '10px 16px',
                      textAlign: isNum ? 'right' : 'left',
                      color: isTop ? 'var(--cyan)' : 'var(--text-secondary)',
                      fontWeight: isTop ? 700 : 400,
                      position: 'relative',
                    }}>
                      {isNum && (
                        <div style={{
                          position: 'absolute',
                          bottom: 0, left: 0,
                          height: 2,
                          width: `${barPct}%`,
                          background: 'linear-gradient(90deg, transparent, var(--cyan-dim))',
                          opacity: 0.4,
                          borderRadius: '0 1px 1px 0',
                        }} />
                      )}
                      {formatCell(val)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
