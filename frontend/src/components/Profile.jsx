import React from 'react'
import { logout } from '../api/auth'

export default function Profile({ user, onLogout }) {
  const handleLogout = async () => {
    try {
      await logout()
    } catch (err) {
      // ignore errors; still clear client state
    }
    onLogout()
  }

  return (
    <div className="profile">
      <div>Signed in as <strong>{user}</strong></div>
      <div>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  )
}
