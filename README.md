# Flask App

This is a flask API project template using python3 and Flask. Run the following commands to get started.

```sh
cd flask-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The `install -r requirements.txt` command will automatically install the required dependencies. To start the dev server:

```sh
/your/path/to/flask-app/venv/bin/python3 /your/path/to/flask-app/main.py
```

If it is your first time running the app (or you want to reset the application), you will need to seed the database. To do this, open a new terminal and run the following command:

```sh
/your/path/to/flask-app/venv/bin/python3 /your/path/to/flask-app/seed_db.py
```

Then open http://localhost:4000 with your browser to see the result.

# biov-backend

To see the database, go request http://localhost:4000/api/seed_db from your browser.

The default credentials for non-admin users are:
username: [a,b,c]
password: [a,b,c]

The default credentials for admin users are:
username: [d,e,f]
password: [d,e,f]
