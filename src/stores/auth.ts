import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    login(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    logout() {
      this.token = null
      localStorage.removeItem('token')
    },
    setLoggedIn(isLoggedIn: boolean) {
      if (isLoggedIn) {
        this.token = localStorage.getItem('token')
      } else {
        this.logout()
      }
    },
  },
})
