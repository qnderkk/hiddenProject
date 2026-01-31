<template>
  <header>
    <router-link to="/" class="logo">Heart&<span>Craft</span></router-link>
    <div class="bx bx-menu" id="menu-icon" @click="toggleMenu"></div>

    <ul class="navbar" :class="{ active: isMenuOpen }">
      <li><router-link to="/" @click="closeMenu">Главная</router-link></li>
      <li><router-link :to="{ path: '/', hash: '#new' }" @click="closeMenu">Новинки</router-link></li>
      <li><router-link to="/products" @click="closeMenu">Каталог</router-link></li>

      <li>
        <router-link to="/cart" class="cart-link" @click="closeMenu">
          Корзина <span v-if="cart.totalCount > 0" class="cart-badge">{{ cart.totalCount }}</span>
        </router-link>
      </li>

      <li>
        <router-link to="/account" @click="closeMenu" class="user-link">
          <span v-if="auth.isLoggedIn">👤 {{ auth.userName }}</span>
          <span v-else>Личный кабинет</span>
        </router-link>
      </li>
    </ul>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth' // Импортируем хранилище юзера
import { useCartStore } from '@/stores/cart' // Импортируем хранилище корзины

const isMenuOpen = ref(false)
const auth = useAuthStore()
const cart = useCartStore()

const toggleMenu = () => isMenuOpen.value = !isMenuOpen.value
const closeMenu = () => isMenuOpen.value = false
</script>

<style scoped>
/* Добавляем стили для индикатора корзины */
.cart-link {
  position: relative;
}

.cart-badge {
  background: var(--main-color);
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 50%;
  position: relative;
  top: -10px;
  margin-left: 2px;
}

.user-link {
  font-weight: bold;
  color: var(--main-color) !important;
}

/* Стили для иконки меню (если нужно подправить под стиль) */
#menu-icon {
  font-size: 24px;
  cursor: pointer;
  z-index: 10001;
  display: none; /* Обычно скрыто на десктопах */
}

@media (max-width: 768px) {
  #menu-icon { display: block; }
}
</style>