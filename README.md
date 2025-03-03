# Intelligent Database Query Agent

## Overview
This project implements an intelligent query agent that dynamically routes user queries to the most relevant database using a graph-based execution model. The project utilizes **LangChain**, **LangGraph**, and **PostgreSQL** to execute queries in a structured and efficient manner.

The system is designed to:
- Classify user queries and identify the relevant database.
- Route queries to the appropriate agent for execution.
- Return structured responses based on the query results.

## Tech Stack
- **Python**: Core programming language.
- **LangChain**: Framework for developing LLM-based applications.
- **LangGraph**: For building graph-based execution flows.
- **PostgreSQL**: Database system for storing financial data.
- **Docker**: Containerization of database instances.
- **Rye**: Python build tool and package manager.

## Installation and Setup

### 1. Install Rye (Build Tool)
Ensure **Rye** is installed on your system:
```sh
sudo yum install postgresql-devel
curl -sSf https://rye.astral.sh/get | bash
```

### 2. Clone the Repository
```sh
git clone https://github.com/commitbyrajat/reporting_agent.git
cd reporting_agent
```

### 3. Install Dependencies
Activate the Rye environment and install dependencies:
```sh
rye sync
```

### 4. Set Up Environment Variables
Create a `.env` file with the required configurations:
```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
OPENAI_API_KEY=your_openai_key
```

### 5. Start the Database Services (via Docker-Compose)
This project requires three PostgreSQL instances:
- **Transaction DB** (Port: 5432)
- **Master Data DB** (Port: 5433)
- **User Management DB** (Port: 5431)

Run the following command to start them:
```sh
docker-compose up -d
```
This will create and start three PostgreSQL containers with pre-configured schemas.

### 6. Run the Application
Start the query agent:
```sh
python graph.py
```

## Project Structure
```
📂 project_root
├── graph.py           # Defines the execution graph and query workflow
├── nodes.py           # Implements nodes for executing queries against databases
├── chain.py           # Handles query classification and database selection
├── schema.py          # Defines schema for response structure
├── agent.py           # Creates agents for different databases
├── db.py              # Database connections and LLM initialization
├── .env               # Environment variables (ignored in Git)
├── docker-compose.yml # Docker configuration for PostgreSQL instances
```

## Code Workflow
1. **User Query Input:**
   - `graph.py` starts by accepting a user query.
   - The query is passed to `first_responder`, which uses **LangChain** to classify the query.
2. **Database Selection:**
   - `chain.py` determines which database is most relevant based on predefined rules.
   - `schema.py` ensures a structured classification of the database.
3. **Query Execution:**
   - The selected agent from `agent.py` handles the query execution.
   - The query is executed on PostgreSQL using `db.py` and retrieved via **LangChain** tools.
4. **Response Generation:**
   - Results are aggregated and formatted before being returned to the user.

## Docker-Compose Configuration
```yaml
services:
  transaction:
    container_name: transaction
    image: postgres:latest
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PW}
      - POSTGRES_DB=${POSTGRES_DB_1}  # Specify default database
    ports:
      - "5432:5432"
    restart: always
    volumes:
      - transaction_data:/var/lib/postgresql/data  # Persistent volume for DB storage
      - ./sql/transaction:/docker-entrypoint-initdb.d  # Initialize DB on first run

  usermanagement:
    container_name: usermanagement
    image: postgres:latest
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PW}
      - POSTGRES_DB=${POSTGRES_DB_2}  # Specify default database
    ports:
      - "5431:5432"
    restart: always
    volumes:
      - usermanagement_data:/var/lib/postgresql/data  # Persistent volume for DB storage
      - ./sql/user_management:/docker-entrypoint-initdb.d  # Initialize DB on first run

  masterdata:
    container_name: masterdata
    image: postgres:latest
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PW}
      - POSTGRES_DB=${POSTGRES_DB_3}  # Specify default database
    ports:
      - "5433:5432"
    restart: always
    volumes:
      - master_data:/var/lib/postgresql/data  # Persistent volume for DB storage
      - ./sql/master_data:/docker-entrypoint-initdb.d  # Initialize DB on first run


  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_MAIL}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PW}
    ports:
      - "5050:80"
    restart: always
    volumes:
      - pgadmin_data:/var/lib/pgadmin  # Persistent volume for PGAdmin
      - ./servers.json:/pgadmin4/servers.json
      - ./pgpass:/pgpass

volumes:
  transaction_data:
    driver: local
  usermanagement_data:
    driver: local
  master_data:
    driver: local
  pgadmin_data:
    driver: local
```

## Packages Used
- **LangChain**: Used for natural language processing and query execution.
- **LangGraph**: Used to define and manage the execution flow of the query system.
- **Pydantic**: Used for structured query classification.
- **SQLAlchemy**: For database connectivity.
- **Dotenv**: To load environment variables securely.
- **OpenAI**: As the LLM provider for processing queries.

## Running Tests
To run unit tests:
```sh
pytest tests/
```

## Future Enhancements
- Implement a frontend UI for user interaction.
- Integrate additional databases for broader query support.
- Improve LLM fine-tuning for better query classification.

---
**Contributions:** PRs are welcome! Follow the issue tracker for feature requests and bug fixes.

