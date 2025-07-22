from agents.extensions.models.litellm_model import LitellmModel
import os, dotenv

dotenv.load_dotenv()

model = LitellmModel(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)