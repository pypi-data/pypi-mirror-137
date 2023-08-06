import json
import re

import requests
from bs4 import BeautifulSoup
from pympler.asizeof import asizeof


def get_wfcd_api():
    wfcd_api = requests.get(
        "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/All.json").json()

    wfcd_api_parsed = {}

    for item in wfcd_api:
        wfcd_api_parsed[item['name']] = item
        if 'components' in wfcd_api_parsed[item['name']]:
            component_dict = {}
            for component in wfcd_api_parsed[item['name']]['components']:
                component_dict[component['name']] = component

            wfcd_api_parsed[item['name']]['components'] = component_dict

    return json.loads(json.dumps(wfcd_api_parsed))


def fix_name(item_name):
    if len(item_name.split()) > 3:
        if item_name.split(" ")[2] == "Systems" \
                or item_name.split(" ")[2] == "Chassis" \
                or item_name.split(" ")[2] == "Neuroptics" \
                or item_name.split(" ")[2] == "Harness" \
                or item_name.split(" ")[2] == "Wings":
            item_name = item_name.rsplit(' ', 1)[0]

    return item_name


# Get price information
def price_info(item_name, price_data):
    if item_name in price_data:
        return int(price_data[item_name][0]['avg_price'])
    else:
        return 0


# Get ducat information
def ducat_info(item_name, wfcd_api):
    set_name = get_set_name(item_name)
    part_name = get_part_name(item_name)

    try:
        ducat_data = wfcd_api[set_name]['components'][part_name]['primeSellingPrice']
    except KeyError:
        ducat_data = "N/A"
    return ducat_data


# Get vaulted status
def vaulted_info(item_name, wfcd_api):
    if item_name in wfcd_api:
        if 'vaulted' in wfcd_api[item_name]:
            return wfcd_api[item_name]['vaulted']

    return False


# Get category info
def category_info(item_name, wfcd_api):
    try:
        category = wfcd_api[item_name]['category']
    except KeyError:
        category = "N/A"

    return category


# Get required item counts
def required_info(item_name, wfcd_api):
    set_name = item_name.split("Prime", 1)[0] + "Prime"
    part_name = item_name.split("Prime ", 1)[1]

    if set_name == "Kavasa Prime":
        part_name = set_name + " " + part_name
        set_name = set_name + " Kubrow Collar"
        if "Blueprint" in part_name:
            part_name = "Blueprint"

    try:
        required = wfcd_api[set_name]['components'][part_name]['itemCount']
    except KeyError:
        required = "N/A"

    return required


def build_relic_list():
    url = 'https://n8k6e2y6.ssl.hwcdn.net/repos/hnfvc0o3jnfvc873njb03enrf56.html'

    source = requests.get(url).text

    soup = BeautifulSoup(source, 'lxml')

    tables = soup.find_all('tr',
                           string=re.compile("Relic .Intact|Relic .Exceptional|Relic .Flawless|Relic .Radiant"))

    relic_list = {}

    for table in tables:
        items = table.find_all_next("tr", limit=6)

        relic = table.find("th").contents[0].split("Relic")[0].rstrip()
        refinement = table.find("th").contents[0].split("(")[1][0:-1].rstrip()

        x = {'drops': {}}
        for item in items:
            item_contents = item.find_all("td")

            item_name = item_contents[0].contents[0]
            item_chance = round(float(item_contents[1].contents[0].split("(")[1][0:-2]) / 100, 3)

            if refinement == "Intact":
                if item_chance == 0.253:
                    tier = "Common"
                    tier_id = 0
                elif item_chance == 0.11:
                    tier = "Uncommon"
                    tier_id = 1
                elif item_chance == 0.02:
                    tier = "Rare"
                    tier_id = 2
            elif refinement == "Exceptional":
                if item_chance == 0.233:
                    tier = "Common"
                    tier_id = 0
                elif item_chance == 0.13:
                    tier = "Uncommon"
                    tier_id = 1
                elif item_chance == 0.04:
                    tier = "Rare"
                    tier_id = 2
            elif refinement == "Flawless":
                if item_chance == 0.2:
                    tier = "Common"
                    tier_id = 0
                elif item_chance == 0.17:
                    tier = "Uncommon"
                    tier_id = 1
                elif item_chance == 0.06:
                    tier = "Rare"
                    tier_id = 2
            elif refinement == "Radiant":
                if item_chance == 0.167:
                    tier = "Common"
                    tier_id = 0
                elif item_chance == 0.2:
                    tier = "Uncommon"
                    tier_id = 1
                elif item_chance == 0.1:
                    tier = "Rare"
                    tier_id = 2

            x['drops'][item_name] = {'chance': item_chance, 'tier': tier, 'tier_id': tier_id}

        relic_drops = dict(sorted(x.items(), key=lambda x: x[1]))

        if relic not in relic_list:
            relic_list[relic] = {}

        relic_list[relic][refinement] = relic_drops

    for i in range(0, 5):
        relic_list.popitem()

    return relic_list


PAlist = {
    "prime access": {
        "Ash": "Carrier,Vectis",
        "Atlas": "Dethcube,Tekko",
        "Banshee": "Euphona,Helios",
        "Chroma": "Gram,Rubico",
        "Ember": "Sicarus,Glaive",
        "Equinox": "Stradavar,Tipedo",
        "Frost": "Latron,Reaper",
        "Gara": "Astilla,Volnus",
        "Hydroid": "Ballistica,Nami Skyla",
        "Inaros": "Karyst,Panthera",
        "Ivara": "Baza,Aksomati",
        "Limbo": "Destreza,Pyrana",
        "Loki": "Bo,Wyrm",
        "Mag": "Boar,Dakra",
        "Mesa": "Akjagara,Redeemer",
        "Mirage": "Akbolto,Kogake",
        "Nekros": "Galatine,Tigris",
        "Nezha": "Guandao,Zakti",
        "Nidus": "Magnus,Strun",
        "Nova": "Soma,Vasto",
        "Nyx": "Hikou,Scindo",
        "Oberon": "Sybaris,Silva & Aegis",
        "Octavia": "Pandero,Tenora",
        "Rhino": "Ankyros,Boltor",
        "Saryn": "Nikana,Spira",
        "Titania": "Corinth,Pangolin",
        "Trinity": "Kavasa,Dual Kamas",
        "Valkyr": "Cernos,Venka",
        "Vauban": "Akstiletto,Fragor",
        "Volt": "Odonata",
        "Wukong": "Ninkondi,Zhuge",
        "Zephyr": "Kronen,Tiberon"
    }
}


def access_info(set):
    PA = "N/A"
    if set.split("Prime")[0].rstrip() in PAlist['prime access']:
        PA = set.split("Prime")[0].rstrip()
    else:
        for frame in PAlist['prime access']:
            if set.split("Prime")[0].rstrip() in PAlist['prime access'][frame].split(","):
                PA = frame
    return PA


def build_set_data(relic_list):
    # List of prime parts
    part_list = []

    # List of prime sets
    set_list = []

    wfcd_api = get_wfcd_api()

    for relic in relic_list:
        for reward in relic_list[relic]['Intact']['drops']:
            set_name = reward.split("Prime", 1)[0] + "Prime"

            if reward != "Forma Blueprint":
                if reward not in part_list:
                    part_list.append(reward)

                if [set_name] not in set_list and set_name != "Kavasa Prime":
                    set_list.append([set_name])

    set_list.append(["Kavasa Prime Kubrow Collar"])

    # Sorts part_list and set_list alphabetically
    part_list = sorted(part_list)
    set_list.sort(key=lambda x: x[0])

    set_data = {}

    for i in range(len(set_list)):
        for j in range(len(part_list)):
            if set_list[i][0].split()[0] == part_list[j].split()[0]:
                set_list[i].append(part_list[j])

    price_data = get_price_data()

    for i, _ps in enumerate(set_list):
        parts = {'parts': {}}

        for j, _p in enumerate(_ps[1:]):
            parts['parts'][_p] = {'plat': price_info(fix_name(_p), price_data),
                                  'ducats': ducat_info(fix_name(_p), wfcd_api),
                                  'required': required_info(fix_name(_p), wfcd_api)}

        set_data[_ps[0]] = parts
        set_data[_ps[0]]['vaulted'] = vaulted_info(_ps[0], wfcd_api)
        set_data[_ps[0]]['type'] = category_info(_ps[0], wfcd_api)
        set_data[_ps[0]]['plat'] = price_info(_ps[0] + " Set", price_data)
        set_data[_ps[0]]['prime-access'] = access_info(_ps[0])

    return set_data


def get_set_name(item_name):
    if "Kavasa" not in item_name:
        return item_name.split("Prime", 1)[0] + "Prime"
    else:
        return "Kavasa Prime Kubrow Collar"


def get_part_name(item_name):
    if "Kavasa" not in item_name:
        return item_name.split(" Prime ", 1)[1]
    elif "Blueprint" in item_name:
        return "Blueprint"
    else:
        return item_name


def calculate_average(relic, style, modifier, drops):
    chance_left = 1
    chance_used = 1
    average_return = 0

    relic_rewards = []

    for drop in relic['drops']:
        relic_rewards.append([drop, relic['drops'][drop]['price']])

    relic_rewards.sort(key=lambda x: x[1], reverse=True)

    for i in range(len(relic_rewards)):
        item_name = relic_rewards[i][0]

        chance = relic['drops'][item_name]['chance']
        price = relic['drops'][item_name]['price']

        adj_chance = 1 - (chance / chance_left)

        actual_chance = adj_chance ** modifier

        item_chance = 1 - actual_chance

        item_chance = chance_used * item_chance

        chance_left = chance_left - chance

        chance_used = chance_used * actual_chance

        adj_price = price * item_chance

        relic['drops'][item_name]['calculated_chance'][style] = item_chance * drops

        relic['drops'][item_name]['calculated_price'][style] = adj_price * drops

        average_return += adj_price * drops

    relic['average_return'][style] = round(average_return, 0)

    return relic


def get_average_return(relic):
    solo = 0
    for drop in relic['drops']:
        solo += relic['drops'][drop]['price'] * relic['drops'][drop]['chance']

    solo = solo
    one_by_one = solo * 4

    relic['average_return']['solo'] = round(solo, 0)
    relic['average_return']['1b1'] = round(one_by_one, 0)

    relic = calculate_average(relic, "2b2", 2, 2)
    relic = calculate_average(relic, "3b3", 3, (4 / 3))
    relic = calculate_average(relic, "4b4", 4, 1)

    return relic


never_vaulted = ['Lith C7', 'Meso N11', 'Neo V9', 'Axi S8', 'Axi V10']


def build_relic_data(relic_data, set_data):
    for relic in relic_data:
        for refinement in relic_data[relic]:
            vaulted = False
            for part in relic_data[relic][refinement]['drops']:
                if "Forma" not in part:
                    if not vaulted and set_data[get_set_name(part)]['vaulted']:
                        vaulted = True

                    relic_data[relic][refinement]['drops'][part]['price'] = \
                        set_data[get_set_name(part)]['parts'][part]['plat']

                    relic_data[relic][refinement]['drops'][part]['ducats'] = \
                        set_data[get_set_name(part)]['parts'][part]['ducats']
                else:
                    relic_data[relic][refinement]['drops'][part]['price'] = 0
                    relic_data[relic][refinement]['drops'][part]['ducats'] = 0

                relic_data[relic][refinement]['drops'][part]['calculated_chance'] = \
                    {"solo": relic_data[relic][refinement]['drops'][part]['chance'],
                     "1b1": relic_data[relic][refinement]['drops'][part]['chance'] * 4}

                relic_data[relic][refinement]['drops'][part]['calculated_price'] = \
                    {"solo": relic_data[relic][refinement]['drops'][part]['price'] *
                             relic_data[relic][refinement]['drops'][part]['chance'],
                     "1b1": relic_data[relic][refinement]['drops'][part]['price'] *
                            relic_data[relic][refinement]['drops'][part]['chance'] * 4}

            relic_data[relic][refinement]['vaulted'] = vaulted if relic not in never_vaulted else False
            relic_data[relic][refinement]['average_return'] = {}
            relic_data[relic][refinement] = get_average_return(relic_data[relic][refinement])

    return relic_data


def build_json_files():
    relic_list = build_relic_list()
    set_data = build_set_data(relic_list)
    relic_data = build_relic_data(relic_list, set_data)

    return json.loads(json.dumps(relic_data)), json.loads(json.dumps(set_data))


def get_price_data():
    soup = BeautifulSoup(requests.get('http://23.95.43.245/history/').text, 'html.parser')
    return requests.get(sorted(['http://23.95.43.245/history/' + node.get('href')
                                for node in soup.find_all('a') if node.get('href').endswith('json')])[-1]).json()