import React, { useState, useEffect } from 'react'
import { getUserChats, createChat } from '../api/chat'
import './ChatList.css'

const ChatList = ({ onChatSelect, selectedChatId }) => {
  const [chats, setChats] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchChats()
  }, [])

  const fetchChats = async () => {
    try {
      setLoading(true)
      const response = await getUserChats()
      setChats(response.data.chats)
    } catch (error) {
      setError('Failed to load chats')
      console.error('Error fetching chats:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateChat = async () => {
    try {
      const response = await createChat()
      const newChatId = response.data.chat_id
      await fetchChats() // Refresh the chat list
      onChatSelect(newChatId) // Select the new chat
    } catch (error) {
      console.error('Error creating chat:', error)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="chat-list">
        <div className="chat-list-header">
          <h2>Chats</h2>
          <button className="new-chat-btn" disabled>
            + New Chat
          </button>
        </div>
        <div className="loading">Loading chats...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="chat-list">
        <div className="chat-list-header">
          <h2>Chats</h2>
          <button className="new-chat-btn" onClick={handleCreateChat}>
            + New Chat
          </button>
        </div>
        <div className="error">{error}</div>
      </div>
    )
  }

  return (
    <div className="chat-list">
      <div className="chat-list-header">
        <h2>Chats</h2>
        <button className="new-chat-btn" onClick={handleCreateChat}>
          + New Chat
        </button>
      </div>
      <div className="chat-list-content">
        {chats.length === 0 ? (
          <div className="no-chats">
            <p>No chats yet</p>
            <p>Create your first chat to get started</p>
          </div>
        ) : (
          chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${selectedChatId === chat.id ? 'active' : ''}`}
              onClick={() => onChatSelect(chat.id)}
            >
              <div className="chat-title">{chat.title}</div>
              <div className="chat-date">{formatDate(chat.updated_at)}</div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default ChatList
