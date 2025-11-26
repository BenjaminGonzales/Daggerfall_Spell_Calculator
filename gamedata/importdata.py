from bs4 import BeautifulSoup
import json
from .spellcost import BaseSpell

def map_to_int(s):
    s = s.strip()
    if s.isnumeric():
        return int(s)
    return 0

def extract_table_html():
    spell_dict: dict[str, BaseSpell] = {}
    # this presupposes the wiki html is in the working directory
    with open("spell_data.html", encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        tables = soup.find_all('table', limit=2)
        data_sheet = tables[1]
        body = data_sheet.tbody
        
        current_effect = ''
        current_sub_effect = ''
        current_school = ''
        effect_size = 0
        for row in body.find_all('tr')[2:]:
            current_spell: BaseSpell = BaseSpell()

            header_text = []
            datum_text  = []
            for headers in row.find_all('th'):
                header_text.append(headers.get_text(strip=True))
            for data in row.find_all('td'):
                datum_text.append(data.get_text())

            if 'colspan' in row.th.attrs:
                current_effect = header_text[0]
                current_sub_effect = ''
                current_school = datum_text[0]
                effect_size = 0
            elif 'rowspan' in row.th.attrs:
                current_effect = header_text[0]
                current_sub_effect = header_text[1]
                current_school = datum_text[0]
                effect_size = map_to_int(row.th['rowspan']) - 1
            else:
                current_sub_effect = header_text[0]
                effect_size = max(effect_size - 1, 0)

            current_spell.effect = current_effect
            current_spell.sub_effect = current_sub_effect
            current_spell.school = current_school
            
            nums_list = [map_to_int(s) for s in datum_text[-6:]]
            current_spell.duration_cost_factor  = tuple(nums_list[0:2])
            current_spell.chance_cost_factor    = tuple(nums_list[2:4])
            current_spell.magnitude_cost_factor = tuple(nums_list[4:6])
            spell_dict[f"{current_spell.effect} {current_spell.sub_effect}"] = current_spell
        fp.close()
    return spell_dict

def base_spell_decoder(obj):
    required = {
        'effect', 'sub_effect', 'school', 'premium',
        'duration_cost_factor', 'chance_cost_factor',
        'magnitude_cost_factor'
        }
    if required.issubset(obj):
        return BaseSpell(
            obj['effect'],
            obj['sub_effect'],
            obj['school'],
            obj['premium'],
            tuple(obj['duration_cost_factor']),
            tuple(obj['chance_cost_factor']),
            tuple(obj['magnitude_cost_factor']),
        )
    else:
        return obj

def extract_table_json():
    with open("./gamedata/spell_data.json", "r") as fp:
        return json.load(fp, object_hook=base_spell_decoder)

if __name__ == "__main__":
    spell_data = {}
    try:
        spell_data = extract_table_json()
    except FileNotFoundError:
        print("JSON file for spell data not found in working directory")
    try:
        extract_table_html()
    except FileNotFoundError:
        print("Wiki page file for spell data not found in working directory")
    print(spell_data)