import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user_data')) || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.user,
    userName: (state) => state.user ? state.user.name : ''
  },
  actions: {
    setUser(userData) {
      this.user = userData
      localStorage.setItem('user_data', JSON.stringify(userData))
    },
    logout() {
      this.user = null
      localStorage.removeItem('user_data')
    }
  }
})