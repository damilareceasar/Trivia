from dotenv import load_dotenv
import os


load_dotenv()
my_user=os.environ.get("user")
my_password = os.environ.get("password")
my_name = os.environ.get("database")