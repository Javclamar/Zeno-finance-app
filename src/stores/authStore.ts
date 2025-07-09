import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    loginTime: localStorage.getItem('loginTime') || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    login(token: string) {
      this.token = token
      const now = Date.now().toString()
      this.loginTime = now

      localStorage.setItem('loginTime', now)
      localStorage.setItem('token', token)
    },

    logout() {
      this.token = null
      this.loginTime = null
      localStorage.removeItem('token')
      localStorage.removeItem('loginTime')

      if (window.location.pathname !== '/') {
        window.location.href = '/'
      }
    },
    setLoggedIn(isLoggedIn: boolean) {
      if (isLoggedIn) {
        const now = Date.now().toString()
        this.loginTime = now
        localStorage.setItem('loginTime', now)
        this.token = localStorage.getItem('token')
        window.location.href = '/dashboard'
      } else {
        this.logout()
      }
    },

    checkTokenValidity() {
      const loginTimestamp = parseInt(localStorage.getItem('loginTime') || '0')
      const now = Date.now()
      const fiveHours = 5 * 60 * 60 * 1000

      if (!loginTimestamp || now - loginTimestamp > fiveHours) {
        this.logout()
      } else {
        this.scheduleAutoLogout(fiveHours - (now - loginTimestamp))
      }
    },

    scheduleAutoLogout(delayMs?: number) {
      const timeout = delayMs ?? 5 * 60 * 60 * 1000
      setTimeout(() => {
        this.logout()
      }, timeout)
    },
  },
})
