#!C:\Python36\python.exe
import sys
 
sys.path.append('d:/webapps/flask_dash/')
 
from app import create_app
from app.config import base_config

app = create_app(config=base_config)
# app.run()