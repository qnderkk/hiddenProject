<template>
  <div class="account-container">
    <div v-if="auth.isLoggedIn" class="profile-view">
      <h2>Личный кабинет</h2>
      <div class="profile-card">
        <p><strong>Имя:</strong> {{ auth.userName }}</p>
        <p><strong>Email:</strong> {{ auth.user?.email }}</p>
      </div>
      <button @click="auth.logout()" class="btn btn-logout">Выйти</button>
    </div>

    <div v-else>
      <div class="tabs">
        <button class="tab" :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">Вход</button>
        <button class="tab" :class="{ active: activeTab === 'register' }" @click="activeTab = 'register'">Регистрация</button>
      </div>

      <div v-if="activeTab === 'login'" class="form-container">
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>Email:</label>
            <input type="email" v-model="loginForm.email" required>
          </div>
          <div class="form-group">
            <label>Пароль:</label>
            <input type="password" v-model="loginForm.password" required>
          </div>
          <button type="submit" class="btn">Войти</button>
        </form>
      </div>

      <div v-if="activeTab === 'register'" class="form-container">
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>Имя:</label>
            <input type="text" v-model="registerForm.name" required>
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input type="email" v-model="registerForm.email" required>
          </div>
          <div class="form-group">
            <label>Пароль:</label>
            <input type="password" v-model="registerForm.password" required>
          </div>
          <button type="submit" class="btn">Зарегистрироваться</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth' // Импортируем наше хранилище

const auth = useAuthStore() // Инициализируем его
const activeTab = ref('login')

const loginForm = reactive({ email: '', password: '' })
const registerForm = reactive({ name: '', email: '', password: '' })

const handleLogin = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(loginForm)
    })
    const data = await response.json()

    if (response.ok) {
      // Сохраняем данные ЧЕРЕЗ Pinia
      auth.setUser({ name: data.user_name, email: loginForm.email })
    } else {
      alert(data.detail)
    }
  } catch (err) {
    alert("Бэкенд недоступен")
  }
}

const handleRegister = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerForm)
    })
    if (response.ok) {
      alert("Успешно! Войдите")
      activeTab.value = 'login'
    }
  } catch (err) {
    alert("Ошибка сети")
  }
}
</script>

<style scoped>
/* Ваши стили из старого файла */
.account-container { margin: 100px auto; max-width: 400px; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-radius: 8px;}
.tabs { display: flex; margin-bottom: 20px; border-bottom: 1px solid #ddd; }
.tab { flex: 1; padding: 10px; cursor: pointer; border: none; background: none; }
.tab.active { border-bottom: 2px solid var(--main-color); color: var(--main-color); font-weight: bold; }
.form-group { margin-bottom: 15px; }
input { width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; }
.btn { width: 100%; padding: 10px; background: var(--main-color); color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>