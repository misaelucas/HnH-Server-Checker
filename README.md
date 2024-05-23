# Haven and Hearth Server Tracker

A comprehensive solution to track the status of the Haven and Hearth game server. This project includes a Python backend to monitor the server and a React frontend to display the data interactively. It's being deployed in render, you can check it. 

here's a script for deployment:

```

services:
  - type: web
    name: backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python server_checker.py
    plan: free
    path: backend

  - type: static
    name: frontend
    buildCommand: npm install && npm run build
    publishPath: build
    plan: free
    path: frontend




## Backend

The backend checks the Haven and Hearth server status periodically and logs crashes. It serves the data through a REST API. You can also test stuff with flask/mocked data. 

### Features

- ⏲️ Monitors server status every 60 seconds
- 📊 Logs crash count and timestamps
- 🌐 Provides crash data via an HTTP server

### Technologies

- 🐍 Python
- 🌐 Flask
- 🎵 Pygame (for audio notifications)
- 🔄 Threading
- 🌍 HTTP Server

### Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

2. **Run the server checker:**
   ```bash
    python server_checker.py


## Frontend

The frontend is a React application built with Vite. It fetches and displays crash data from the backend.

### Features

-  📈 Displays server crash data
-  🔍 Filters data by month and year
-  📊 Visualizes data with Chart.js

### Technologies

-  ⚛️ React
-  🚀 Vite
-  📊 Chart.js
-  📡 Axios


