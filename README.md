# Auction App


## Requirements
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)


## Run the Application
-  **Development mode**:
  `docker compose up`

- **Production mode**:
    `docker compose -f docker-compose.yml up --build -d`

  
## Environment Variables

Before running the project, you need to create a `.env` file at the same level as `.env.example`.  
Use `.env.example` as a template and fill in the required variables.

```bash
cp .env.example .env

