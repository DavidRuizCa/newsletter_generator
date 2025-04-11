import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if OPENAI_API_KEY and OPENAI_API_KEY.startswith('sk-proj-') and len(OPENAI_API_KEY)>10:
    print("OPENAI_API_KEY looks good so far")
else:
    print("OPENAI_API_KEY is not set. Check your .env file.")

