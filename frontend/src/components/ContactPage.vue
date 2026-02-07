<template>
  <div class="contact-page">
    <div class="container">
      <div class="contact-card">
        <h2 class="section-title">Свяжитесь с нами</h2>

        <form @submit.prevent="submitForm" class="contact-form">
          <div class="form-group">
            <label for="name">Ваше имя *</label>
            <input
              id="name"
              v-model="formData.name"
              type="text"
              placeholder="Введите ваше имя"
              required
            />
          </div>

          <div class="form-group">
            <label for="email">Email *</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              placeholder="Введите ваш email"
              required
            />
          </div>

          <div class="form-group">
            <label for="subject">Тема *</label>
            <select id="subject" v-model="formData.subject" required>
              <option value="" disabled selected>Выберите тему</option>
              <option value="order">Вопрос по заказу</option>
              <option value="cooperation">Сотрудничество</option>
              <option value="feedback">Отзыв / Предложение</option>
              <option value="other">Другое</option>
            </select>
          </div>

          <div class="form-group">
            <label for="message">Сообщение *</label>
            <textarea
              id="message"
              v-model="formData.message"
              placeholder="Введите ваше сообщение"
              rows="5"
              required
            ></textarea>
          </div>

          <button type="submit" class="submit-btn">Отправить</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";

const formData = reactive({
  name: "",
  email: "",
  subject: "",
  message: "",
});

const submitForm = async () => {
  // Здесь будет логика отправки на бэкенд
  console.log("Отправка данных формы:", formData);

  // Пример запроса (раскомментируй когда будет готов бэкенд)
  try {
    const res = await fetch("http://127.0.0.1:8000/contacts/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    if (res.ok) alert("Сообщение отправлено!");
  } catch (e) {
    console.error(e);
  }

  alert("Спасибо, ${formData.name}! Мы получили ваше сообщение.");

  // Очистка формы
  formData.name = "";
  formData.email = "";
  formData.subject = "";
  formData.message = "";
};
</script>

<style scoped>
.contact-page {
  padding-top: 100px;
  padding-bottom: 60px;
  background-color: #f9f9f9; /* Общий фон как на главной */
  min-height: 100vh;
}

.container {
  max-width: 800px; /* Делаем форму уже, чем весь сайт, для читаемости */
  margin: 0 auto;
  padding: 0 20px;
}

.contact-card {
  background: #ffffff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); /* Легкая тень вместо темного фона */
}

.section-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  color: #333; /* Твой основной цвет текста */
  font-weight: 700;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  font-size: 0.95rem;
  color: #444;
}

/* Стили полей ввода под Heart&Craft */
.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #fdfdfd;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #ba1c1c; /* Твой акцентный красный */
  box-shadow: 0 0 0 3px rgba(186, 28, 28, 0.1);
}

.form-group textarea {
  resize: vertical;
}

/* Кнопка под стиль админки и карточек */
.submit-btn {
  margin-top: 10px;
  background-color: #333; /* Темный, как в админ-панели */
  color: white;
  border: none;
  padding: 15px;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s;
}

.submit-btn:hover {
  background-color: #ba1c1c; /* Красный при наведении */
  transform: translateY(-2px);
}

.submit-btn:active {
  transform: translateY(0);
}
</style>
