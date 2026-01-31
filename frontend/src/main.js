import { createApp } from 'vue'
import { createPinia } from 'pinia' // Импортируем Pinia
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
const pinia = createPinia() // Создаем экземпляр Pinia

app.use(pinia)   // Подключаем Pinia ПЕРЕД роутером или вместе с ним
app.use(router)
app.mount('#app')