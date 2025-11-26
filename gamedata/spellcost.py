from dataclasses import dataclass
from gamedata.character import Character
from enum import Enum

CastType = Enum('CastType', [('SELF', 1), ('TOUCH', 1), ('SINGLE', 1.5), ('AREA', 2), ('AREA_RANGE', 2.5)])

@dataclass
class BaseSpell:
    effect: str = ''
    sub_effect: str = ''
    school: str = ''
    premium: int = 0
    duration_cost_factor: tuple[int, int]  = (0, 0)
    chance_cost_factor: tuple[int, int]    = (0, 0)
    magnitude_cost_factor: tuple[int, int] = (0, 0)

    @property
    def has_duration(self) -> bool:
        return self.duration_cost_factor  != (0, 0)
    @property
    def has_chance(self) -> bool:
        return self.chance_cost_factor    != (0, 0)
    @property
    def has_magnitude(self) -> bool:
        return self.magnitude_cost_factor != (0, 0)
    
@dataclass
class SpecificSpell:
    base: BaseSpell
    cast_type: CastType
    element: str | None = None
    duration:  tuple[(int, int, int)]             = (0, 0, 0)
    chance:    tuple[(int, int, int)]             = (0, 0, 0)
    magnitude: tuple[(int, int), (int, int), int] = (0, 0, 0, 0, 0)

    @property
    def cost_raw(self) -> float:
        cost: float = self.base.premium
        if self.base.has_duration:
            cost += cost_of_property_raw(self.duration,  self.base.duration_cost_factor)
        if self.base.has_chance:
            cost += cost_of_property_raw(self.chance,    self.base.chance_cost_factor)
        if self.base.has_magnitude:
            cost += cost_of_mag_raw(self.magnitude, self.base.magnitude_cost_factor)
        return cost * self.cast_type.value * 4 # raw costs are stored at lowest common den values (4)
        
    @property
    def name(self) -> str:
        if self.base.sub_effect == '' or self.base.sub_effect == 'Normal':
            return self.base.effect
        else:
            return f"{self.base.effect} {self.base.sub_effect}".strip()
   
    def casting_cost(self, character_skill):
        return (0.275 - 0.0025 * character_skill) * self.cost_raw
    

def cost_of_property_raw(cost_factor, base_cost_factor) -> float:
    cost:float = 0
    base, scaling, per_lvl = cost_factor
    base_cost, scaling_cost = base_cost_factor
    cost += base * base_cost
    cost += (scaling // per_lvl) * scaling_cost
    return cost

def cost_of_mag_raw(cost_factor, base_cost_factor) -> float:
    cost:float = 0
    base_low, base_high, scaling_low, scaling_high, per_lvl = cost_factor
    base_cost, scaling_cost = base_cost_factor
    cost += ((base_low + base_high) / 2) * base_cost
    cost += (((scaling_low + scaling_high) / 2) // per_lvl) * scaling_cost
    return cost

def calc_things(spell: SpecificSpell, character: Character, levels: range) -> dict[str, int | float]:
    calcs = {}
    magnitudes = []
    chances    = []
    durations  = []
    manacost = spell.casting_cost(character.skills[spell.base.school])
    attr_str = 'magnitude'

    if spell.base.has_magnitude:    
        mlow, mhigh, mslow, mshigh, perlvl = spell.magnitude
        avg = (mlow + mhigh) // 2
        savg = (mslow + mshigh) // 2

        magnitudes = [avg + (savg * ((level + 1)// perlvl))  for level in levels]
        calcs[attr_str] = magnitudes
    
    if spell.base.has_chance:
        base, scale, perlvl = spell.chance
        chances    = [base + (scale * ((level + 1) // perlvl)) for level in levels]
        calcs['chance'] = chances      

    if spell.base.has_duration:
        base, scale, perlvl = spell.duration
        durations  = [base + (scale * ((level + 1) // perlvl)) for level in levels]
        calcs['duration'] = durations

    if spell.base.has_duration and spell.base.has_magnitude:
        attr_per_mana = [attr / manacost for attr in magnitudes]
        calcs[attr_str + '/mana'] = attr_per_mana
    return calcs
