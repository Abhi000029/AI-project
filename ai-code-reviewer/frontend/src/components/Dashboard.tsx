import { useEffect, useState } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import { api } from '../api/client'
import type { DashboardData } from '../types'
import { severityDotColor } from './SeverityBadge'

const SEVERITY_ORDER = ['critical', 'high', 'medium', 'low', 'info'] as const

export function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .dashboard()
      .then(setData)
      .catch((err) => setError(err.message))
  }, [])

  if (error) {
    return (
      <div className="rounded-xl border border-severity-critical/30 bg-severity-critical/10 px-5 py-4 text-sm text-severity-critical">
        {error}
      </div>
    )
  }

  if (!data) {
    return <div className="font-mono text-sm text-text-faint">Loading metrics…</div>
  }

  const severityData = SEVERITY_ORDER.map((s) => ({
    name: s,
    value: data.severity_breakdown[s] || 0,
  }))

  const categoryData = Object.entries(data.category_breakdown).map(([name, value]) => ({
    name: name.replace('_', ' '),
    value,
  }))

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <MetricCard label="Total reviews" value={data.metrics.total_reviews} />
        <MetricCard label="Total findings" value={data.metrics.total_findings} />
        <MetricCard
          label="Avg quality score"
          value={data.metrics.avg_quality_score ?? '—'}
        />
        <MetricCard
          label="Avg review time"
          value={
            data.metrics.avg_review_time_ms
              ? `${(data.metrics.avg_review_time_ms / 1000).toFixed(1)}s`
              : '—'
          }
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <ChartCard title="Findings by severity">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={severityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#232B3A" vertical={false} />
              <XAxis
                dataKey="name"
                tick={{ fill: '#8A93A6', fontSize: 11 }}
                axisLine={{ stroke: '#232B3A' }}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: '#8A93A6', fontSize: 11 }}
                axisLine={{ stroke: '#232B3A' }}
                tickLine={false}
                allowDecimals={false}
              />
              <Tooltip
                contentStyle={{
                  background: '#171D29',
                  border: '1px solid #232B3A',
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {severityData.map((entry) => (
                  <Cell key={entry.name} fill={severityDotColor(entry.name as any)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Findings by category">
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={categoryData}
                dataKey="value"
                nameKey="name"
                innerRadius={50}
                outerRadius={80}
                paddingAngle={3}
              >
                {categoryData.map((_, i) => (
                  <Cell key={i} fill={['#6C8EFF', '#FF8B5E', '#FFD166', '#6FCF97', '#7C9CFF'][i % 5]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: '#171D29',
                  border: '1px solid #232B3A',
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="rounded-xl border border-ink-border bg-ink-panel">
        <div className="border-b border-ink-border px-5 py-3 font-display text-sm font-semibold">
          Recent reviews
        </div>
        <div className="divide-y divide-ink-border">
          {data.recent_reviews.length === 0 && (
            <div className="px-5 py-6 text-sm text-text-faint">No reviews yet.</div>
          )}
          {data.recent_reviews.map((r) => (
            <div key={r.id} className="flex items-center justify-between px-5 py-3">
              <div>
                <div className="text-sm text-text-primary">
                  {r.repo_full_name}{' '}
                  <span className="text-text-faint">#{r.pr_number}</span>
                </div>
                <div className="mt-0.5 text-xs text-text-faint">{r.pr_title}</div>
              </div>
              <div className="flex items-center gap-4 font-mono text-xs">
                <span className="text-text-muted">{r.findings_count} findings</span>
                <span
                  className={
                    r.score !== null && r.score >= 80
                      ? 'text-severity-low'
                      : r.score !== null && r.score >= 50
                      ? 'text-severity-medium'
                      : 'text-severity-critical'
                  }
                >
                  {r.score ?? '—'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function MetricCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-xl border border-ink-border bg-ink-panel p-4">
      <div className="text-xs text-text-faint">{label}</div>
      <div className="mt-1.5 font-display text-2xl font-semibold text-text-primary">{value}</div>
    </div>
  )
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-ink-border bg-ink-panel p-5">
      <h3 className="font-display text-sm font-semibold text-text-primary">{title}</h3>
      <div className="mt-3">{children}</div>
    </div>
  )
}
