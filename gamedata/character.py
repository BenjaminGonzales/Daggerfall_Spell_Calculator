from dataclasses import dataclass
import json

@dataclass
class Skills:
    Medical: int
    Etiquette: int
    Streetwise: int
    Jumping: int
    Orcish: int
    Harpy: int
    Giantish: int
    Dragonish: int
    Nymph: int
    Daedric: int
    Spriggan: int
    Centaurian: int
    Impish: int
    Lockpicking: int
    Mercantile: int
    Pickpocket: int
    Stealth: int
    Swimming: int
    Climbing: int
    Backstabbing: int
    Dodging: int
    Running: int
    Destruction: int
    Restoration: int
    Illusion: int
    Alteration: int
    Thaumaturgy: int
    Mysticism: int
    ShortBlade: int
    LongBlade: int
    HandToHand: int
    Axe: int
    BluntWeapon: int
    Archery: int
    CriticalStrike: int

class Stats:
    strength: int
    intelligence: int
    willpower: int
    agility:  int
    endurance: int
    personality: int
    speed: int
    luck: int

class Character:
    def __init__(self, filepath: str):
        with open(filepath, "r") as fp:
            file_stats = {}
            file_skills = {}
            level = 1
            try:
                savedata = json.load(fp)
                playerentity = savedata['playerData']['playerEntity']
                file_stats = playerentity['stats']
                file_skills = playerentity['skills']
                level = playerentity['level']
            except:
                print("error reading save file for character data")
            fp.close()
            
        self.stats  = file_stats
        self.skills = file_skills
        self.level  = level
    stats:  dict[str, int]
    skills: dict[str, int]
    level:  int
