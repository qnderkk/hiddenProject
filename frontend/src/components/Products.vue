<template>
  <div class="catalog-page">
    <h2 class="section-title">Каталог товаров</h2>

    <div class="container">
      <div v-if="auth.isAdmin" class="admin-panel">
        <form @submit.prevent="addProduct" class="admin-form">
          <input v-model="newProd.name" placeholder="Название" required />
          <input
            v-model.number="newProd.price"
            type="number"
            placeholder="Цена"
            required
          />
          <input v-model="newProd.image" placeholder="URL картинки" />
          <div class="file-input-wrapper">
            <label for="file-upload">Загрузить фото товара:</label>
            <input
              id="file-upload"
              type="file"
              @change="handleFileUpload"
              accept="image/*"
              required
            />
          </div>
          <button type="submit">Добавить в каталог</button>
        </form>
      </div>

      <div class="product-grid">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
          :isAdmin="auth.isAdmin"
          @add-to-cart="handleAddToCart"
          @delete="deleteItem"
        />
      </div>
    </div>

    <div
      v-if="flyingItem.visible"
      class="flying-dot"
      :style="{ left: flyingItem.x + 'px', top: flyingItem.y + 'px' }"
    ></div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import ProductCard from "@/components/ProductCard.vue"; // Импортируем компонент
import { useAuthStore } from "@/stores/auth";
import { useCartStore } from "@/stores/cart";

const selectedFile = ref(null);
const auth = useAuthStore();
const cart = useCartStore();
const products = ref([]);
const newProd = reactive({
  name: "",
  price: "",
  image: "",
  category: "standard",
});
const flyingItem = reactive({ x: 0, y: 0, visible: false });

const loadData = async () => {
  const res = await fetch("http://127.0.0.1:8000/products");
  if (res.ok) products.value = await res.json();
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
  }
};

const handleAddToCart = ({ product, event }) => {
  flyingItem.x = event.clientX;
  flyingItem.y = event.clientY;
  flyingItem.visible = true;
  setTimeout(() => {
    flyingItem.x = window.innerWidth - 60;
    flyingItem.y = 30;
  }, 10);
  setTimeout(() => {
    flyingItem.visible = false;
    cart.addToCart(product);
  }, 600);
};

const addProduct = async () => {
  const formData = new FormData();

  formData.append("name", newProd.name);
  formData.append("price", newProd.price);
  formData.append("category_id", 1);

  if (selectedFile.value) {
    formData.append("file", selectedFile.value);
  }

  const res = await fetch("http://127.0.0.1:8000/products", {
    method: "POST",
    body: formData,
  });

  if (res.ok) {
    await loadData();
    newProd.name = "";
    newProd.price = "";
    selectedFile.value = null;
    document.getElementById("file-upload").value = "";
  } else {
    const errorData = await res.json();
    alert("Ошибка при добавлении: " + JSON.stringify(errorData.detail));
  }
};

const deleteItem = async (id) => {
  if (confirm("Удалить товар?")) {
    await fetch(`http://127.0.0.1:8000/products/${id}`, { method: "DELETE" });
    loadData();
  }
};

onMounted(loadData);
</script>

<style scoped>
.catalog-page {
  padding-top: 100px;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}
.section-title {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2rem;
}
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
/* Стили для админ-панели */
.admin-panel {
  background: #f9f9f9;
  padding: 20px;
  margin-bottom: 30px;
  border: 1px dashed #ccc;
}
.admin-form {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.admin-form input {
  flex: 1;
  padding: 10px;
}
.admin-form button {
  background: #333;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}
</style>
