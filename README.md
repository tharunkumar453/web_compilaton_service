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

## Architecture d<img width="1117" height="565" alt="Untitled-2026-04-01-2225" src="https://github.com/user-attachments/assets/0c797861-93e0-4e97-8f81-b499c923a572" />
iagram


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
    git clone https://github.com/tharunkumar453/web_compilaton_service.git
    ```

2.  **Build and run the containers:**

    ```bash
    docker-compose up --build
    ```

This will start all the services, and the web application will be accessible at `http://localhost:8000`.
# Screenshorts
## Admin Dashboard
![admin](https://github.com/user-attachments/assets/d1cddd93-47f9-4933-80fe-35e372d50f01)

## User Registration via Postman API
![add_user](https://github.com/user-attachments/assets/81c88bde-1c79-4c1c-9a7d-c85dadd1a473)

## User login via Postman API
![log_in](https://github.com/user-attachments/assets/8264b480-a93e-47fc-ac7a-7f6efdcbd10b)
## Submit a code file via Postman API
![submit](https://github.com/user-attachments/assets/981cbc4a-4dd1-4acc-bfb7-a102bb936d2f)
## Leader Board
![leader](https://github.com/user-attachments/assets/6329cd98-87bb-4f6f-a07b-8f076bd69dde)
# Azure VM
![vm](https://github.com/user-attachments/assets/e0de8368-b3ae-4c14-a8fe-bb8a60ff678c)
## Containers in VM
![containers](https://github.com/user-attachments/assets/c4ee170c-e7ee-407e-93aa-6d3d1ef13f5c)

