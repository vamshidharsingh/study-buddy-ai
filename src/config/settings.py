import os 
from dotenv import load_dotenv


load_dotenv()

#storing our class config

class Settings():

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL_NAME = "llama-3.1-8b-instant"
   #CREATIVITY LEVEL SINICE IT MAKING QUESTIONS  WE GIVE ..9
    TEMPERATURE = 0.9
    
    # MAX RETRIES NO OF RETRIES FOR API 
    MAX_RETRIES = 3

settings = Settings()
    

