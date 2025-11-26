from gamedata.importdata import extract_table_json
from gamedata.spellcost import SpecificSpell, calc_things, CastType
from gamedata.character import Character

def print_calculated_values(calcs, spell,levels):
    print(spell.name)
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    print("Level       ", end = " | ")
    for i in levels:
        print(f"{i + 1:6}", end=" | ")

    for title, data in calcs.items():

        print()    
        print("-------------",end="+")
        for _ in levels:
            print("--------", end="+")
        print()

        print(f"{title:12}", end = " | ")
        for i in levels:
            print(f"{(data[i]) / 5:6.2f}", end=" | ")
            
    print()
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

def main():
    spell_data = extract_table_json()
    specific_spells: list[SpecificSpell] = []
    for name, base_spell in spell_data.items():
        this_spell = SpecificSpell(base_spell, CastType.TOUCH)
        if base_spell.has_duration:
            this_spell.duration = (1, 1, 2)
        if base_spell.has_chance:
            this_spell.chance = (1, 1, 2)
        if base_spell.has_magnitude:
            this_spell.magnitude = (1, 1, 1, 1, 2)
        specific_spells.append(this_spell)

    character = Character("C:\\Users\\Benji\\AppData\\LocalLow\\Daggerfall Workshop\\Daggerfall Unity\\Saves\\SAVE49\\SaveData.txt")
    levels = range(20)
    for spell in specific_spells:
        test = calc_things(spell, character, levels)
        print_calculated_values(test, spell, levels)
        print()

if __name__ == "__main__":
    main()
