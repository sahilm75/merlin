import React, { useState, useEffect } from 'react'
import ChatList from './components/ChatList'
import ChatWindow from './components/ChatWindow'
import { getChatDetails } from './api/chat'
import api from './api/index'
import './App.css'

function App() {
  const [selectedChatId, setSelectedChatId] = useState(null)
  const [chatData, setChatData] = useState(null)
  const [loading, setLoading] = useState(false)

  // Get CSRF token on app load
  useEffect(() => {
    const fetchCSRFToken = async () => {
      try {
        // Get CSRF token from our dedicated endpoint
        await api.get('/nodes/csrf-token/')
        console.log('CSRF token fetched successfully')
      } catch (error) {
        console.error('Error fetching CSRF token:', error)
      }
    }
    fetchCSRFToken()
  }, [])

  const handleChatSelect = async (chatId) => {
    setLoading(true)
    try {
      const response = await getChatDetails(chatId)
      setChatData(response.data.chat)
      setSelectedChatId(chatId)
    } catch (error) {
      console.error('Error fetching chat details:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="app-container">
        <div className="sidebar">
          <ChatList 
            onChatSelect={handleChatSelect}
            selectedChatId={selectedChatId}
          />
        </div>
        <div className="main-content">
          {selectedChatId ? (
            <ChatWindow 
              chatId={selectedChatId}
              chatData={chatData}
              loading={loading}
            />
          ) : (
            <div className="welcome-screen">
              <h1>Welcome to Merlin</h1>
              <p>Select a chat from the sidebar or create a new one to get started.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
