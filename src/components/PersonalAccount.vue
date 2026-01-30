<template>
  <div class="account-container">
    <div class="tabs">
      <button class="tab" :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">Вход</button>
      <button class="tab" :class="{ active: activeTab === 'register' }" @click="activeTab = 'register'">Регистрация</button>
    </div>

    <div v-if="activeTab === 'login'" class="form-container active">
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

    <div v-if="activeTab === 'register'" class="form-container active">
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
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeTab = ref('login')
const loginForm = reactive({ email: '', password: '' })
const registerForm = reactive({ name: '', email: '', password: '' })

const handleLogin = () => alert(`Вход: ${loginForm.email}`)
const handleRegister = () => alert(`Регистрация: ${registerForm.name}`)
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