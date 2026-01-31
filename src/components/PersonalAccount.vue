<template>
  <div class="account-container">
    <div v-if="auth.isLoggedIn" class="profile-view">
      <h2>Личный кабинет</h2>
      <div class="profile-card">
        <p><strong>Имя:</strong> {{ auth.userName }}</p>
        <p><strong>Email:</strong> {{ auth.user?.email }}</p>
        <p v-if="auth.isAdmin" class="admin-badge">Статус: Администратор</p>
        <p v-else class="user-badge">Статус: Покупатель</p>
      </div>
      <button @click="auth.logout()" class="btn btn-logout">Выйти из аккаунта</button>
    </div>

    <div v-else>
      <div class="tabs">
        <button class="tab" :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">Вход</button>
        <button class="tab" :class="{ active: activeTab === 'register' }" @click="activeTab = 'register'">Регистрация</button>
      </div>
      <div v-if="activeTab === 'login'" class="form-container">
        <form @submit.prevent="handleLogin">
          <input type="email" v-model="loginForm.email" placeholder="Email" required>
          <input type="password" v-model="loginForm.password" placeholder="Пароль" required>
          <button type="submit" class="btn">Войти</button>
        </form>
      </div>
      <div v-if="activeTab === 'register'" class="form-container">
        <form @submit.prevent="handleRegister">
          <input type="text" v-model="registerForm.name" placeholder="Имя" required>
          <input type="email" v-model="registerForm.email" placeholder="Email" required>
          <input type="password" v-model="registerForm.password" placeholder="Пароль" required>
          <button type="submit" class="btn">Зарегистрироваться</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const activeTab = ref('login')

const loginForm = reactive({ email: '', password: '' })
const registerForm = reactive({ name: '', email: '', password: '' })

const handleLogin = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(loginForm)
    })
    if (res.ok) {
      const data = await res.json()
      auth.setUser(data)
    } else { alert("Неверный логин или пароль") }
  } catch (err) { alert("Ошибка сервера") }
}

const handleRegister = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerForm)
    })
    if (res.ok) { alert("Регистрация успешна!"); activeTab.value = 'login' }
  } catch (err) { alert("Ошибка сети") }
}
</script>

<style scoped>
.account-container { margin: 120px auto; max-width: 450px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-radius: 12px; background: #fff; }
.tabs { display: flex; margin-bottom: 20px; border-bottom: 2px solid #eee; }
.tab { flex: 1; padding: 10px; border: none; background: none; cursor: pointer; font-weight: bold; }
.tab.active { color: #ba1c1c; border-bottom: 2px solid #ba1c1c; }
.profile-card { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 20px; line-height: 1.6; }
.admin-badge { color: #d9534f; font-weight: bold; }
.btn-logout { background: #333; color: white; border: none; padding: 12px; width: 100%; cursor: pointer; border-radius: 5px; }
.form-container input { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
.btn { background: #ba1c1c; color: white; border: none; padding: 12px; width: 100%; cursor: pointer; border-radius: 5px; font-weight: bold; }
</style>