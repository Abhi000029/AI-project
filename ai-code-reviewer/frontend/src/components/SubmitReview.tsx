import { useState } from 'react'
import { api } from '../api/client'
import type { ReviewResult } from '../types'
import { FindingsList } from './FindingsList'

const SAMPLE_DIFF = `diff --git a/api/auth.py b/api/auth.py
index 3a1f2c1..9b2e0aa 100644
--- a/api/auth.py
+++ b/api/auth.py
@@ -12,6 +12,14 @@ def login(request):
     username = request.form.get("username")
     password = request.form.get("password")
 
+    query = "SELECT * FROM users WHERE username = '" + username + "'"
+    user = db.execute(query).fetchone()
+
+    if user and user["password"] == password:
+        session["user_id"] = user["id"]
+        return redirect("/dashboard")
+
+    return render_template("login.html", error="Invalid credentials")
+
 def logout(request):
     session.clear()
     return redirect("/login")
`

export function SubmitReview() {
  const [repo, setRepo] = useState('acme/webapp')
  const [prNumber, setPrNumber] = useState(42)
  const [prTitle, setPrTitle] = useState('Add login endpoint')
  const [author, setAuthor] = useState('priya')
  const [language, setLanguage] = useState('python')
  const [diff, setDiff] = useState(SAMPLE_DIFF)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<ReviewResult | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await api.analyze({
        repo_full_name: repo,
        pr_number: Number(prNumber),
        pr_title: prTitle,
        author,
        language,
        diff,
      })
      setResult(res)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[1fr_1fr]">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="rounded-xl border border-ink-border bg-ink-panel p-5">
          <h2 className="font-display text-sm font-semibold text-text-primary">
            Pull request details
          </h2>
          <div className="mt-4 grid grid-cols-2 gap-3">
            <Field label="Repository">
              <input
                value={repo}
                onChange={(e) => setRepo(e.target.value)}
                className="input"
                placeholder="org/repo"
              />
            </Field>
            <Field label="PR number">
              <input
                type="number"
                value={prNumber}
                onChange={(e) => setPrNumber(Number(e.target.value))}
                className="input"
              />
            </Field>
            <Field label="Author">
              <input
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                className="input"
              />
            </Field>
            <Field label="Language">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="input"
              >
                {['python', 'javascript', 'typescript', 'java', 'go', 'auto'].map((l) => (
                  <option key={l} value={l}>
                    {l}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="PR title" full>
              <input
                value={prTitle}
                onChange={(e) => setPrTitle(e.target.value)}
                className="input"
              />
            </Field>
          </div>
        </div>

        <div className="rounded-xl border border-ink-border bg-ink-panel p-5">
          <h2 className="font-display text-sm font-semibold text-text-primary">Diff</h2>
          <p className="mt-1 text-xs text-text-faint">
            Paste a unified diff. In production this arrives automatically via a GitHub/GitLab/
            Bitbucket webhook (FR-1).
          </p>
          <textarea
            value={diff}
            onChange={(e) => setDiff(e.target.value)}
            rows={14}
            spellCheck={false}
            className="mt-3 w-full resize-none rounded-lg border border-ink-border bg-ink px-3 py-3 font-mono text-xs leading-relaxed text-text-primary outline-none placeholder:text-text-faint focus:border-brand"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="flex items-center justify-center gap-2 rounded-lg bg-brand py-3 font-display text-sm font-semibold text-ink transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {loading ? (
            <>
              <span className="h-2 w-2 animate-pulseDot rounded-full bg-ink" />
              Analyzing diff…
            </>
          ) : (
            'Run AI review'
          )}
        </button>

        {error && (
          <div className="rounded-lg border border-severity-critical/30 bg-severity-critical/10 px-4 py-3 text-sm text-severity-critical">
            {error}
          </div>
        )}
      </form>

      <div className="min-h-[400px]">
        {loading && <ScanningPanel />}
        {!loading && result && <FindingsList result={result} />}
        {!loading && !result && !error && <EmptyPanel />}
      </div>
    </div>
  )
}

function Field({
  label,
  children,
  full,
}: {
  label: string
  children: React.ReactNode
  full?: boolean
}) {
  return (
    <label className={`flex flex-col gap-1.5 ${full ? 'col-span-2' : ''}`}>
      <span className="text-xs font-medium text-text-muted">{label}</span>
      {children}
    </label>
  )
}

function ScanningPanel() {
  return (
    <div className="relative flex h-full flex-col items-center justify-center overflow-hidden rounded-xl border border-ink-border bg-ink-panel py-24">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-24 animate-scan bg-gradient-to-b from-brand/25 to-transparent" />
      <div className="font-mono text-xs text-text-faint">
        <div className="mb-2 flex items-center gap-2 text-brand">
          <span className="h-2 w-2 animate-pulseDot rounded-full bg-brand" />
          scanning diff for bugs, vulnerabilities, style issues…
        </div>
      </div>
    </div>
  )
}

function EmptyPanel() {
  return (
    <div className="flex h-full flex-col items-center justify-center rounded-xl border border-dashed border-ink-border py-24 text-center">
      <div className="font-mono text-2xl text-text-faint">{'{ }'}</div>
      <p className="mt-3 max-w-xs text-sm text-text-faint">
        Findings will appear here once the review engine finishes analyzing the diff.
      </p>
    </div>
  )
}
