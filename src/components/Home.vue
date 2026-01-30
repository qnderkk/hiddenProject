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
            @add-to-cart="onAdd"
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Product } from '../models/Product'
import ProductCard from './ProductCard.vue'

const newProducts = ref([
  new Product(1, 'Серое Кресло', 4999, '/img/new1.jpg', 4.5, 'new'),
  new Product(2, 'Бежевый Диван', 12999, '/img/new2.jpg', 5.0, 'new'),
  new Product(3, 'Деревянный Стол', 8499, '/img/new3.jpg', 4.5, 'new')
])

const onAdd = (product) => alert(`Добавлено: ${product.name}`)
</script>