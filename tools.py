import random

def roll_dice(sides: int = 20) -> int:
    """Return a random integer between 1 and `sides` (inclusive)."""
    return random.randint(1, sides)

def generate_event() -> str:
    """Return a random mystical event string."""
    events = [
        "A strange mist envelops the street, muting all sound.",
        "A raven caws loudly, startling a nearby passerby.",
        "An old clock chimes thirteen times, unnervingly.",
        "Whispers of an ancient curse fill the air around you.",
        "A flicker of ghostly light dances in the corner of your eye.",
    ]
    return random.choice(events)
