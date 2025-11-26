from gamedata.importdata import extract_table_json
from gamedata.spellcost import SpecificSpell, calc_things, CastType
from gamedata.character import Character

def print_calculated_values(calcs: dict, spell: SpecificSpell, character: Character, levels: range) -> None:
    print(spell.name + f" | {spell.casting_cost(character.skills[spell.base.school]):.2f} magika", end ='   ')
    print(f"(D: ({spell.duration[0]}, {spell.duration[1]}))/{spell.duration[2]} lvls", end= ', ')
    print(f"(C: ({spell.chance[0]}, {spell.chance[1]}))/{spell.chance[2]} lvls", end= ', ')
    print(f"(M: ({spell.magnitude[0]} - {spell.magnitude[1]}) + ({spell.magnitude[2]} - {spell.magnitude[3]})/{spell.magnitude[4]} lvls)")

    for _ in range(14):
        print("-", end="")
    for _ in levels:
        print("---------", end='')
    print()

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
        for d in data:
            print(f"{(d):6.2f}", end=" | ")

    print()
    for _ in range(14):
        print("-", end="")
    for _ in levels:
        print("---------", end='')
    print()    

def main():
    spell_data = extract_table_json()
    specific_spells: list[SpecificSpell] = []
    for base_spell in spell_data.values():
        for i in range(5):
            this_spell = SpecificSpell(base_spell, CastType.TOUCH)
            if base_spell.has_duration:
                this_spell.duration = (1, i, 1)
            if base_spell.has_chance:
                this_spell.chance = (1, i, 1)
            if base_spell.has_magnitude:
                this_spell.magnitude = (1, 1, i, i, 1)
            specific_spells.append(this_spell)

    character = Character("C:\\Users\\Benji\\AppData\\LocalLow\\Daggerfall Workshop\\Daggerfall Unity\\Saves\\SAVE49\\SaveData.txt")
    levels = range(25)
    for i in levels:
        print(i)
    for spell in specific_spells:
        test = calc_things(spell, character, levels)
        print_calculated_values(test, spell, character, levels)
        print()

if __name__ == "__main__":
    main()
