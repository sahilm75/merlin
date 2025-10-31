# Merlin

A sophisticated AI chat application built with Django and React, featuring a node-based conversation management system.

## 🌟 Features

- **Modern Web Interface**: Beautiful React frontend with real-time chat
- **Node-based Conversations**: Track conversation history as a tree structure
- **AI Integration**: Powered by LangChain and Groq for intelligent responses
- **User Management**: Built-in Django authentication system
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 5.2.7
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **AI Integration**: LangChain with Groq LLM
- **API**: RESTful endpoints with CORS support

### Frontend (React + Vite)
- **Framework**: React 18 with modern hooks
- **Build Tool**: Vite for fast development and optimized builds
- **Styling**: Modern CSS with gradients and glass morphism effects
- **HTTP Client**: Axios for API communication

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- pip and npm

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd merlin
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file in the root directory
GROQ_API_KEY=your_groq_api_key_here
```

5. Run database migrations:
```bash
cd src
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Start the Django development server:
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## 📁 Project Structure

```
merlin/
├── src/                    # Django backend
│   ├── merlin/            # Main Django project
│   ├── nodes/             # Chat and node management app
│   ├── manage.py
│   └── db.sqlite3
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── api/          # API integration
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
├── requirements.txt       # Python dependencies
├── docker-compose.yml    # Docker configuration
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Django Settings (optional)
DEBUG=True
SECRET_KEY=your_secret_key_here
```

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (React dev server)
- `http://127.0.0.1:3000`

## 🐳 Docker Support

Run the entire application with Docker:

```bash
docker-compose up -d
```

This will start both the Django backend and React frontend in containers.

## 📖 API Documentation

### Chat Endpoints

- `POST /nodes/create_chat/` - Create a new chat
- `GET /nodes/get_user_chats/` - Get user's chat list
- `GET /nodes/get_chat_details/{chat_id}/` - Get chat details
- `POST /nodes/change_chat_title/{chat_id}/` - Update chat title
- `POST /nodes/get_response/` - Send message and get AI response

### Authentication

The application uses Django's built-in session authentication. Users need to be logged in to access chat functionality.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Django](https://djangoproject.com/)
- Frontend powered by [React](https://react.dev/) and [Vite](https://vitejs.dev/)
- AI integration via [LangChain](https://langchain.com/) and [Groq](https://groq.com/)