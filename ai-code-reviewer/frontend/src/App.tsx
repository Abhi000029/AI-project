import { useState } from 'react'
import { Header } from './components/Header'
import { SubmitReview } from './components/SubmitReview'
import { Dashboard } from './components/Dashboard'

function App() {
  const [view, setView] = useState<'review' | 'dashboard'>('review')

  return (
    <div className="min-h-screen">
      <Header view={view} onChange={setView} />
      <main className="mx-auto max-w-6xl px-6 py-8">
        {view === 'review' ? <SubmitReview /> : <Dashboard />}
      </main>
    </div>
  )
}

export default App
