from gamedata.importdata import extract_table_json
from gamedata.spellcost import SpecificSpell, calc_things, CastType
from gamedata.character import Character
from tkinter import *
from tkinter import ttk
from gui.gui import dsc_gui

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

def alternative_calc():
    spell_data = extract_table_json()
    spell_to_test = spell_data['Damage Health']
    character = Character("SaveData.txt")
    calcs: dict[SpecificSpell, dict] = {}
    spell_variants = [[]]
    levels = range(5, 15)
    for i in range(1, 3):
        for j in range(1, 8):
            spell = SpecificSpell(spell_to_test, CastType.SINGLE, magnitude=(2, 2, j, j, 1))
            calcs[spell] = calc_things(spell, character, levels)
    
    for spell, calc in calcs.items():
        print_calculated_values(calc, spell, character, levels)

def main_gui():
    spells = extract_table_json()
    spell_titles = list(spells.keys())
    app = dsc_gui()
    app.set_spells(spell_titles)
    app.start_gui()

if __name__ == "__main__":
    main_gui()
