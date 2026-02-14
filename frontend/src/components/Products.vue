<template>
  <div class="catalog-page">
    <h2 class="section-title">Каталог товаров</h2>

    <div class="container">
      <div v-if="auth.isAdmin" class="admin-panel">
        <h3>Добавить новый товар</h3>
        <form @submit.prevent="addProduct" class="admin-form">
          <input v-model="newProd.name" placeholder="Название товара" required />
          <input v-model.number="newProd.price" type="number" placeholder="Цена (₽)" required />

          <div class="file-input-wrapper">
            <label for="file-upload" class="custom-file-upload">
              <i class='bx bx-cloud-upload'></i>
              {{ selectedFile ? selectedFile.name : 'Выберите фото' }}
            </label>
            <input id="file-upload" type="file" @change="handleFileUpload" accept="image/*" required />
          </div>

          <button type="submit" class="btn-submit">Добавить в каталог</button>
        </form>
      </div>

      <div class="product-grid">
        <ProductCard
            v-for="product in products"
            :key="product.id"
            :product="product"
            :isAdmin="auth.isAdmin"
            @add-to-cart="onAdd($event)"
            @delete="deleteItem"
        />
      </div>
    </div>

    <div v-if="flyingItem.visible"
         class="flying-dot"
         :style="{ left: flyingItem.x + 'px', top: flyingItem.y + 'px' }">
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import ProductCard from "@/components/ProductCard.vue";
import { useAuthStore } from "@/stores/auth";
import { useCartStore } from "@/stores/cart";

const auth = useAuthStore();
const cart = useCartStore();
const products = ref([]);
const selectedFile = ref(null);

const newProd = reactive({
  name: "",
  price: "",
  category_id: 1 // Оставляем 1 по умолчанию для бэкенда
});

const flyingItem = reactive({ x: 0, y: 0, visible: false });

const loadData = async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/products");
    if (res.ok) {
      const data = await res.json();
      products.value = data.map(p => ({
        ...p,
        image: p.image_url ? `http://127.0.0.1:8000/${p.image_url.replace(/^\//, '')}` : '/img/placeholder.jpg'
      }));
    }
  } catch (err) {
    console.error("Ошибка загрузки:", err);
  }
};

const handleFileUpload = (event) => {
  selectedFile.value = event.target.files[0];
};

const addProduct = async () => {
  const formData = new FormData();
  formData.append("name", newProd.name);
  formData.append("price", newProd.price);
  formData.append("category_id", newProd.category_id); // Отправляем скрытую категорию
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
    const fileInput = document.getElementById("file-upload");
    if (fileInput) fileInput.value = "";
  }
};

const onAdd = (data) => {
  const { product, event } = data;
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

const deleteItem = async (id) => {
  if (confirm("Удалить товар?")) {
    await fetch(`http://127.0.0.1:8000/products/${id}`, { method: "DELETE" });
    loadData();
  }
};

onMounted(loadData);
</script>

<style scoped>
.catalog-page { padding-top: 120px; min-height: 100vh; background: #fff; }
.section-title { text-align: center; margin-bottom: 40px; font-size: 2.2rem; color: #333; font-weight: 600; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

/* Улучшенная админ-панель */
.admin-panel {
  background: #fdfdfd;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 50px;
  border: 1px dashed #ba1c1c;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.admin-panel h3 { margin-bottom: 20px; color: #333; font-size: 1.2rem; }
.admin-form { display: flex; gap: 20px; flex-wrap: wrap; align-items: center; }
.admin-form input {
  padding: 12px 15px;
  border: 1px solid #eee;
  border-radius: 6px;
  flex: 1;
  min-width: 200px;
  outline: none;
  transition: border 0.3s;
}
.admin-form input:focus { border-color: #ba1c1c; }

.btn-submit {
  background: #ba1c1c;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}
.btn-submit:hover { background: #961717; }

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 80px;
}

/* Летающая точка */
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

.custom-file-upload {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  cursor: pointer;
  background: #f0f0f0;
  border-radius: 6px;
  border: 1px solid #ddd;
  font-size: 0.9rem;
  transition: 0.3s;
}
.custom-file-upload:hover { background: #e5e5e5; }
#file-upload { display: none; }
</style>