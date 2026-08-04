import type { DashboardData, ReviewResult } from '../types'

const BASE = '/api/v1'

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed (${res.status})`)
  }
  return res.json()
}

export interface AnalyzePayload {
  repo_full_name: string
  pr_number: number
  pr_title: string
  author: string
  language: string
  diff: string
}

export const api = {
  analyze: (payload: AnalyzePayload) =>
    fetch(`${BASE}/reviews/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).then((r) => handle<ReviewResult>(r)),

  dashboard: () => fetch(`${BASE}/analytics/dashboard`).then((r) => handle<DashboardData>(r)),

  listReviews: () => fetch(`${BASE}/reviews`).then((r) => handle(r)),
}
