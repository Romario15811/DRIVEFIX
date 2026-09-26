# 🚗 DRIVEFIX

Responsive full-stack website for an auto service with online booking and Telegram integration.

Customers can submit a service request directly through the website. The request is validated by the frontend and backend, processed by a Flask API and delivered to the auto service owner through Telegram.

## 🌐 Live Demo

**Website:**  
https://romario15811.github.io/DRIVEFIX/

**API Health Check:**  
https://drivefix-api-pwn5.onrender.com/api/health

## 📸 Preview

![DRIVEFIX Preview](images/drivefix-preview.png)

## ✨ Features

- Responsive design for desktop, tablet and mobile
- Mobile navigation menu
- Online service booking form
- Frontend form validation
- Backend validation
- Telegram booking notifications
- Basic rate limiting
- CORS configuration
- Environment variables for sensitive data
- API health check
- Responsive hero section
- Production deployment

## 🛠 Technologies

### Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API
- GitHub Pages

### Backend

- Python
- Flask
- Flask-CORS
- Gunicorn
- Requests
- python-dotenv
- Render

### Integration

- Telegram Bot API

## 🔄 Architecture

```text
Customer
   ↓
GitHub Pages
   ↓
DRIVEFIX Frontend
   ↓
JavaScript validation
   ↓
HTTPS POST /api/booking
   ↓
Render
   ↓
Flask + Gunicorn
   ↓
Backend validation
   ↓
Telegram Bot API
   ↓
Auto service owner
```

## 🔐 Security

Sensitive data such as the Telegram bot token and chat ID are stored in environment variables and are not included in the repository.

The backend performs its own validation instead of relying only on client-side JavaScript.

CORS is configured to allow requests from the production frontend and local development environment.

## 🚀 Local Development

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
FRONTEND_ORIGIN=https://your-frontend-domain.com
```

Run the backend:

```bash
python server.py
```

Run the frontend using Live Server or another local development server.

## 📡 API

### Health Check

```http
GET /api/health
```

Example response:

```json
{
    "service": "DRIVEFIX API",
    "status": "ok"
}
```

### Create Booking

```http
POST /api/booking
```

Example request:

```json
{
    "name": "Roman",
    "phone": "+380991234567",
    "car": "Ford Focus",
    "service": "Diagnostics"
}
```

## 📌 Status

✅ Deployed and working.

The frontend is hosted on GitHub Pages and the Flask API is deployed on Render.

## 👨‍💻 Author

Created as a full-stack web development portfolio project.