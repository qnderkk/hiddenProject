<template>
  <div class="product-card">
    <div class="image-container">
      <img
          :src="product.image"
          :alt="product.name"
          class="product-image"
          @error="(e) => e.target.src = '/img/placeholder.jpg'"
      />
      <div class="overlay">
        <button @click="handleOnAdd($event)" class="add-to-cart-btn">
          В корзину
        </button>
      </div>
    </div>
    <div class="product-details">
      <h3>{{ product.name }}</h3>
      <p class="product-price">{{ product.price }} ₽</p>

      <button
          v-if="isAdmin"
          @click="$emit('delete', product.id)"
          class="admin-delete-btn"
      >
        Удалить товар
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(["product", "isAdmin"]);
const emit = defineEmits(["delete", "add-to-cart"]);

const handleOnAdd = (event) => {
  emit("add-to-cart", { product: props.product, event: event });
};
</script>

<style scoped>
/* Ваши оригинальные стили */
.product-card {
  background: #fff;
  transition: transform 0.4s ease;
  border: 1px solid #f0f0f0;
  width: 100%;
}
.product-card:hover { transform: translateY(-10px); }

.image-container {
  position: relative;
  overflow: hidden;
  height: 350px;
}
.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}
.product-card:hover .image-container img { transform: scale(1.1); }

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.product-card:hover .overlay { opacity: 1; }

.add-to-cart-btn {
  background: #ba1c1c;
  color: #fff;
  border: none;
  padding: 12px 25px;
  cursor: pointer;
  font-weight: bold;
  text-transform: uppercase;
}

.product-details { padding: 20px; text-align: center; }
.product-details h3 { font-size: 1.1rem; margin-bottom: 10px; font-weight: 500; color: #333; }
.product-price { color: #ba1c1c; font-size: 1.2rem; font-weight: 600; }

.admin-delete-btn {
  margin-top: 15px;
  background: none;
  border: 1px solid #ff4d4d;
  color: #ff4d4d;
  padding: 5px 12px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.8rem;
  transition: 0.3s;
}
.admin-delete-btn:hover {
  background: #ff4d4d;
  color: #fff;
}
</style>
