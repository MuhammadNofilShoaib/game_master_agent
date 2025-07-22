"""Mystical Detective Game Master orchestration – NO hosted tools passed to model."""

import random
from agents import Runner, set_tracing_disabled
import chainlit as cl
from dotenv import load_dotenv

from model_loader import model
from tools import roll_dice, generate_event
from game_agents.narrator_agent import NarratorAgent
from game_agents.suspect_agent import SuspectAgent
from game_agents.clue_agent import ClueAgent

load_dotenv()
set_tracing_disabled(True)

# Keywords for interrogation or investigation
KEYWORDS_INTERROGATE = [
    "suspect", "interrogate", "question", "accuse", "investigate", "search", "clue", "evidence",
    "witness", "detective", "mystery"
]

# Words indicating a successful interrogation or clue discovery
SUCCESS_WORDS = ["revealed", "discovered", "confessed", "found", "secret", "clue", "artifact"]

def needs_interrogation(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in KEYWORDS_INTERROGATE)

def interrogation_success(text: str) -> bool:
    return any(w in text.lower() for w in SUCCESS_WORDS)

@cl.on_chat_start
async def on_start():
    await cl.Message(content="""
👋 **Welcome, Detective!** 🕵️‍♂️

🔎 You are investigating a series of magical crimes in a mysterious city.
Type an action to begin, e.g.:
• *Investigate the alley*
• *Interrogate the suspicious witness*
• *Search the ancient library*

Let the mystery unfold! 🧙‍♀️
""").send()

@cl.on_message
async def handle_turn(msg: cl.Message):
    user_input = msg.content.strip()

    # 1️⃣ Narration
    narr_out = await Runner.run(NarratorAgent, input=user_input)
    story = narr_out.final_output.strip()

    if len(story.split()) < 5:
        story += " " + generate_event()

    parts = [f"📖 **Narration:**\n{story}"]

    # 2️⃣ Optional interrogation
    if needs_interrogation(user_input) or needs_interrogation(story):
        # Simulate dice locally
        dice_roll = roll_dice()
        interrogation_prompt = f"Detective rolled {dice_roll} during interrogation."
        suspect_out = await Runner.run(SuspectAgent, input=interrogation_prompt)
        suspect_text = suspect_out.final_output.strip()
        parts.append(f"🕵️‍♂️ **Interrogation:**\n{suspect_text}")

        # 3️⃣ Clues if interrogation succeeds
        if interrogation_success(suspect_text):
            clue_out = await Runner.run(ClueAgent, input="reveal clue")
            parts.append(f"🗝️ **Clue Found:**\n{clue_out.final_output.strip()}")

    parts.append("🔁 *Your move?* (investigate / interrogate / examine / follow / etc.)")

    await cl.Message(content="\n\n".join(parts)).send()
