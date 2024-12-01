# PJM - Project Manager

PJM is a **project management platform** with real-time **group chat** capabilities. Designed for teams to collaborate efficiently, manage projects, and communicate seamlessly.

## Features

### 🔑 Key Features
- **Real-Time Group Chat**: Connect with team members instantly using WebSockets.
- **Project Management**: Create, assign, and track project progress.
- **User Authentication**: Secure login and registration for users.
- **Role Management**: Assign roles like Admin, Manager, and Member.
- **Activity Logs**: Track project and chat room activities.
- **Responsive Design**: Optimized for both desktop and mobile.

### 🚀 Advanced Features
- **Multiple Chat Rooms**: Collaborate in dedicated project-based chat rooms.
- **Persistent Messaging**: Messages stored for future reference.
- **Custom Notifications**: Get alerts for new messages and project updates.

## Tech Stack

- **Backend**: Django, Django Channels
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)
- **WebSocket Backend**: Daphne
- **Authentication**: Django's built-in authentication system + JWT for APIs

## Installation

### Prerequisites
- Python 3.9+
- Node.js (for additional frontend dependencies, if applicable)
- Redis (optional, for scalable WebSocket backend)

### Steps to Set Up

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/PJM.git
   cd PJM
