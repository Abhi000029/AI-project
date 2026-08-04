export type Severity = 'critical' | 'high' | 'medium' | 'low' | 'info'
export type Category = 'bug' | 'security' | 'performance' | 'style' | 'best_practice'

export interface Finding {
  id: string
  review_id: string
  file: string
  line: number | null
  severity: Severity
  category: Category
  message: string
  suggestion: string | null
}

export interface ReviewResult {
  review_id: string
  status: string
  summary: string
  score: number
  duration_ms: number
  findings: Finding[]
}

export interface Review {
  id: string
  repo_full_name: string
  pr_number: number
  pr_title: string
  author: string
  status: string
  score: number | null
  findings_count: number
  critical_count: number
  created_at: string
  duration_ms: number | null
}

export interface DashboardData {
  metrics: {
    total_reviews: number
    total_findings: number
    avg_quality_score: number | null
    avg_review_time_ms: number | null
  }
  severity_breakdown: Record<string, number>
  category_breakdown: Record<string, number>
  recent_reviews: Review[]
}
