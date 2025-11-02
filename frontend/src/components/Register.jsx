import React, { useState } from 'react'
import { register } from '../api/auth'

export default function Register({ onRegister, switchToLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      const res = await register(username, password)
      if (res && res.data) {
        onRegister(res.data.username)
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed')
    }
  }

  return (
    <div className="auth-form">
      <h3>Register</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <input placeholder="username" value={username} onChange={e => setUsername(e.target.value)} />
        </div>
        <div>
          <input type="password" placeholder="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        <div>
          <button type="submit">Register</button>
          <button type="button" onClick={switchToLogin}>Back to Login</button>
        </div>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  )
}
