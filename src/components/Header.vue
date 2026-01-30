<template>
  <header>
    <router-link to="/" class="logo">Heart&<span>Craft</span></router-link>
    <div class="bx bx-menu" id="menu-icon" @click="toggleMenu"></div>

    <ul class="navbar" :class="{ active: isMenuOpen }">
      <li><router-link to="/" @click="closeMenu">Главная</router-link></li>
      <li><router-link :to="{ path: '/', hash: '#new' }" @click="closeMenu">Новые поступления</router-link></li>
      <li><router-link :to="{ path: '/', hash: '#about' }" @click="closeMenu">О Нас</router-link></li>
      <li><router-link to="/products" @click="closeMenu">Каталог</router-link></li>
      <li><router-link to="/account" @click="closeMenu">Личный кабинет</router-link></li>
    </ul>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)
const toggleMenu = () => isMenuOpen.value = !isMenuOpen.value
const closeMenu = () => isMenuOpen.value = false
</script>