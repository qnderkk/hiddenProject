<template>
  <div class="box">
    <div class="box-img">
      <img :src="product.image" :alt="product.name">
      <span v-if="product.isNewArrival && product.isNewArrival()" class="badge-new">New</span>
    </div>
    <div class="title-price">
      <h3>{{ product.name }}</h3>
      <div class="stars">
        <i v-for="i in 5" :key="i" :class="product.getStarClass ? product.getStarClass(i) : 'bx bxs-star'"></i>
      </div>
    </div>
    <span>{{ product.formattedPrice || product.price + ' ₽' }}</span>

    <i class='bx bx-cart' @click="addToCart"></i>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useCartStore } from '@/stores/cart' // Импортируем хранилище корзины

const props = defineProps(['product'])
const cart = useCartStore() // Инициализируем корзину

const addToCart = () => {
  // Добавляем объект товара в корзину
  // Если product — это класс, Pinia сохранит его данные
  cart.addToCart({
    id: props.product.id,
    name: props.product.name,
    price: props.product.price,
    image: props.product.image
  })

  // Маленькое уведомление для пользователя
  console.log(`Товар ${props.product.name} добавлен!`)
}
</script>

<style scoped>
/* Твои стили */
.box {
  position: relative;
  transition: all .40s ease;
}
.box:hover {
  transform: translateY(-5px);
}
.badge-new {
  position: absolute;
  top: 10px;
  left: 10px;
  background: var(--main-color);
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  z-index: 10;
}
.bx-cart {
  position: absolute;
  bottom: 20px;
  right: 20px;
  padding: 7px;
  background: var(--main-color);
  color: white;
  border-radius: 5px;
  cursor: pointer;
}
.bx-cart:hover {
  background: #333; /* Темнеет при наведении */
}
</style>