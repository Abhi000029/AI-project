import type { ReviewResult } from '../types'
import { SeverityBadge, severityDotColor } from './SeverityBadge'

export function FindingsList({ result }: { result: ReviewResult }) {
  const grouped = result.findings.reduce<Record<string, typeof result.findings>>((acc, f) => {
    acc[f.file] = acc[f.file] || []
    acc[f.file].push(f)
    return acc
  }, {})

  return (
    <div className="flex flex-col gap-4">
      <div className="rounded-xl border border-ink-border bg-ink-panel p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="font-display text-sm font-semibold text-text-primary">
              Review summary
            </h2>
            <p className="mt-1.5 text-sm leading-relaxed text-text-muted">{result.summary}</p>
          </div>
          <ScoreRing score={result.score} />
        </div>
        <div className="mt-4 flex gap-4 border-t border-ink-border pt-4 font-mono text-xs text-text-faint">
          <span>{result.findings.length} findings</span>
          <span>·</span>
          <span>{(result.duration_ms / 1000).toFixed(1)}s review time</span>
        </div>
      </div>

      {result.findings.length === 0 && (
        <div className="rounded-xl border border-severity-low/30 bg-severity-low/10 px-5 py-4 text-sm text-severity-low">
          No issues found — this diff looks clean.
        </div>
      )}

      {Object.entries(grouped).map(([file, findings]) => (
        <div key={file} className="overflow-hidden rounded-xl border border-ink-border">
          <div className="border-b border-ink-border bg-ink-raised px-4 py-2 font-mono text-xs text-text-muted">
            {file}
          </div>
          <div className="divide-y divide-ink-border bg-ink-panel">
            {findings.map((f) => (
              <div key={f.id} className="flex gap-3 px-4 py-3.5">
                <div className="flex w-10 flex-shrink-0 flex-col items-center pt-0.5">
                  <span
                    className="h-2.5 w-2.5 rounded-full"
                    style={{ backgroundColor: severityDotColor(f.severity) }}
                  />
                  {f.line && (
                    <span className="mt-1 font-mono text-[11px] text-text-faint">L{f.line}</span>
                  )}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <SeverityBadge severity={f.severity} />
                    <span className="rounded bg-ink px-1.5 py-0.5 font-mono text-[11px] uppercase tracking-wide text-text-faint">
                      {f.category.replace('_', ' ')}
                    </span>
                  </div>
                  <p className="mt-2 text-sm leading-relaxed text-text-primary">{f.message}</p>
                  {f.suggestion && (
                    <pre className="mt-2 overflow-x-auto rounded-lg border border-ink-border bg-ink px-3 py-2 font-mono text-xs leading-relaxed text-brand-soft">
                      {f.suggestion}
                    </pre>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function ScoreRing({ score }: { score: number }) {
  const color = score >= 80 ? '#6FCF97' : score >= 50 ? '#FFD166' : '#FF4757'
  return (
    <div className="flex flex-shrink-0 flex-col items-center">
      <div
        className="flex h-14 w-14 items-center justify-center rounded-full border-2 font-mono text-lg font-semibold"
        style={{ borderColor: color, color }}
      >
        {score}
      </div>
      <span className="mt-1 text-[10px] uppercase tracking-wide text-text-faint">Score</span>
    </div>
  )
}
