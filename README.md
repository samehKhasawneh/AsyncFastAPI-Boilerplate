# AsyncFastAPI-Boilerplate

An async API template built with FastAPI, featuring asynchronous database connections, JWT authentication, and modular architecture for high-performance, scalable applications. This boilerplate provides a strong starting point for real-time apps with modern async features and best practices.

## Features
- **Asynchronous FastAPI** for handling high-traffic, concurrent requests.
- **JWT Authentication** for secure, stateless user management.
- **Structured Project Layout** for scalable development.
- **Async Database Connections** to avoid blocking I/O tasks.
- **Built-in CRUD Operations** for quick data management.

## Getting Started

### Prerequisites
- **Python** 3.10+ (Recommended: 3.12)
- **Docker** (optional)
- **Poetry** for dependency management
- **PostgreSQL** (local or via Docker Compose)


### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/samehKhasawneh/AsyncFastAPI-Boilerplate.git
   cd AsyncFastAPI-Boilerplate
   ```
2. **Environment Setup:**
   - Copy the `.env.development` file in the root directory.
   - Set environment variables such as `ACCESS_SECRET_KEY`, `REFRESH_SECRET_KEY`, and database connection details.
   - Generate secure keys for tokens:
     ```bash
     openssl rand -hex 32
     ```
3. **Install Dependencies:**
   ```bash
   poetry install
   ```

### Usage
  Start the FastAPI server:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```
Access the interactive API docs at http://localhost:8000/docs.

### Project Structure
  ```bash
  AsyncFastAPI-Boilerplate/
  ├── app/
  │   ├── api/                    # API routes
  │   ├── core/                   # Config, logging, security
  │   ├── crud/                   # CRUD operations
  │   ├── db/                     # Database setup
  │   ├── models/                 # SQLAlchemy models
  │   ├── schemas/                # Pydantic schemas
  │   └── main.py                 # FastAPI app entry
  ├── Dockerfile
  ├── docker-compose.yml
  └── Makefile                    # Build, run, test commands
  ```
   
### Core Features
1. JWT Authentication: Secure token-based access for users.
2. Modular API Routing: Organized by version and endpoint for easy scalability.
3. Async CRUD Operations: Base CRUD for all models with async support.
4. Middleware: CORS

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

### License
This project is licensed under the MIT License.


This `README.md` provides a solid overview, setup instructions, core features, and structure of your project. Let me know if you’d like more details added in any specific section!


- http://localhost:8000/docs

- make up

- make down

- make generate-migrations message="Add new migration"

- make apply-migrations

- make downgrade-migrations

- make seed-initial-data
