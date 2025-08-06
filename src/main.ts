import './assets/css/main.css'

import { Chart, Filler } from 'chart.js'
import { createPinia } from 'pinia'
import { createApp } from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faArrowDown,
  faArrowRight,
  faArrowUp,
  faGear,
  faHome,
  faMagnifyingGlass,
  faUser,
  faWallet,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import type { PluginOptions } from 'vue-toastification'
import Toast, { POSITION } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import App from './App.vue'
import router from './router'

library.add(
  faUser,
  faHome,
  faGear,
  faWallet,
  faArrowUp,
  faArrowDown,
  faMagnifyingGlass,
  faArrowRight,
)
const app = createApp(App)
const pinia = createPinia()
const options: PluginOptions = {
  position: POSITION.TOP_RIGHT,
  timeout: 3000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
}

Chart.register(Filler)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(pinia)
app.use(router)
app.use(Toast, options)

app.mount('#app')
