Create a virtual environment:
```
python -m venv venv
```

Activate the virtual environment of Bash:
```
source venv/Scripts/activate
```

Activate the virtual environment of PowerShell:
```
.\venv\Scripts\activate
```

Install requirements:
```
pip install -r requirements.txt
```

Create an .env file that contains the following:
```
DB=mongodb://x.x.x.x:27017/
GOOGLE_CLIENT_ID=client_id
GOOGLE_CLIENT_SECRET=secret
GOOGLE_REDIRECT_URI=http://localhost:8000/google/auth
```

Run FastAPI:
```
fastapi dev app.py
```
