# Web Compilation Service

This project is a web-based service for compiling and executing code. It's designed to function as a backend for online coding platforms, competitive programming websites, or any application requiring automated code evaluation.

## Features

*   **Code Compilation & Execution:** Supports compiling and running code in various languages(python,cpp).
*   **User Registration:** Allows users to register and manage their accounts.
*   **Submission Handling:** Manages code submissions and tracks their status.
*   **Test Case Management:** Provides a system for managing test cases for problems.
*   **Asynchronous Task Processing:** Uses Celery and Redis to handle code compilation and execution asynchronously, preventing requests from timing out.

## Tech Stack

*   **Backend:** Python, Django
*   **Asynchronous Tasks:** Celery
*   **Message Broker:** Redis
*   **Web Server:** Nginx
*   **Containerization:** Docker, Docker Compose

## Project Structure

The project is containerized using Docker and consists of the following services:

*   `web`: The main Django application.
*   `celery`: The Celery worker for asynchronous task processing.
*   `redis`: The Redis message broker.
*   `nginx`: The Nginx web server.

## Getting Started

To get the project up and running, you'll need to have Docker and Docker Compose installed.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/web_compilaton_service.git
    ```

2.  **Build and run the containers:**

    ```bash
    docker-compose up --build
    ```

This will start all the services, and the web application will be accessible at `http://localhost:8000`.

## Screenshots

![Screenshot](images/screenshot.png)