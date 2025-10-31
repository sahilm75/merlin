import api from './index'

// Create a new chat
export const createChat = (systemMessage = '') => {
  const formData = new FormData()
  if (systemMessage) {
    formData.append('system_message', systemMessage)
  }
  
  return api.post('/nodes/create_chat/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

// Get user's chats
export const getUserChats = () => {
  return api.get('/nodes/get_user_chats/')
}

// Get chat details
export const getChatDetails = (chatId) => {
  return api.get(`/nodes/get_chat_details/${chatId}/`)
}

// Change chat title
export const changeChatTitle = (chatId, title) => {
  const formData = new FormData()
  formData.append('title', title)
  
  return api.post(`/nodes/change_chat_title/${chatId}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

// Get response from AI
export const getResponse = (prompt, nodeId) => {
  const formData = new FormData()
  formData.append('prompt', prompt)
  formData.append('node_id', nodeId)
  
  return api.post('/nodes/get_response/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}
