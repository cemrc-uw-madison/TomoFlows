# TomoFlows

Project for a pipeline process with visual web feedback on tasks completed in a pipeline.

See [Design Documentation](scripts/Documentation/Design/index.md)

## Running on Docker
1. Install Docker: See [Docker Documentation](https://docs.docker.com/get-docker/)
2. Configure "Preferences > Resources > File Sharing" in Docker Desktop to include `/tmp`
2. Build Docker Image: `docker build . -t tomoflows-img`
3. Run Docker Container: `docker compose up -d` (remove -d to attach container to terminal and not run in background)
4. Open Browser and visit `http://localhost:8000`
5. Connect to container shell: `docker compose exec tomoflows bash` (OPTIONAL)
7. Stop and Remove Container: `docker compose down` (OPTIONAL)
6. Kill Container: `docker compose kill` (OPTIONAL)

## Local Developement
### Virtualenv Setup

1. Create virtual env: `python3 -m virtualenv ~/path/to/env`
2. Activate virtual env: `source ~/path/to/env/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

### Run Development Server

1. Ensure to setup and activate virtualenv and install dependencies
2. Run Django Migrations: `python3 manage.py makemigrations && python3 manage.py migrate`
3. Start Django Server: `python3 manage.py runserver`
4. Setup Frontend in New Terminal: `cd frontend && npm install`
5. Run Frontend in New Terminal: `npm run dev`
