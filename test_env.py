from dotenv import load_dotenv
import os

load_dotenv()
print("ENCRYPTION_KEY =", os.getenv("ENCRYPTION_KEY"))
