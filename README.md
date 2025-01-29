# Flask Vulnerable App

Этот проект представляет собой веб-приложение на Flask с намеренно оставленными уязвимостями (SQL Injection, XSS, RCE) для целей обучения и тестирования.

## **Установка и запуск**

### **1. Клонируем репозиторий**
```bash
git clone https://github.com/Alex-XO/vulnerableapp.git
cd vulnerableapp
```

### **2. Создаём виртуальное окружение и активируем его**
```bash
python -m venv venv
```
- **Windows:**  `venv\Scripts\activate`
- **Linux/macOS:**  `source venv/bin/activate`

### **3. Устанавливаем зависимости**
```bash
pip install -r requirements.txt
```

### **4. Запускаем приложение**
```bash
python app.py
```
Приложение будет доступно по адресу **http://127.0.0.1:5000**

## **Описание уязвимостей**
1. **SQL Injection** (`/login`) – уязвимость в форме входа.
2. **XSS (Cross-Site Scripting)** (`/comments`) – неэкранированный ввод комментариев.
3. **RCE (Remote Code Execution)** (`/search`) – выполнение системных команд.
