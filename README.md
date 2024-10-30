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
   - Set environment variables such as `ACCESS_SECRET_KEY`, `REFRESH_SECRET_KEY`, and database connection details.
   - Generate secure keys for tokens:
     ```bash
     openssl rand -hex 32
     ```
   - For other environments like production create the following file:
      `.env.production` copy its content from `.env.development` or `.env.$ENV.example`

### Use Makefile to build the app and run the migrations **(Recommended)**
   Skip points 3-5 if you're planning to use Makefile
   - `make up` # build and start the application and lastly apply the migrations
   - `make down` # turn off the application
   - `make generate-migrations message="Add new migration"` # generate migrations when creating new model
   - `make apply-migrations` # apply generated migrations
   - `make downgrade-migrations` # rollback migration changes
   - `make seed-initial-data` # seed initial data into DB

3. **Install Dependencies:**
   *Manual*
   - Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   - Use Poetry to install dependencies
   ```bash
   poetry install
   ```
   
   *Using Docker and docker-compose*
   ```bash
   docker compose build
   ```
4. **Applying migrations**
   Using scripts/start.sh
   ```bash
   cd scripts && ./start.sh 1
   ```
5. **Running the Application**
   - Start the FastAPI server:
   *Manual*
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --reload
   ```
   *Using Docker Compose*
   ```bash
   docker compose up
   # or with -d if you skipped the build step above
   ```

**Access the interactive API docs at http://localhost:8000/docs.**

### Project Structure
  ```bash
  AsyncFastAPI-Boilerplate/
  ├── app/
  │   ├── api/                    # Versioned API structure, API routes and API shared dependencies
  │   ├── core/                   # Config, logging, security
  │   ├── crud/                   # CRUD operations (Base CRUD class)
  │   ├── db/                     # Database setup (DB Session)
  │   ├── models/                 # SQLAlchemy models
  │   ├── schemas/                # Pydantic schemas
  │   ├── services/               # Service interface it could be ElasticSearch or in this case Async HTTP client
  │   ├── tests/                  # Testing directory
  │   ├── utils/                  # Helper utilities
  │   ├── logs/                   # Stores application logs
  │   └── main.py                 # FastAPI app entry
  |── scripts/                    # Helper scripts for app management
  |── alembic/                    # Database migrations
  ├── Dockerfile
  ├── docker-compose.yml
  ├── pyproject.toml              # Handles dependency management with Poetry
  └── Makefile                    # Build, run commands
  ```
   
### Core Features
1. JWT Authentication: Secure token-based access for users.
2. Modular API Routing: Organized by version and endpoint for easy scalability.
3. Async CRUD Operations: Base CRUD for all models with async support.
4. Async Database and Session Managementand DB pooling
5. Middleware: CORS

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

### License
This project is licensed under the MIT License.


This `README.md` provides a solid overview, setup instructions, core features, and structure of your project. Let me know if you’d like more details added in any specific section!
