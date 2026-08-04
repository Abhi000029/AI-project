import type { Severity } from '../types'

const CONFIG: Record<Severity, { label: string; color: string; bg: string }> = {
  critical: { label: 'Critical', color: '#FF4757', bg: 'rgba(255,71,87,0.12)' },
  high: { label: 'High', color: '#FF8B5E', bg: 'rgba(255,139,94,0.12)' },
  medium: { label: 'Medium', color: '#FFD166', bg: 'rgba(255,209,102,0.12)' },
  low: { label: 'Low', color: '#6FCF97', bg: 'rgba(111,207,151,0.12)' },
  info: { label: 'Info', color: '#7C9CFF', bg: 'rgba(124,156,255,0.12)' },
}

export function SeverityBadge({ severity }: { severity: Severity }) {
  const cfg = CONFIG[severity]
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-mono font-medium tracking-wide"
      style={{ color: cfg.color, backgroundColor: cfg.bg }}
    >
      <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: cfg.color }} />
      {cfg.label.toUpperCase()}
    </span>
  )
}

export function severityDotColor(severity: Severity) {
  return CONFIG[severity].color
}
