<template>
  <section class="shop" id="shop">
    <div class="heading">
      <span style="color: var(--main-color); font-weight: 600;">Каталог товаров</span>
      <h2>Все товары</h2>
    </div>

    <div class="shop-container">
      <ProductCard
          v-for="item in catalog"
          :key="item.id"
          :product="item"
          @add-to-cart="handleAddToCart"
      />
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { Product } from '../models/Product'
import ProductCard from './ProductCard.vue'

const catalog = ref([
  new Product(1, 'Серое Кресло', 4999, '/img/p1.jpg', 4.5),
  new Product(2, 'Бежевый Диван', 12999, '/img/p2.jpg', 5.0),
  new Product(3, 'Деревянный Стол', 8499, '/img/p3.jpg', 4.5),
  new Product(4, 'Белый Комод', 6999, '/img/p4.jpg', 5.0),
  new Product(5, 'Двуспальная Кровать', 24999, '/img/p5.jpg', 4.5),
  new Product(6, 'Прикроватная Тумба', 3499, '/img/p6.jpg', 4.5)
])

const handleAddToCart = (product) => {
  alert(`Товар "${product.name}" добавлен в корзину!`)
}
</script>