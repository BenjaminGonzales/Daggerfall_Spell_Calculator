from dataclasses import dataclass
from enum import Enum

CastType = Enum('CastType', [('SELF', 1), ('TOUCH', 1), ('SINGLE', 1.5), ('AREA', 2), ('AREA_RANGE', 2.5)])

@dataclass
class BaseSpell:
    effect: str = ''
    sub_effect: str = ''
    school: str = ''
    premium: int = 0
    duration_cost_factor: tuple[int, int] | None = None
    chance_cost_factor: tuple[int, int] | None = None
    magnitude_cost_factor: tuple[int, int] | None = None

    @property
    def has_duration(self) -> bool:
        return self.duration_cost_factor != (0,0)
    @property
    def has_chance(self) -> bool:
        return self.chance_cost_factor != (0, 0)
    @property
    def has_magnitude(self) -> bool:
        return self.magnitude_cost_factor != (0,0)   

    def __repr__(self):
        return f"{self.effect} ({self.sub_effect}) from the {self.school} school. COSTS:(dur: {self.duration_cost_factor}, chan: {self.chance_cost_factor}, mag: {self.magnitude_cost_factor}"
    
@dataclass
class SpecificSpell:
    base: BaseSpell
    cast_type: CastType
    element: str | None = None
    duration: tuple[(int, int, int)] | None = None
    chance: tuple[(int, int, int)] | None = None
    magnitude: tuple[(int, int), (int, int), int] | None = None

    @property
    def cost_raw(self) -> float:
        cost: float = self.base.premium
        if self.duration is not None:
            cost += cost_of_property(self.duration, self.base.duration_cost_factor)
        if self.chance is not None:
            cost += cost_of_property(self.chance, self.base.chance_cost_factor)
        if self.magnitude is not None:
            cost += cost_of_property(self.magnitude, self.base.magnitude_cost_factor)
        return cost * self.cast_type.value * 4 # raw costs are stored at lowest common den values (4)
    
    @property
    def name(self) -> str:
        if self.base.sub_effect == '' or self.base.sub_effect == 'Normal':
            return self.base.effect
        else:
            return f"{self.base.effect} {self.base.sub_effect}"

def cost_of_property(cost_factor, base_cost_factor) -> float:
    cost:float = 0
    base, scaling, per_lvl = cost_factor
    base_cost, scaling_cost = base_cost_factor
    cost += base * base_cost
    cost += (scaling // per_lvl) * scaling_cost
    return cost

def calc_damage(spell: SpecificSpell, mana_cost) -> dict[str, list[int | float]]:
    levels = range(20)
    base_damage, per_lvl_dmg, lvl_jumps = spell.magnitude
    damage_values = [base_damage + per_lvl_dmg * (level//lvl_jumps) for level in levels]
    damage_per_mana = [damage / mana_cost for damage in damage_values]
    return {
        "damage_values" : damage_values, 
        "damage_per_mana" : damage_per_mana
        }

def calc_chance(chance, mana_cost) -> dict[str, list[float]]:
    return {}

