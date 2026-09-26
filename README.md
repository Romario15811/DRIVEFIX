# 🚗 DRIVEFIX

Responsive website for an auto service with online booking and Telegram integration.

DRIVEFIX allows customers to submit a service request through the website. The request is validated by the frontend and backend and then delivered to the auto service owner through a Telegram bot.

## ✨ Features

- Responsive design for desktop, tablet and mobile
- Mobile navigation menu
- Online service booking form
- Frontend form validation
- Backend validation
- Telegram booking notifications
- Basic rate limiting
- CORS configuration
- Secure environment variables
- Responsive hero section

## 🛠 Technologies

### Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API

### Backend

- Python
- Flask
- Flask-CORS
- Requests
- python-dotenv

### Integration

- Telegram Bot API

## 🔄 How it works

```text
Customer
   ↓
DRIVEFIX website
   ↓
JavaScript validation
   ↓
POST /api/booking
   ↓
Flask backend
   ↓
Server validation
   ↓
Telegram Bot API
   ↓
Auto service owner
```

## 🔐 Security

Sensitive data such as the Telegram bot token and chat ID are stored in environment variables and are not included in the repository.

The backend performs its own validation instead of relying only on client-side JavaScript.

## 🚀 Local development

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Run the backend:

```bash
python server.py
```

Run the frontend using Live Server or another local development server.

## 📌 Status

DRIVEFIX is currently being prepared for deployment.

## 👨‍💻 Author

Created as a full-stack web development project.