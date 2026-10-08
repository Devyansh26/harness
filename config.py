import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
base_url = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("deployment_name")
api_version = os.getenv("AZURE_API_VERSION")