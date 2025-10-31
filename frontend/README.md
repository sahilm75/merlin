# Merlin Frontend

A modern React + Vite frontend for the Merlin AI chat application.

## Features

- ✨ Beautiful, modern UI with gradient backgrounds and glass morphism effects
- 💬 Real-time chat interface
- 📱 Responsive design for desktop and mobile
- 🔄 Live chat management with create/select functionality
- 🎨 Smooth animations and typing indicators
- 🌙 Dark theme optimized design

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Axios** - HTTP client for API calls
- **CSS3** - Styling with modern features (gradients, backdrop-filter, etc.)

## Getting Started

### Prerequisites

- Node.js (version 14+ recommended)
- npm or yarn package manager

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Configuration

The frontend is configured to proxy API requests to the Django backend running on `localhost:8000`. 

### API Integration

All API calls are handled through the `/src/api/` directory:

- `index.js` - Axios configuration and interceptors
- `chat.js` - Chat-related API endpoints

### Environment Setup

Make sure your Django backend is running on `http://localhost:8000` for the API proxy to work correctly.

## Project Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── api/         # API integration
│   ├── components/  # React components
│   │   ├── ChatList.jsx
│   │   ├── ChatWindow.jsx
│   │   └── *.css    # Component styles
│   ├── App.jsx      # Main app component
│   ├── main.jsx     # App entry point
│   └── index.css    # Global styles
├── package.json
└── vite.config.js   # Vite configuration
```

## Styling

The application uses a modern design system featuring:

- **Color Scheme**: Purple-blue gradients with glass morphism effects
- **Typography**: Inter font family for clean, modern text
- **Layout**: Flexbox-based responsive layouts
- **Effects**: Backdrop blur, box shadows, and smooth transitions

## Contributing

1. Follow the existing code structure and naming conventions
2. Use functional components with React hooks
3. Keep components modular and reusable
4. Add appropriate CSS classes following the BEM methodology where applicable
