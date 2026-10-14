import { useState } from 'react'

const defaultPrefs = {
  tone: 0.7,
  length: 0.5,
  technicality: 0.4,
  urgency: 0.3,
  clarity: 0.9,
}

export default function App() {
  const [features, setFeatures] = useState(defaultPrefs)
  const [result, setResult] = useState(null)
  const [feedback, setFeedback] = useState(0.8)

  const updateField = (key, value) => {
    setFeatures((prev) => ({ ...prev, [key]: Number(value) }))
  }

  const callPredict = async () => {
    const payload = { features: Object.values(features) }
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await response.json()
    setResult(data)
  }

  const sendFeedback = async () => {
    const payload = {
      ...features,
      rating: Number(feedback),
    }

    await fetch('http://localhost:8000/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    setResult({ status: 'feedback-submitted', rating: feedback })
  }

  return (
    <div className="app-shell">
      <header>
        <div>
          <h1>Personal AI Agent</h1>
          <div className="subtitle">Hybrid edge + cloud learning prototype</div>
        </div>
      </header>

      <div className="layout">
        <section className="panel">
          <div className="section-title">Preference profile</div>
          <div className="grid">
            {Object.entries(features).map(([key, value]) => (
              <label key={key}>
                <span>{key}</span>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={value}
                  onChange={(e) => updateField(key, e.target.value)}
                />
                <strong>{Number(value).toFixed(2)}</strong>
              </label>
            ))}
          </div>

          <div className="actions">
            <button onClick={callPredict}>Predict preference</button>
            <button className="secondary" onClick={sendFeedback}>Send feedback</button>
          </div>

          <div className="feedback-wrap">
            <label>
              User rating
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
              />
              <strong>{Number(feedback).toFixed(2)}</strong>
            </label>
          </div>
        </section>

        <section className="panel">
          <div className="section-title">System status</div>
          <div className="result-box">
            {result ? JSON.stringify(result, null, 2) : 'No result yet. Run a prediction or submit feedback.'}
          </div>
        </section>
      </div>
    </div>
  )
}
