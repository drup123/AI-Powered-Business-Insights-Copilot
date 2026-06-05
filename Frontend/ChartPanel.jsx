import React, { useMemo } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ScatterChart, Scatter, ResponsiveContainer, Cell,
  Legend, ZAxis, ReferenceLine,
} from 'recharts';

const PALETTE = ['#00d4ff','#10b981','#f59e0b','#8b5cf6','#f472b6','#34d399','#fb923c'];

const DARK_TOOLTIP = {
  contentStyle: {
    background: '#0c1525',
    border: '1px solid #1a2740',
    borderRadius: 6,
    fontFamily: "'Space Mono', monospace",
    fontSize: '0.7rem',
    color: '#e2e8f0',
  },
  labelStyle: { color: '#7a92b0', marginBottom: 4 },
  itemStyle:  { color: '#00d4ff' },
  cursor:     { fill: 'rgba(0,212,255,0.05)' },
};

// ── Custom Axis Tick ──────────────────────────────────────────
function MonoTick({ x, y, payload }) {
  const v = payload.value;
  const display = typeof v === 'number'
    ? v >= 1000 ? `${(v/1000).toFixed(1)}k` : v.toFixed(v < 1 ? 4 : 1)
    : v;
  return (
    <text x={x} y={y} dy={12} textAnchor="middle"
      fill="#3d5475" fontSize={9} fontFamily="Space Mono, monospace">
      {display}
    </text>
  );
}
function MonoTickY({ x, y, payload }) {
  const v = payload.value;
  const display = typeof v === 'number'
    ? v >= 1000 ? `$${(v/1000).toFixed(0)}k` : v.toFixed(v < 1 ? 3 : 0)
    : v;
  return (
    <text x={x} y={y} dy={4} textAnchor="end"
      fill="#3d5475" fontSize={9} fontFamily="Space Mono, monospace">
      {display}
    </text>
  );
}

// ── Bar Chart ─────────────────────────────────────────────────
function PrimaryBarChart({ chartData }) {
  const data = chartData.x.map((label, i) => ({
    name: label,
    value: chartData.y[i],
  }));

  const maxVal = Math.max(...data.map(d => d.value));

  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} margin={{ top: 10, right: 10, left: 10, bottom: 40 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1a2740" vertical={false} />
        <XAxis dataKey="name" tick={MonoTick} axisLine={false} tickLine={false} interval={0} />
        <YAxis tick={MonoTickY} axisLine={false} tickLine={false} width={60} />
        <Tooltip {...DARK_TOOLTIP} formatter={(v) => [
          typeof v === 'number'
            ? v >= 1000 ? `$${v.toLocaleString(undefined, {maximumFractionDigits:0})}`
              : v.toFixed(4)
            : v,
          chartData.y_label || 'Value'
        ]} />
        <Bar dataKey="value" radius={[4, 4, 0, 0]} maxBarSize={60}>
          {data.map((_, i) => (
            <Cell key={i} fill={PALETTE[i % PALETTE.length]}
              fillOpacity={0.85} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

// ── Scatter Chart ─────────────────────────────────────────────
function SecondaryScatterChart({ chartData }) {
  // Group by color (Category / Region)
  const colorValues = chartData.color || [];
  const uniqueGroups = [...new Set(colorValues)];

  const grouped = uniqueGroups.map((group, gi) => ({
    name: group,
    color: PALETTE[gi % PALETTE.length],
    points: chartData.x
      .map((x, i) => ({
        x,
        y: chartData.y[i],
        roi: chartData.extra?.roi?.[i],
      }))
      .filter((_, i) => colorValues[i] === group),
  }));

  return (
    <ResponsiveContainer width="100%" height={260}>
      <ScatterChart margin={{ top: 10, right: 10, left: 10, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1a2740" />
        <XAxis
          type="number" dataKey="x" name="Marketing Spend"
          tick={MonoTick} axisLine={false} tickLine={false}
          label={{ value: 'Marketing Spend', position: 'insideBottom', offset: -10,
            fill: '#3d5475', fontSize: 9, fontFamily: 'Space Mono' }}
        />
        <YAxis
          type="number" dataKey="y" name="Monthly Sales"
          tick={MonoTickY} axisLine={false} tickLine={false} width={60}
        />
        <ZAxis range={[20, 60]} />
        <Tooltip
          {...DARK_TOOLTIP}
          content={({ payload }) => {
            if (!payload?.length) return null;
            const d = payload[0].payload;
            return (
              <div style={{ ...DARK_TOOLTIP.contentStyle }}>
                <div style={{ color: '#7a92b0', marginBottom: 4, fontSize: '0.65rem' }}>
                  {payload[0].name}
                </div>
                <div>Spend: <b style={{ color: '#00d4ff' }}>${d.x?.toLocaleString()}</b></div>
                <div>Sales: <b style={{ color: '#10b981' }}>${d.y?.toLocaleString()}</b></div>
                {d.roi !== undefined && <div>ROI: <b style={{ color: '#f59e0b' }}>{d.roi?.toFixed(4)}</b></div>}
              </div>
            );
          }}
        />
        <Legend
          wrapperStyle={{
            fontFamily: 'Space Mono, monospace',
            fontSize: '0.65rem',
            color: '#7a92b0',
          }}
        />
        {grouped.map(g => (
          <Scatter key={g.name} name={g.name} data={g.points} fill={g.color} fillOpacity={0.7} />
        ))}
      </ScatterChart>
    </ResponsiveContainer>
  );
}

// ── Main ChartPanel ───────────────────────────────────────────
export default function ChartPanel({ charts }) {
  if (!charts) return null;
  const { primary, secondary } = charts;

  const isEmpty = (c) => !c?.x?.length;

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 12,
    }}>
      {/* Primary */}
      <div className="animate-fade-up delay-2" style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-xl)',
        padding: '16px 12px 8px',
        minWidth: 0,
      }}>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.65rem',
          color: 'var(--text-dim)',
          letterSpacing: '0.08em',
          marginBottom: 16,
          paddingLeft: 8,
        }}>
          {primary.title?.replace(/^[^\w]*/, '')}
        </div>
        {isEmpty(primary)
          ? <EmptyChart />
          : <PrimaryBarChart chartData={primary} />
        }
      </div>

      {/* Secondary */}
      <div className="animate-fade-up delay-3" style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-xl)',
        padding: '16px 12px 8px',
        minWidth: 0,
      }}>
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.65rem',
          color: 'var(--text-dim)',
          letterSpacing: '0.08em',
          marginBottom: 16,
          paddingLeft: 8,
        }}>
          {secondary.title?.replace(/^[^\w]*/, '')}
        </div>
        {isEmpty(secondary)
          ? <EmptyChart />
          : <SecondaryScatterChart chartData={secondary} />
        }
      </div>
    </div>
  );
}

function EmptyChart() {
  return (
    <div style={{
      height: 260,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      color: 'var(--text-dim)',
      fontFamily: 'var(--font-mono)',
      fontSize: '0.7rem',
      letterSpacing: '0.1em',
    }}>
      NO CHART DATA
    </div>
  );
}
