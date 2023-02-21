# TomoFlows

## Virtualenv Setup

1. Create virtual env: `python3 -m virtualenv ~/path/to/env`
2. Activate virtual env: `source ~/path/to/env/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

## Run Development Server

1. Ensure to setup and activate virtualenv and install dependencies
2. Run Django Migrations: `python3 manage.py makemigrations && python3 manage.py migrate`
3. Start Django Server: `python3 manage.py runserver`
4. Setup Frontend in New Terminal: `cd frontend && npm install`
5. Run Frontend in New Terminal: `npm run dev`
