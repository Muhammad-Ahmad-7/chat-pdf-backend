from dotenv import load_dotenv
load_dotenv()
import os

JWT_SECRET = os.getenv('JWT_SECRET')
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
PRIVATE_ROUTES=['/pdf/*', '/user/*']