import api from './index'

export const register = (username, password) => {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  return api.post('/nodes/register/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export const login = (username, password) => {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  return api.post('/nodes/login/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export const logout = () => {
  // logout endpoint expects POST
  return api.post('/nodes/logout/', {}, {
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

export const currentUser = () => {
  return api.get('/nodes/current_user/')
}

export default {
  register,
  login,
  logout,
  currentUser,
}
