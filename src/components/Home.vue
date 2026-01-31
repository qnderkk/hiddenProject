<template>
  <div>
    <section class="home" id="home" :style="{ backgroundImage: 'url(/img/background.jpg)', backgroundSize: 'cover' }">
      <div class="home-text">
        <h1>Ваш комфорт<br> - Наше счастье</h1>
        <router-link to="/products" class="btn">Купить сейчас</router-link>
      </div>
    </section>

    <section class="new" id="new">
      <div class="heading">
        <span>Новая Коллекция</span>
        <h2>Лидеры продаж</h2>
      </div>
      <div class="new-container">
        <ProductCard
            v-for="item in newProducts"
            :key="item.id"
            :product="item"
            @add-to-cart="onAdd($event)"
        />
      </div>
    </section>

    <section class="about" id="about">
      <div class="about-img">
        <img src="/img/about.jpg" alt="О нас">
      </div>
      <div class="about-text">
        <span>О нас</span>
        <h2>Мебель — это важная часть<br>уютного интерьера.</h2>
        <p>Мебель задаёт тон и атмосферу. Мы создаём решения, которые дарят комфорт и продуманность каждой детали.</p>
        <p>Откройте для себя мир, где эстетика встречается с функциональностью.</p>
      </div>
    </section>

    <div v-if="flyingItem.visible"
         class="flying-dot"
         :style="{ left: flyingItem.x + 'px', top: flyingItem.y + 'px' }">
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Product } from '../models/Product'
import ProductCard from './ProductCard.vue'
import { useCartStore } from '@/stores/cart' // Импортируем вашу корзину

const cart = useCartStore()

const newProducts = ref([
  new Product(1, 'Серое Кресло', 4999, '/img/new1.jpg', 4.5, 'new'),
  new Product(2, 'Бежевый Диван', 12999, '/img/new2.jpg', 5.0, 'new'),
  new Product(3, 'Деревянный Стол', 8499, '/img/new3.jpg', 4.5, 'new')
])

// Логика анимации
const flyingItem = reactive({ x: 0, y: 0, visible: false })

const onAdd = (data) => {
  // Вытаскиваем продукт и событие из того, что прислал ProductCard
  const { product, event } = data

  // Больше никаких alert! Запускаем полет:
  flyingItem.x = event.clientX
  flyingItem.y = event.clientY
  flyingItem.visible = true

  // Координаты корзины (обычно правый верхний угол)
  setTimeout(() => {
    flyingItem.x = window.innerWidth - 60
    flyingItem.y = 30
  }, 10)

  // Добавляем в хранилище и скрываем точку
  setTimeout(() => {
    flyingItem.visible = false
    cart.addToCart(product)
  }, 600)
}
</script>

<style scoped>
/* Добавляем стиль для летающей точки, чтобы она была видна */
.flying-dot {
  position: fixed;
  width: 15px;
  height: 15px;
  background: #ba1c1c;
  border-radius: 50%;
  z-index: 9999;
  pointer-events: none;
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Остальные ваши стили... */
</style>