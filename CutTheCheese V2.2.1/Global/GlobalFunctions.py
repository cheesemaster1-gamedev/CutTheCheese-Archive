from Global import GlobalVariables as GVars
from Global import GlobalVarsBackup as GVB
from AUDIO import musicVars as musVars
import random, os, time, logging, json, copy, sys, importlib.util, main, traceback
import pygame.mixer as music

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QApplication,
    QSpacerItem,
    QSizePolicy, 
    QLineEdit
)
from PySide6.QtCore import (
    Qt,
    QObject
)


def load_addons_expansions(folder='ADDONS/Expansions'):
    for filename in os.listdir(folder):
        if filename.endswith('.py') and filename != '__init__.py' and not filename.endswith('.pyc'):
            filepath = os.path.join(folder, filename)
            modulename = filename[:-3]  # Remove '.py'

            spec = importlib.util.spec_from_file_location(modulename, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(t(f"Loaded expansion: {modulename}"))
            GVars.loadedExpansions[modulename] = module

            if hasattr(module, 'addon_loader'):
                try:
                    module.addon_loader()
                    logging.debug(f"Successfully loaded module {module}")
                except Exception as e:
                    logging.exception(f"Error loading module {module}: {e}")
            else:
                logging.warning(f"Module {modulename} is not built yet")

def load_addons_extensions(folder='ADDONS/Extensions'):
    for filename in os.listdir(folder):
        if filename.endswith('.py') and filename != '__init__.py' and not filename.endswith('.pyc'):
            filepath = os.path.join(folder, filename)
            modulename = filename[:-3]  # Remove '.py'

            spec = importlib.util.spec_from_file_location(modulename, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(t(f"Loaded extension: {modulename}"))
            GVars.loadedExpansions[modulename] = module

            if hasattr(module, 'addon_loader'):
                try:
                    module.addon_loader()
                    logging.debug(f"Successfully loaded module {module}")
                except Exception as e:
                    logging.exception(f"Error loading module {module}: {e}")
            else:
                logging.warning(f"Module {modulename} is not built yet")

def load_addons_realms(folder='ADDONS/Realms'):
    for filename in os.listdir(folder):
        if filename.endswith('.py') and filename != '__init__.py' and not filename.endswith('.pyc'):
            filepath = os.path.join(folder, filename)
            modulename = filename[:-3]  # Remove '.py'

            spec = importlib.util.spec_from_file_location(modulename, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(t(f"Loaded realm: {modulename}"))
            GVars.loadedExpansions[modulename] = module

            if hasattr(module, 'addon_loader'):
                try:
                    module.addon_loader()
                    logging.debug(f"Successfully loaded module {module}")
                except Exception as e:
                    logging.exception(f"Error loading module {module}: {e}")
            else:
                logging.warning(f"Module {modulename} is not built yet")


rooms = [{'Location': 'OUTSIDE', 'Description': '', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', '7': '7 = load menu', '8': '8 = show inventory'},
        {'Location': 'CORRIDOR', 'Description': '', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory'},
        {'Location': 'KITCHEN', 'Description': '', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory'}]
menu = [{'Main Menu' : 'MENU', '0' : '0 = resume', '1' : '1 = start new', '2' : '2 = manage add-ons', '3' : '3 = Save', '4' : '4 = Tutorial'}]
letters = [':', '=', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
complete = []
playing = False
translations, cachefile, lang = {}, None, None


def print_grid(my_list, cols=3):
    for i in range(0, len(my_list), cols):
        row = my_list[i:i+cols]
        print('  '.join(str(item).ljust(10) for item in row))

def func_help(mode='main'):
    if mode == 'main':
        tprint("1 = Enter a room with a connecting door to your current room")
        tprint("2 = Open a storage box inside your current room and gain an item")
        tprint("3 = Use the item you currently have equipped")
        tprint("4 = Equip an item currently in inventory")
        tprint("5 = Store an item in your inventory inside another item of type container in your inventory")
        tprint("6 = Drop a container in your inventory into your current roomto come back and find later")
        tprint("7 = Load the main menu")
        tprint("8 = Show your current inventory and the number of each item in your inventory")

    tinput("Hit ENTER to continue...")

def t(text, targetLang=None, sourceLang='auto'):
    return text

def tinput(text):
    output = input(text)
    return output

def tprint(text):
    print(text)

def func_scroll_letters(text):
    complete.clear()
    for char in text:
        letter = letters.copy()
        if char not in letter:
            logging.error(f'could not find letter {char}')
            continue
        letter.remove(char)
        for i in range(5):
            temp = random.choice(letter)
            print((''.join(complete)) + temp)
            os.system('cls' if os.name == 'nt' else 'clear')
        complete.append(char)
        letter.append(char)
    print(text)
    text = ''

def func_smooth_scroll(lines, Spaces=5, delay=0.5):
    for _ in range(Spaces):
        print()
        sys.stdout.flush()
        time.sleep(delay)
    for _ in lines:
        print(t(_))
        sys.stdout.flush()
        time.sleep(delay)
    for _ in range(Spaces):
        print()
        sys.stdout.flush()
        time.sleep(delay)

def func_equip_iem(equip):
    if equip in GVars.inventory:
        for item in GVars.itemProperties:
            if item['Item'] == equip and item['Type'] != 'Wearable':    
                GVars.equipped = equip
                logging.info(f"Item {equip} equipped")
                if GVars.equipped not in GVars.itemCopies:
                    itemCopy = copy.deepcopy(item)
                    GVars.itemCopies.update({item['Item'] : itemCopy})
                return True
            elif item['Item'] == equip and item['Type'] == 'Wearable':
                GVars.wearing = equip
                logging.info(f"Item {equip} put on")
                return True
        else:
            logging.warning(f"No properties found for {equip}")
            return False
    elif equip not in GVars.inventory:
        print(t(f"Item '{equip}' not found in inventory..."))
        logging.debug(f"Item '{equip}' not found in inventory {GVars.inventory}")
        return False

def func_load_room(array, selection):
    for elPos, element in enumerate(array):
        #print(t(elPos, element)
        if element['Location'] == selection:
            for valPos, value in enumerate(element.values()):
                if value == selection:
                    if lang == 'en': 
                        func_scroll_letters(value)
                        print(f"Health : %{GVars.Health}")
                        print(f"equipped: [{GVars.equipped}]")
                        print(f"wearing: [{GVars.wearing}]")
                    else:
                        os.system('cls')
                        print(t(value))
                        print(t(f"Health : %{GVars.Health}"))
                        print(t(f"equipped: [{GVars.equipped}]"))
                        print(t(f"wearing: [{GVars.wearing}]"))
                else:
                    if lang != 'en':
                        print(t(value))
                    else:
                        print(value)
            break
    else:
        GVars.crashed = True
        raise KeyError(f"Ivalid room: {selection}")

def func_get_loot(storage, room, roomAttributesFunc, lootBoxesFunc):
    dropable = [d for d in GVars.dropables if d['Storage'] == storage]
    
    if not dropable:
        # Locked chest handling
        if storage == 'DECORATED CHEST' and 'Key' not in GVars.inventory:
            print(t("Requires 'Key' to open"))
            logging.debug(f"Dependency of key not met. {GVars.inventory}")
            return

        for element in lootBoxesFunc:
            if element['Storage'] == storage and element['Loot']:
                loot_list = element['Loot']
                # Cheese rarity: 0.2 vs 1.0 for others
                loot = random.choices(
                    population=loot_list,
                    weights=[0.25 if item == 'Cheese' else 1.0 for item in loot_list],
                    k=1
                )[0]

                GVars.inventory[loot] = GVars.inventory.get(loot, 0) + 1
                element['Loot'].remove(loot)
                logging.info(f"Item {loot} collected")
                if loot == 'Cheese':
                    GVars.cheeseTotal += 1 
                break

        # Remove storage from room
        for loc in roomAttributesFunc:
            if loc['Location'] == room and 'Storage' in loc and storage in loc['Storage']:
                loc['Storage'].remove(storage)
                break

        if storage == 'DECORATED CHEST' and 'Key' in GVars.inventory.keys():
            GVars.inventory['Key'] -= 1
            if GVars.inventory['Key'] <= 0:
                del GVars.inventory['Key']
            logging.info(f"Key removed from inventory")

    else:
        logging.info(f"picking up dropable {storage}")
        for room in roomAttributesFunc:
            if room['Location'] == GVars.room:
                room['Storage'].remove(storage)
        GVars.inventory[storage] = GVars.inventory.get(storage, 0) + 1

def func_load_demon_fight(enemy_Data, enemy):
    runAttack = True
    music.music.load(musVars.musBoss)
    music.music.play(loops=-1)
    
    for enem, data in GVars.enemies.items():
        if enem == enemy:
           enemyName = enem 
           enemyData = GVars.enemies[enemy]
           enemyHealth = data['Health']
           enemyDamage = data['Damage']
           break
    else:
        logging.error(f"enemy {enemy} not found")
        return
    while True: 
        func_scroll_letters(f"BATTLE: {enemyName} - Health: {enemyHealth}")
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if runAttack == True:
                print(t(f"BATTLE: {enemy}\nHealth : %{GVars.Health} - {enemyDamage*(1-GVars.resistance)}\nequipped: [{GVars.equipped}]"))
                time.sleep(1)
                GVars.Health = GVars.Health - (enemyDamage*(1-GVars.resistance))
                os.system('cls' if os.name == 'nt' else 'clear')
            print(t(f"BATTLE: {enemyName} - Enemy Health: {enemyHealth}\nHealth : %{GVars.Health}\nequipped: [{GVars.equipped}]"))
            print(t('\n0 = equip\n1 = use\n2 = menu'))
            battle = input(' ---> ')

            #equip item
            if battle == '0':
                runAttack = False
                for item, count in GVars.inventory.items():
                    print(t(f"{item} x {count}"))
                while True:
                    itemchoice = input('What Item?\n ---> ').strip().title()   
                    if itemchoice in GVars.inventory:
                        for item in GVars.itemProperties:
                            if item['Item'] == itemchoice and item['Type'] != 'Wearable':    
                                GVars.equipped = itemchoice
                                if itemchoice not in GVars.itemCopies:
                                    itemCopy = copy.deepcopy(item)
                                    GVars.itemCopies.update({itemchoice : itemCopy})
                                break
                            elif item['Item'] == itemchoice and item['Type'] == 'Wearable':
                                GVars.wearing = itemchoice
                                logging.info(f"Item {itemchoice} put on")
                                break
                    else:
                        print(t(f"Item '{itemchoice}' not in inventory...\nTry again..."))
                        continue
            #use item
            elif battle == '1':
                if GVars.equipped:
                    for item, properties in GVars.itemCopies.items():
                        if item == GVars.equipped:
                            itemType = properties['Type']
                            itemName = properties['Item']
                            itemDetails = properties
                            break

                    if itemType == 'Weapon':
                        enemyHealth = enemyHealth - int(itemDetails['Damage'])
                        enemyData['Health'] = enemyHealth
                        itemDetails['Count'] -= 1
                        runAttack = True
                    elif itemType == 'Food':
                        nHealth = GVars.Health + itemDetails['Health']
                        print(f"{nHealth} = {GVars.Health} + {itemDetails['Health']}")
                        if nHealth > GVars.maxHealth:
                            GVars.Health = GVars.maxHealth
                        else:
                            GVars.Health = nHealth
                        nHealth = 0
                        itemDetails['Count'] -= 1
                        runAttack = True
                    elif itemType == 'Effect':
                        if itemDetails['Effect'] == 'Strength':
                            GVars.maxHealth += 50
                            GVars.inventoryLen += 5
                            logging.info(f"Strength buff activated")
                            itemDetails['Count'] = itemDetails['Count'] - 1
                            if itemDetails['Count'] == 0:
                                GVars.inventory[item] -= 1
                                del GVars.itemCopies[item]
                                GVars.equipped = ''
                            logging.info(f"Item count decreased")
                        elif itemDetails['Effect'] == 'Health':
                            nHealth = GVars.Health + itemDetails['Health']
                            tprint(f"{nHealth} = {GVars.Health} + {itemDetails['Health']}")
                            if nHealth > GVars.maxHealth:
                                GVars.Health = GVars.maxHealth
                            else:
                                GVars.Health = nHealth
                            nHealth = 0
                            logging.info(f"Healed {itemDetails['Health']}")
                            itemDetails['Count'] = itemDetails['Count'] - 1
                            if itemDetails['Count'] == 0:
                                GVars.inventory[item] -= 1
                                del GVars.itemCopies[item]
                                GVars.equipped = ''
                        elif itemDetails['Effect'] == 'Damage':
                            nHealth = GVars.Health - random.randint(10, 15)
                            tprint(f"{nHealth} = {GVars.Health} - {GVars.Health - nHealth}")
                            GVars.Health = nHealth
                            logging.info(f"Took effect damage {GVars.Health - nHealth}")
                            nHealth = 0
                            itemDetails['Count'] = itemDetails['Count'] - 1
                            if itemDetails['Count'] == 0:
                                GVars.inventory[item] -= 1
                                del GVars.itemCopies[item]
                                GVars.equipped = ''
                        elif itemDetails['Effect'] == 'Resistance':
                            GVars.resistance = 0.20
                            logging.info(f"Resistance applied")
                            itemDetails['Count'] = itemDetails['Count'] - 1
                            if itemDetails['Count'] == 0:
                                GVars.inventory[item] -= 1
                                del GVars.itemCopies[item]
                                GVars.equipped = ''
                        elif itemDetails['Effect'] == 'Weakness':
                            GVars.resistance -= 0.20
                            logging.info(f"Weakness applied")
                            itemDetails['Count'] = itemDetails['Count'] - 1
                            if itemDetails['Count'] == 0:
                                GVars.inventory[item] -= 1
                                del GVars.itemCopies[item]
                                GVars.equipped = ''
                        else:
                            print(t(f"Cannot use {itemDetails['Item']} in battle..."))
                            runAttack = False
                    else:
                        print(t(f"Cannot use {itemDetails['Item']} in battle..."))
                        runAttack = False
                            
                    if itemDetails['Count'] == 0:
                        GVars.inventory[itemName] -= 1
                        del GVars.itemCopies[itemName]
                        GVars.equipped = ''
                        if GVars.inventory[itemName] == 0:
                            del GVars.inventory[itemName]
            #menu
            elif battle == '2':
                func_load_menu(None)
                runAttack = False
            #else
            else:
                print(t(f"'{battle}' is not an option..."))
                runAttack = False

            print(GVars.Health)
            print()

            if GVars.Health <= 0:
                break

            if enemyData['Health'] <= 0:
                enemyData['Defeated'] = True
                if enemyData['Drop']:
                    if enemyData['Drop'] not in GVars.inventory.keys():
                        GVars.inventory[enemyData['Drop']] = 1
                    else:
                        GVars.inventory[enemyData['Drop']] += 1
                    logging.info(f"{enemyName} dropped {enemyData['Drop']}")
                    print(f"{enemyName} dropped {enemyData['Drop']}")
                    time.sleep(1)
                GVars.ending = enemyData['Ending']
                break

            for modName, module in GVars.loadedExpansions.items():
                if hasattr(module, 'battle_conditions'):
                    module.battle_conditions()

            time.sleep(1)

def func_load_menu(choice=None):
    logging.info(f"Menu loaded")
    music.music.load(musVars.musCredits)
    music.music.play(-1)
    global playing

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(t(f"Cut The Cheese - version {main.version}"))
        for menu_index, menu_val in enumerate(menu):
            for item_index, item_val in enumerate(menu_val.values()):
                print(t(item_val))
        if choice == None:
            menuchoice = input('--> ').strip().lower()
        else:
            menuchoice = choice

        if menuchoice == '0':
            if playing == True: 
                print(t("Save current game to which slot --> "))
                for i in range(1, 4):
                    try:
                        with open(f"Saves/Save{i}.json", 'r') as f:
                            data = json.load(f)
                            name = data.get("name", "Unnamed")
                            print(t(f"{i}. {name}"))
                    except FileNotFoundError:
                        print(t(f"{i}. [Empty]"))                
                slot = input("--> ").strip()
                if slot.isdigit() and int(slot) in [1, 2, 3]:
                    func_save_to_file(slot)
                else:
                    logging.error(f"Slot {slot} not found")
                    print(t(f"Slot {slot} not found..."))
                    continue
                
            print(t("Load which slot --> "))
            for i in range(1, 4):
                try:
                    with open(f"Saves/Save{i}.json", 'r') as f:
                        data = json.load(f)
                        name = data.get("name", "Unnamed")
                        print(t(f"{i}. {name}"))
                except FileNotFoundError:
                    print(t(f"{i}. [Empty]"))
            try:
                with open(f"Saves/EmergencySave.json", 'r') as f:
                    data = json.load(f)
                    name = data.get("name", "Unnamed")
                    print(t(f"{name}. {name}"))
            except FileNotFoundError:
                print(f"Crash Save. [Empty]")
            slot = input("--> ").strip().title()
            if slot != 'Crash Save':
                func_load_game(slot)
            else:
                func_load_game(slot=8)
            time.sleep(1)
            if GVars.failed == True:
                continue
            else:
                GVars.start = True
                playing = True
                break

        elif menuchoice == '1':
            if playing == True:
                print(t("Save current game to which slot --> "))
                for i in range(1, 4):
                    try:
                        with open(f"Saves/Save{i}.json", 'r') as f:
                            data = json.load(f)
                            name = data.get("name", "Unnamed")
                            print(t(f"{i}. {name}"))
                    except FileNotFoundError:
                        print(t(f"{i}. [Empty]"))
                
                slot = input("--> ").strip()
                if slot.isdigit() and int(slot) in [1, 2, 3]:
                    func_save_to_file(slot)
                    func_reset_all_vars()
                    GVars.start = 'new'
                    playing = True
                    break
                else:
                    playing = False
                    logging.error(f"Slot {slot} not found")
                    print(t(f"Slot {slot} not found..."))
                    continue
            else:
                func_reset_all_vars()
                GVars.start = 'new'
                logging.info("New game started")
                playing = True
                break

        elif menuchoice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(t("Addons:\n"))
            for addon_category in GVars.addons:
                for category, packs in addon_category.items():
                    print(t(f"{category}:"))
                    for pack, details in packs.items():
                        if isinstance(details, dict):
                            status = details.get('Status', 'Unknown')
                            location = details.get('Location', 'N/A')
                        else:
                            status = details
                            location = 'N/A'
                        print(f" - Pack: {pack} --- Status: {status}")

            toggle = tinput("\nToggle which pack...\n---> ").strip().title()

            toggled = False
            for addon_category in GVars.addons:
                for category, packs in addon_category.items():
                    if toggle in packs:
                        details = packs[toggle]
                        if isinstance(details, dict):
                            current_status = details.get('Status', 'Off')
                            location = details.get('Location', 'Unknown')
                        else:
                            current_status = 'Off'
                            location = 'Unknown'

                        new_status = 'On' if current_status == 'Off' else 'Off'
                        packs[toggle] = {'Status': new_status, 'Location': location}

                        if category == 'Expansions':
                            if new_status == 'On':
                                if location not in GVars.addonLocations:
                                    GVars.addonLocations.append(location) if location != 'CHEESE REALM' else None
                                    GVars.expansions = True if location != 'CHEESE REALM' else None
                                    for modulename, module in GVars.loadedExpansions.items():
                                        if hasattr(module, 'func_Var_Loader') and modulename == toggle:
                                            try:
                                                module.func_Var_Loader()
                                                logging.debug(f"Successfully loaded module {module}")
                                            except Exception as e:
                                                logging.exception(f"Error loading module {modulename}: {e}")
                                        elif modulename == toggle and not hasattr(module, 'func_Var_Loader'):
                                            logging.warning(f"Module {modulename} is not built yet")
                            else:
                                if location in GVars.addonLocations:
                                    GVars.addonLocations.remove(location)
                                    if len(GVars.addonLocations) < 1:
                                        GVars.expansions = False
                                    for modulename, module in GVars.loadedExpansions.items():
                                        if hasattr(module, 'func_Var_Unloader'):
                                            try:
                                                module.func_Var_Unloader()
                                            except Exception as e:
                                                logging.exception(f"Error deleting vars from {modulename} : {e}")
                        elif category == 'Extensions':
                            if new_status == 'On':
                                for modName, module in GVars.loadedExpansions.items():
                                    if hasattr(module, 'func_Var_Loader') and modName == toggle:
                                        try:
                                            module.func_Var_Loader()
                                            logging.debug(f"Successfully loaded module {modName}")
                                        except Exception as e:
                                            logging.exception(f"Error loading module {modName}: {e}")
                                    elif modulename == toggle and not hasattr(module, 'func_Var_Loader'):
                                        logging.warning(f"Module {modName} has not been built yet")
                            else:
                                for modulename, module in GVars.loadedExpansions.items():
                                    if hasattr(module, 'func_Var_Unloader'):
                                        try:
                                            module.func_Var_Unloader()
                                        except Exception as e:
                                            logging.exception(f"Error deleting vars from {modulename} : {e}")

                        print(t(f"\nToggled '{toggle}' to {new_status}..."))
                        logging.debug(f"Toggled pack {toggle}")
                        toggled = True
                        break
                if toggled:
                    break

            if not toggled:
                print(t(f"\nAddon '{toggle}' not found."))
                logging.error(f"Addon {toggle} not ofund")

            input("\nPress Enter to continue...")
    
        elif menuchoice == '3':
            print(t("Save current game to which slot --> "))
            for i in range(1, 4):
                try:
                    with open(f"Saves/Save{i}.json", 'r') as f:
                        data = json.load(f)
                        name = data.get("name", "Unnamed")
                        print(t(f"{i}. {name}"))
                except FileNotFoundError:
                    print(t(f"{i}. [Empty]"))

            slot = input("--> ").strip()
            if slot.isdigit() and int(slot) in [1, 2, 3]:
                func_save_to_file(slot)
                playing = True
                break
            else:
                logging.error(f"Slot {slot} not found")
                print(t(f"Slot {slot} not found..."))
                continue

        elif menuchoice == '4':
            GVars.tutorialMode = True
            #func_tutorial_mode()

        else:
            print(t("Invalid menu choice..."))
            logging.error(f"Invalid menu choice {menuchoice}")
        time.sleep(1)
    
    music.music.fadeout(2000)
    music.music.load(musVars.musPeaceful)
    music.music.play(-1, fade_ms=2000)    

def func_save_to_file(filename=f"", slot=None, name='', confirm=False):    
    if os.path.exists(filename):
        if confirm == 'Y':
            logging.debug(f"Game attempting to save to {filename}")
        else:
            logging.debug("Save cancelled")
            return
    
    expansions = {}
    special = {}

    for modname, module in GVars.loadedExpansions.items():
        if hasattr(module, 'specialVars'):
            special[f'{modname}-specialVars'] = module.specialVars
        if hasattr(module, 'expansions'):
            special[f'{modname}-expansions'] = module.expansions

    for modName, module in GVars.loadedExpansions.items():
        if hasattr(module, 'roomAttributes') and hasattr(module, 'lootBoxes'):
            expansions[f'{modName}-roomAttributes'] = module.roomAttributes
            expansions[f'{modName}-lootBoxes'] = module.lootBoxes
    
    data = {
        "name" : name,
        "inventory" : GVars.inventory,
        "inventoryLen" : GVars.inventoryLen,
        "equipped" : GVars.equipped,
        "health" : GVars.Health,
        "maxHealth" : GVars.maxHealth,
        "resistance" : GVars.resistance,
        "expansion" : GVars.expansions,
        "realm" : GVars.realm,
        "vehicleVariants" : GVars.vehicleVariants,
        "addons" : GVars.addons,
        "addonLocations" : GVars.addonLocations,
        "Enemies" : GVars.enemies,
        "dropables" : GVars.dropables,
        "cheeseTolerance" : GVars.cheeseTolerance,
        "itemCopies" : GVars.itemCopies,
        "craftables" : GVars.craftables,
        "cheeseTotal" : GVars.cheeseTotal,
        "totalCheeseCount" : GVars.totalCheeseCount,
        "darkRooms" : GVars.darkRooms,

        "roomAttributes" : main.roomAttributes,
        "lootBoxes" : main.lootBoxes,
        "itemProperties" : GVars.itemProperties,

        "room" : GVars.room,
        "expansionLoc" : GVars.expansionLoc,

        "expansions" : expansions,
        "special" : special
    }

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        logging.debug(f"Game saved to {filename}")
        print(f"Game saved to slot {slot}...")
    except Exception as e:
        logging.exception(f"Save failed: {e}")
        print("Save failed...")

def func_load_game(slot):
    if slot != 4 and slot != 8:
        filename = f"Saves/Save{slot}.json"
    elif slot == 4:
        filename = "Saves/Tutorial.json"
    elif slot == 8:
        filename = "Saves/EmergencySave.json"

    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        GVars.inventory = data["inventory"]
        GVars.inventoryLen = data["inventoryLen"]
        GVars.equipped = data["equipped"]
        GVars.Health = data["health"]
        GVars.maxHealth = data["maxHealth"]
        GVars.expansions = data["expansion"]
        GVars.realm = data["realm"]
        GVars.vehicleVariants = data["vehicleVariants"]
        GVars.addons = data["addons"]
        GVars.addonLocations = data["addonLocations"]
        GVars.enemies = data["Enemies"]
        GVars.dropables = data["dropables"]
        GVars.cheeseTolerance = data["cheeseTolerance"]
        GVars.resistance = data["resistance"]
        GVars.cheeseTotal = data["cheeseTotal"]
        GVars.totalCheeseCount = data["totalCheeseCount"]
        GVars.darkRooms = data["darkRooms"]

        main.roomAttributes = data["roomAttributes"]
        main.lootBoxes = data["lootBoxes"]
        GVars.itemProperties = data["itemProperties"]
        GVars.itemCopies = data["itemCopies"]
        GVars.craftables = data["craftables"]

        GVars.room = data["room"]
        GVars.expansionLoc = data["expansionLoc"]

        expansionsData = data.get("expansions", {})
        for modName, module in GVars.loadedExpansions.items():
            for data_type, value in expansionsData.items():
                if data_type.startswith(f'{modName}-'):
                    data_type = data_type[len(modName):].lstrip("-")
                    if data_type == 'roomAttributes' and hasattr(module, 'roomAttributes'):
                        module.roomAttributes = value
                    elif data_type == 'lootBoxes' and hasattr(module, 'lootBoxes'):
                        module.lootBoxes = value

        specialData = data.get('special', {})
        for modname, module in GVars.loadedExpansions.items():
            for data_type, value in specialData.items():
                if data_type.startswith(f'{modname}-'):
                    data_type = data_type[len(modname):].lstrip('-')
                    if data_type == 'specialVars' and hasattr(module, 'specialVars'):
                        module.specialVars = value
                    if data_type == 'expansions' and hasattr(module, 'expansions'):
                        module.expansions = value


        logging.debug(f"game loaded from {filename}")
        print(t(f"Game loaded from slot {slot}"))
        GVars.failed = False
    except Exception as e:
        logging.exception(f"load failed: {e}")
        print(t("load failed..."))
        GVars.failed = True

def func_reset_all_vars():
    main.cssSelected = main.cssMain
    
    GVars.ending = ''
    GVars.gameEnd = False
    GVars.totalCheeseCount = 3
    GVars.cheeseTotal = 0
    GVars.room = 'OUTSIDE'
    GVars.expansionLoc = 'HOUSE'

    GVars.resistance = 0
    GVars.inventory = GVB.inventory
    GVars.inventoryLen = GVB.inventoryLen
    GVars.equipped = GVB.equipped
    GVars.Health = GVB.maxHealth
    GVars.maxHealth = GVB.maxHealth
    GVars.enemies = GVB.enemies
    GVars.dropables = GVB.dropables
    GVars.cheeseTolerance = GVB.cheeseTolerance
    GVars.itemCopies = {}
    GVars.cheeseTolerance = 0
    GVars.resistance = GVB.resistance
    GVars.darkRooms = GVB.darkRooms

    main.roomAttributes = GVB.roomAttributes
    main.lootBoxes = GVB.lootBoxes
    GVars.itemProperties = GVB.itemProperties
    GVars.craftables = GVB.craftables
    GVars.cheeseTotal = GVB.cheeseTotal
    GVars.totalCheeseCount = GVB.totalCheeseCount
    
    for modName, module in GVars.loadedExpansions.items():
        if hasattr(module, 'roomAttributes') and hasattr(module, 'roomAttributesBackup'):
            module.roomAttributes = module.roomAttributesBackup
        if hasattr(module, 'lootBoxes') and hasattr(module, 'lootBoxesBackup'):
            module.lootBoxes = module.lootBoxesBackup
        if hasattr(module, 'reset_module_vars'):
            module.reset_module_vars()
