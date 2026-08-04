interface Props {
  view: 'review' | 'dashboard'
  onChange: (v: 'review' | 'dashboard') => void
}

export function Header({ view, onChange }: Props) {
  return (
    <header className="border-b border-ink-border">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand/15 font-mono text-sm font-semibold text-brand">
            ▲▼
          </div>
          <div>
            <h1 className="font-display text-lg font-semibold leading-none text-text-primary">
              AI Code Reviewer
            </h1>
            <p className="mt-0.5 text-xs text-text-faint">Automated PR analysis engine</p>
          </div>
        </div>

        <nav className="flex items-center gap-1 rounded-lg bg-ink-panel p-1">
          <button
            onClick={() => onChange('review')}
            className={`rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
              view === 'review'
                ? 'bg-brand text-ink'
                : 'text-text-muted hover:text-text-primary'
            }`}
          >
            Review
          </button>
          <button
            onClick={() => onChange('dashboard')}
            className={`rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
              view === 'dashboard'
                ? 'bg-brand text-ink'
                : 'text-text-muted hover:text-text-primary'
            }`}
          >
            Dashboard
          </button>
        </nav>
      </div>
    </header>
  )
}
