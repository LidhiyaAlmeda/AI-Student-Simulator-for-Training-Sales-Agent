import random

MALE_NAMES = [
    "Rahul",
    "Arjun",
    "Karthik",
    "Aditya",
    "Vikram",
    "Rohan"
]

FEMALE_NAMES = [
    "Aisha",
    "Priya",
    "Ananya",
    "Meera"
]

def generate_student():
    if random.choice([True, False]):
        name = random.choice(MALE_NAMES)
        gender = "male"
    else:
        name = random.choice(FEMALE_NAMES)
        gender = "female"

    return {
        "name": name,
        "gender": gender
    }