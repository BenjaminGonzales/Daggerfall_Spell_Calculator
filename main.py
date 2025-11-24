from gamedata.import_data import extract_table
from gamedata.spellcost import SpecificSpell, BaseSpell, CastType

def damage_calc_continuous(duration, magnitude, mana):
    dur, dlvl = duration
    mag, mlvl = magnitude

    lvl_range = range(20)
    durations = [1 + dur * ((i + 1) // dlvl) for i in lvl_range]
    magnitudes = [1 + mag * ((i + 1) // mlvl) for i in lvl_range]


    print(f"spell of 1 + {mag} per {mlvl} level(s) for 1 + {dur} per {dlvl} level(s) rounds casting {mana} mana")
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    print("Level       ", end = " | ")
    for i in lvl_range:
        print(f"{i + 1:6}", end=" | ")

    print()    
    print("-------------",end="+")
    for _ in lvl_range:
        print("--------", end="+")
    print()

    print("Duration    ", end = " | ")
    for i in lvl_range:
        print(f"{durations[i]:6}", end=" | ")

    print()    
    print("-------------",end="+")
    for _ in lvl_range:
        print("--------", end="+")
    print()

    print("Dmg/Instance", end = " | ")
    for i in lvl_range:
        print(f"{magnitudes[i]:6}", end=" | ")


    print()    
    print("-------------",end="+")
    for _ in lvl_range:
        print("--------", end="+")
    print()

    print("real time   ", end = " | ")
    for i in lvl_range:
        print(f"{(durations[i] * 5):6}", end=" | ")

    print()    
    print("-------------",end="+")
    for _ in lvl_range:
        print("--------", end="+")
    print()

    print("dps         ", end = " | ")
    for i in lvl_range:
        print(f"{(magnitudes[i]) / 5:6.2f}", end=" | ")

    print()    
    print("-------------",end="+")
    for _ in lvl_range:
        print("--------", end="+")
    print()

    print("total damage", end = " | ")
    for i in lvl_range:
        print(f"{magnitudes[i] * durations[i]:6}", end=" | ")


    print()    
    print("-------------",end="+")
    for _ in lvl_range:
        print("--------", end="+")
    print()

    print("damage/mana ", end = " | ")
    for i in lvl_range:
        print(f"{(magnitudes[i] * durations[i]) / mana:6.2f}", end=" | ")
    print()
    
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


def print_calculated_values(calcs):
    for title, data in calcs:
        pass

def main():
    spell_data = extract_table()
    specific_spells: list[SpecificSpell] = []
    for name, base_spell in spell_data.items():
        this_spell = SpecificSpell(base_spell, CastType.TOUCH)
        if base_spell.has_duration:
            this_spell.duration = (1, 1, 2)
        if base_spell.has_chance:
            this_spell.chance = (1, 1, 2)
        if base_spell.has_magnitude:
            this_spell.magnitude = (1, 1, 2)
        specific_spells.append(this_spell)

    for spell in specific_spells:
        print(f"{spell.name} has a cost of {spell.cost_raw} with everything at 1 with level @ 2")
        print()

if __name__ == "__main__":
    main()
