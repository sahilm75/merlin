import React, { useState } from 'react'
import { login } from '../api/auth'

export default function Login({ onLogin, switchToRegister }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      const res = await login(username, password)
      if (res && res.data) {
        onLogin(res.data.username)
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed')
    }
  }

  return (
    <div className="auth-form">
      <h3>Login</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <input placeholder="username" value={username} onChange={e => setUsername(e.target.value)} />
        </div>
        <div>
          <input type="password" placeholder="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        <div>
          <button type="submit">Login</button>
          <button type="button" onClick={switchToRegister}>Register</button>
        </div>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  )
}
