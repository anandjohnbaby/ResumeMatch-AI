import re

def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()
    return skill