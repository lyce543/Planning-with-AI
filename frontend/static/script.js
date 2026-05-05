// frontend/static/script.js
console.log("✅ script.js виконався");  // Перевірка підключення

document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ DOM завантажено");

  const chatContainer = document.getElementById("chat-container");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");

  console.log("form:", form, "input:", input, "chatContainer:", chatContainer);

  if (!chatContainer || !form || !input) {
    console.error("❌ Якийсь елемент не знайдено у DOM.");
    return;
  }

  async function sendMessage(message) {
    // Додаємо повідомлення користувача
    const userDiv = document.createElement("div");
    userDiv.classList.add("message", "user-message");
    userDiv.textContent = message;
    chatContainer.appendChild(userDiv);

    // Очистимо інпут
    input.value = "";

    try {
      const res = await fetch("/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      // Перевірка статусу
      if (!res.ok) {
        const errorText = await res.text();  // <- читаємо як текст
        throw new Error(`❌ Server returned ${res.status}: ${errorText}`);
      }

      // Парсимо JSON
      const data = await res.json();
      console.log("✅ AI response:", data);

      // Додаємо відповідь бота
      const botDiv = document.createElement("div");
      botDiv.classList.add("message", "bot-message");
      botDiv.textContent = data.response || "⚠️ Бот не відповів.";
      chatContainer.appendChild(botDiv);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    } catch (err) {
      console.error("❌ Помилка при fetch:", err.message || err);

      const errorDiv = document.createElement("div");
      errorDiv.classList.add("message", "bot-message", "error-message");
      errorDiv.textContent = `⚠️ Помилка: ${err.message || "невідома"}`;
      chatContainer.appendChild(errorDiv);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }

  // Відправка через кнопку
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if (message) sendMessage(message);
  });

  // Відправка через Enter
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const message = input.value.trim();
      if (message) sendMessage(message);
    }
  });
});
