from sys import argv, exit
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
    QObject, 
    QTimer
)
import time, json, random, logging, sys, string, inspect, main
import pygame.mixer as music

from Global import (
    GlobalVariables as GVars,
    GlobalFunctions as GFuncs
)
from RESOURCES import (
    Languages_handler as lang
)
from AUDIO import musicVars as musVars


temp_widgets = ['roomsList', 'storageList', 'invList', 'helpList', 'itemsList', 'equipList', 'storeWidget', 'dropList', 'dropWidget', 'load_widget', 'toggle_widget', 'addon_widget', 'instructions', 'craftWidget']  # Add more as needed
tutorial = ["Welcome to 'Cut The Cheese' tutorial mode! let's begin...\nTo enter a room, press 1 (the button) then type the name of the room you want to enterand hit ENTER...", 
            "Good job!\nNow to open a loot container, press 2 (the button) then type the name of the container you want to open and hit ENTER...", 
            "Great!\n, To equip an item press 4 (the button) then type the name of the item and hit ENTER, do not enter the x(count) though...\nEquip a food item...", 
            "Awesome!\nNow to use that item, press 3 (the button)...\nMost item types have a unique action associated with them, like a sword for cutting/slashing, food for healing, and potions for effects with other items doing other things as well",
            "Perfect!\nNow to store an item in a handheld container, press 5 (the button) then enter the name of what you want to store and what in when prompted, hit ENTER after each input that isn't clicking a button...",
            "Excellent!\nFinally, to drop a container, press 6 (the button). Then enter the item you want to drop and hit ENTER...\nThis only works with dropable items such as the box or sack",
            "Well done! You've completed the tutorial mode!\nYou can now explore the house and beyond, collecting items, crafting, and facing challenges.\nRemember, you can always access the help menu by pressing 9 (the button) if you need assistance.\nGood luck on your adventure in 'Cut The Cheese'!"]
tip = 0

prevroom, module = None, None

credits = ['Cheese Master 1 - Lead developer', 'Chuck B - Lead sound designer', 'Ethan Molyneux - Beta tester', "Tech - Thanks for the Slipper", "Special thanks to the developers at OpenAI for the online chatbot ChatGPT for it's assistance in debugging as well as the developers behind SUNO for it's assistance in developing sound tracks"]
hallOfCheese = []
DBLeaderboard = {'1':'[empty]', '2':'[empty]', '3':'[empty]'}


class Tutorial_UI(QWidget):
    global tip

    def __init__(self, app_window=None):
        super().__init__()
        
        self.setWindowTitle("CutTCheese2 - Tutorial")
        self.setStyleSheet(main.cssMain)
        self.setMinimumSize(720, 640)
        self.page = QVBoxLayout()
        self.setLayout(self.page)

        self.rooms = [{'Location': 'OUTSIDE', 'Description': 'You stand in a quiet yard, the air crisp and fresh. The mailbox creaks gently in the breeze, leaves rustle softly beneath your feet, and distant birdsong fills the morning. The cracked pathway leads your eyes toward the old house, promising stories waiting inside.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', '7': '7 = load menu', '9': '9 = help'},
                {'Location': 'CORRIDOR', 'Description': 'A dimly lit corridor stretches ahead, its scuffed wooden floor whispering secrets of countless footsteps. Doors to other rooms flank each side, some slightly ajar, revealing glimpses of shadowed interiors. The faint smell of aged wood mingles with dust in the air.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '9': '9 = help'},
                {'Location': 'KITCHEN', 'Description': 'The kitchen is cluttered and cozy, filled with forgotten utensils hanging on rusty hooks and mismatched plates stacked high. The fridge hums steadily in the corner, its glow casting eerie shadows over cracked countertops. The scent of stale coffee lingers faintly.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '9': '9 = help'}]
        self.roomAttributes = [{'Location' : 'OUTSIDE', 'Doors' : ['KITCHEN', 'CORRIDOR'], 'Storage' : ['MAILBOX']},
                        {'Location' : 'CORRIDOR', 'Doors' : ['KITCHEN', 'OUTSIDE'], 'Storage' : ['CABINET']},
                        {'Location' : 'KITCHEN', 'Doors' : ['CORRIDOR', 'OUTSIDE'], 'Storage' : ['CABINET','FRIDGE']}]
        self.lootBoxes = [{'Storage' : 'DECORATED CHEST', 'Loot' : ['Soul Orb']},
                    {'Storage' : 'CHEST', 'Loot' : ['Sword', 'Potion', 'Sack', 'Revolver', 'Key', 'Belt']},
                    {'Storage' : 'MAILBOX', 'Loot' : ['Box']},
                    {'Storage' : 'FRIDGE', 'Loot' : ['Cheese', 'Apple']},
                    {'Storage' : 'CABINET', 'Loot' : ['Cheese', 'Slingshot', 'Water Bottle', 'Ham', 'Bread', 'Recipe']},
                    {'Storage' : 'WAR CHEST', 'Loot' : ['Cannon']},
                    {'Storage' : 'TENT', 'Loot' : ['Stick']}]

        self.app_window = app_window

        self.tip = 0
        self.initialisation(self.page)

    def initialisation(self, layout):
        global tip

        if self.tip == 1:
            tip += 1
            self.tip = 0

        if tip == 7:
            self.open_menu()
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clearLayout(item.layout())
        
        self.column_widget = QWidget()
        self.columns = QHBoxLayout(self.column_widget)
        self.content_Widget = QWidget()
        self.content = QVBoxLayout(self.content_Widget)
        self.columns.addWidget(self.content_Widget)

        self.Location = QLabel(GVars.room)
        self.Location.setStyleSheet('font-weight: bold;' \
        'font-size: 16px;')
        self.page.addWidget(self.Location)
        self.reveal_room_name_effect(GVars.room)
        time.sleep(float(len(GVars.room)*2*0.04))
        self.Location.setContentsMargins(0, 0, 0, 0)
        self.page.setContentsMargins(0, 0, 0, 0)
        self.page.setSpacing(0)
        self.Location.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.stats_Widget = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_Widget)
        self.Health = QLabel(f"Health: %{GVars.Health}")
        self.Health.setStyleSheet('font-weight: bold;')
        self.Health.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Equipped = QLabel(f"Equipped: [{GVars.equipped}]")
        self.Equipped.setStyleSheet('font-weight: bold;')
        self.Equipped.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Wearing = QLabel(f"Wearing: [{GVars.wearing}]")
        self.Wearing.setStyleSheet('font-weight: bold;')
        self.Wearing.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        if GVars.room.endswith(' PORTAL'):
            for modname, module in GVars.loadedExpansions.items():
                if hasattr(module, 'realm'):
                    module.realm(GVars.room, self)
        else:
            self.options = next(loc for loc in self.rooms if loc['Location'] == GVars.room)

        describe = next((loc.get('Description' ,'') for loc in self.rooms if loc['Location'] == GVars.room), '')
        self.Description = QLabel(describe)
        self.Description.setWordWrap(True)
        self.Description.setSizePolicy(QLabel.sizePolicy(self.Description).horizontalPolicy(), QLabel.sizePolicy(self.Description).verticalPolicy())
        self.Description.setMinimumWidth(600)
        self.Description.setMinimumHeight(80)
        self.Description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Description.setContentsMargins(0, 0, 0, 0)

        tutor = tutorial[tip]
        self.Tutorial = QLabel(tutor)
        self.Tutorial.setWordWrap(True)
        self.Tutorial.setSizePolicy(QLabel.sizePolicy(self.Tutorial).horizontalPolicy(), QLabel.sizePolicy(self.Tutorial).verticalPolicy())
        self.Tutorial.setMinimumWidth(600)
        self.Tutorial.setMinimumHeight(80)
        self.Tutorial.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Tutorial.setContentsMargins(0, 0, 0, 0)
        if tip == 6:
            QTimer.singleShot(10000, lambda: self.open_menu())

        self.stats_layout.setContentsMargins(4, 4, 4, 4)
        self.stats_layout.setSpacing(4)

        self.stats_layout.addWidget(self.Health, alignment=Qt.AlignLeft)
        self.stats_layout.addWidget(self.Equipped, alignment=Qt.AlignLeft)
        self.stats_layout.addWidget(self.Wearing, alignment=Qt.AlignLeft)
        self.stats_layout.addWidget(self.Description, alignment=Qt.AlignLeft)
        self.stats_layout.addWidget(self.Tutorial, alignment=Qt.AlignLeft)
     
        self.page.addWidget(self.stats_Widget)
        self.page.addWidget(self.column_widget)

        self.button_options = []

        self.otherOption = QLineEdit()
        self.otherOption.setStyleSheet(main.cssMain)
        self.content.addWidget(self.otherOption, alignment=Qt.AlignLeft)
        self.otherOption.returnPressed.connect(lambda: self.handle_runtime(choice=self.otherOption.text().strip().title()))

        for key, option in self.options.items():
            if key != 'Location' and key != 'Description':
                self.option = QPushButton(option)
                self.option.setStyleSheet(main.cssMain)
                self.option.setFixedWidth(128)
                self.content.addWidget(self.option, alignment=Qt.AlignLeft)
                self.option.clicked.connect(lambda checked, btn=self.option, k=key, o=option: self.handle_option_click(k, o, btn))
                self.button_options.append(self.option)

        self.spacerOption = QWidget()
        self.content.addWidget(self.spacerOption, stretch=1)

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.columns.addItem(self.spacer)

        self.inv_widget = QWidget()
        self.inv_widget.setObjectName('inv_widget')
        self.inv_layout = QVBoxLayout(self.inv_widget)
        self.inv_widget.setStyleSheet("""
            QWidget#inv_widget {
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 4px;
            }
        """)
        self.inv_title = QLabel('Inventory: ')
        self.inv_title.setStyleSheet('font-weight: bold;')
        self.inv_layout.addWidget(self.inv_title, alignment=Qt.AlignLeft)
        for item, count in GVars.inventory.items():
            self.inv_label = QLabel(f"{item} x {count}")
            self.inv_layout.addWidget(self.inv_label, alignment=Qt.AlignLeft)
        self.spacer = QWidget()
        self.inv_layout.addWidget(self.spacer, stretch=1)
        self.columns.addWidget(self.inv_widget, alignment=Qt.AlignRight)

    def handle_option_click(self, key=0, option='', button=None):            
        self.cancel_action()
        
        # Reset all buttons: enable and set normal style
        for btn in self.button_options:
            btn.setEnabled(True)
            btn.setStyleSheet(main.cssMain)  # normal style

        # Disable all buttons
        for btn in self.button_options:
            btn.setEnabled(False)

        # Highlight the clicked button and keep it disabled
        button.setEnabled(False)
        button.setStyleSheet('background-color: #ffa600')  # clicked style

        if key != 'menu':
            key = int(key)
            if 0 <= key < 10:
                logging.info(f"Key: {key}, Option: {option}")
                self.handle_runtime(choice=key)
            elif key >= 10:
                logging.debug(f"accessing an add-on's option listing: {key}, {option}")
                for modname, module in GVars.loadedExpansions.items():
                    matching_mod = next(
                        ({name: mods[name]} for addon in GVars.addons 
                        for top, mods in addon.items() 
                        for name in mods if name == modname),
                        None
                    )
                    if matching_mod:
                        inner_mod = next(iter(matching_mod.values()))  # gets the {...} dict
                        if inner_mod.get('Status') == 'On' and hasattr(module, 'handle_module_options'):
                            module.handle_module_options(action=key, self=self, layout=self.columns)
            elif not key:
                logging.debug(f"text input {option}")
            else:
                logging.error(f"somehow invalid: {key}, {option}")
        else:
            self.handle_runtime(choice=7)

    def handle_runtime(self, choice):
        global tip
        #wait
        if choice == 0:
            QTimer.singleShot(1000, lambda: None)
            self.end_of_turn()
            self.cancel_action()
        #enter room
        elif choice == 1:
            self.active_popup = True
            self.roomsList = QWidget()
            self.roomsListLayout = QGridLayout(self.roomsList)
            doors = next(loc['Doors'] for loc in self.roomAttributes if loc['Location'] == GVars.room)
            for pos, door in enumerate(doors):
                self.roomLabel = QLabel(door)
                self.roomsListLayout.addWidget(self.roomLabel, pos, 0)
            
            self.input = QLineEdit()
            self.input.setFixedWidth(156)
            self.input.setStyleSheet(main.cssMain)
            self.roomsListLayout.addWidget(self.input, len(doors), 0)
            self.input.returnPressed.connect(lambda: self.method_enter_room(self.input.text().upper()))

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(main.cssMain)
            self.roomsListLayout.addWidget(self.cancel, len(doors)+1, 0)
            self.cancel.clicked.connect(self.cancel_action)

            self.roomsSpacer = QWidget()
            self.roomsListLayout.addWidget(self.roomsSpacer, len(doors)+3, 0)
            self.roomsListLayout.setRowStretch(len(doors)+3, 1)
            self.columns.insertWidget(1, self.roomsList, alignment=Qt.AlignLeft)
        #open storage
        elif choice == 2:
            self.active_popup = True
            self.storageList = QWidget()
            self.storageListLayout = QGridLayout(self.storageList)
            storageData = next(loc['Storage'] for loc in self.roomAttributes if loc['Location'] == GVars.room)
            for pos, storage in enumerate(storageData):
                self.storeLabel = QLabel(storage)
                self.storeLabel.setFixedWidth(128)
                self.storageListLayout.addWidget(self.storeLabel, pos, 0)
            
            self.input = QLineEdit()
            self.input.setFixedWidth(156)
            self.input.setStyleSheet(main.cssMain)
            self.storageListLayout.addWidget(self.input, len(storageData), 0)
            self.input.returnPressed.connect(lambda: self.method_open_loot(self.input.text().strip()))
            
            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(main.cssMain)
            self.storageListLayout.addWidget(self.cancel, len(storageData)+1, 0)
            self.cancel.clicked.connect(self.cancel_action)

            self.roomsSpacer = QWidget()
            self.storageListLayout.addWidget(self.roomsSpacer, len(storageData)+2, 0)
            self.storageListLayout.setRowStretch(len(storageData)+2, 1)
            self.columns.insertWidget(1, self.storageList, alignment=Qt.AlignLeft)
        #use item
        elif choice == 3:
            self.active_popup = True
            try:
                itemDetails = next(item for item in GVars.itemCopies.values() if item['Item'] == GVars.equipped)
                item = itemDetails['Item']
                itemType = itemDetails['Type']

                if itemType == 'Weapon' and itemDetails.get('Cutting', False):
                    self.itemsList = QWidget()
                    self.itemsListLayout = QVBoxLayout(self.itemsList)
                    self.CutLabel = QLabel('Cut What? --> ')
                    self.itemsListLayout.addWidget(self.CutLabel, alignment=Qt.AlignLeft)
                    for cutting, count in GVars.inventory.items():
                        cuttingDetails = next(item for item in GVars.itemProperties if item['Item'] == cutting)
                        if cuttingDetails['Type'] == 'Food' and cuttingDetails['Item'] != 'Water':
                            self.itemButton = QLabel(cuttingDetails['Item'])
                            self.itemButton.setFixedWidth(128)
                            self.itemsListLayout.addWidget(self.itemButton, alignment=Qt.AlignLeft) 

                    self.itemInput = QLineEdit()
                    self.itemInput.setFixedWidth(128)
                    self.itemInput.setStyleSheet(main.cssMain)
                    self.itemInput.returnPressed.connect(lambda: (
                        setattr(GVars, 'ending', 'Jokester') if self.itemInput.text().title() == 'Cheese' and GVars.room == 'BATHROOM' else None,
                        (self.clearLayout(self.page), self.ending_credits()) if GVars.ending == 'Jokester' else None,
                        None if self.itemInput.text().title().strip() in GVars.itemCopies.keys() else next(
                            GVars.itemCopies.update({e['Item']: e}) for e in GVars.itemProperties if e['Item'] == self.itemInput.text().title().strip()
                        ),
                        GVars.itemCopies[self.itemInput.text().title()].__setitem__('Cut', True),
                        logging.info(f"Item {self.itemInput.text().title()} cut"),

                        # CREATE MESSAGE
                        (lambda msg: (
                            self.itemsListLayout.insertWidget(0, msg, alignment=Qt.AlignLeft),
                            # WAIT 2 SECONDS, THEN DO THE REST
                            QTimer.singleShot(2000, lambda: (
                                self.itemsListLayout.removeWidget(msg),
                                msg.deleteLater(),
                                next(
                                    (lambda dec: (
                                        dec.__setitem__('Count', dec['Count'] - 1),
                                        GVars.inventory.update({dec['Item']: GVars.inventory[dec['Item']] - 1}) if dec['Count'] - 1 == 0 else None,
                                        GVars.itemCopies.pop(dec['Item']) if dec['Count'] - 1 == 0 else None,
                                        setattr(GVars, 'equipped', '') if dec['Count'] - 1 == 0 else None
                                    ))(item) for item in GVars.itemCopies.values() if item['Item'] == GVars.equipped
                                ),
                                self.end_of_turn(),
                                self.cancel_action()
                            ))
                        ))(QLabel(f"Item {self.itemInput.text().title()} has been cut!"))
                    ))
                    self.itemsListLayout.addWidget(self.itemInput)

                    self.cancel = QPushButton('Cancel')
                    self.cancel.setFixedWidth(128)
                    self.cancel.setStyleSheet(main.cssMain)
                    self.itemsListLayout.addWidget(self.cancel)
                    self.cancel.clicked.connect(self.cancel_action)

                    self.roomsSpacer = QWidget()
                    self.itemsListLayout.addWidget(self.roomsSpacer, stretch=1)
                    self.columns.insertWidget(1, self.itemsList, alignment=Qt.AlignLeft, stretch=1)  
                elif itemType == 'Food':
                    nHealth = GVars.Health + int(itemDetails['Health'])
                    print(GFuncs.t(f"Health: {nHealth} = {GVars.Health} + {int(itemDetails['Health'])}"))
                    if nHealth > GVars.maxHealth:
                        GVars.Health = GVars.maxHealth
                        logging.info(f"Maxhealth {GVars.maxHealth} reached")
                    else:
                        GVars.Health = nHealth

                    if item == 'Cheese':
                        GVars.cheeseTolerance += 1
                        logging.info(f"Cheese tolerance decreased")
                    itemDetails['Count'] -= 1
                    if itemDetails['Count'] == 0:
                        GVars.inventory[item] -= 1
                        del GVars.itemCopies[item]
                        GVars.equipped = ''
                    logging.info(f"Item count decreased")
                    tip += 1 if tip == 3 else None
                elif itemType == 'Container':
                    # Find the lootbox data matching the equipped LootBox item
                    lootbox = next((lb for lb in GVars.dropables if lb['Storage'] == item), None)
                    if lootbox:
                        # Transfer all loot from the lootbox to player's inventory
                        for loot_item in lootbox['Loot'][:]:  # copy to avoid modification during iteration
                            if loot_item in GVars.inventory:
                                GVars.inventory[loot_item] += 1
                            else:
                                GVars.inventory[loot_item] = 1
                            lootbox['Loot'].remove(loot_item)
                        print(f"You opened the {item} and collected its contents...")
                        logging.info(f"LootBox '{item}' opened and emptied into inventory")
                    else:
                        print(f"No lootbox data found for {item}...")
                        logging.error(f"LootBox '{item}' data missing in dropables")
                elif itemType == 'Effect':
                    if itemDetails['Effect'] == 'Teleport':
                        roomDict = random.choice(self.rooms)
                        while True:
                            if GVars.room == roomDict['Location']:
                                roomDict = random.choice(self.rooms)
                            elif roomDict['Location'] == 'VEHICLE':
                                roomDict = random.choice(self.rooms)
                            else:
                                GVars.room = roomDict['Location']
                                break
                        logging.info(f"teleported to room {GVars.room}")
                        itemDetails['Count'] = itemDetails['Count'] - 1
                        if itemDetails['Count'] == 0:
                            GVars.inventory[item] -= 1
                            del GVars.itemCopies[item]
                            GVars.equipped = ''
                        logging.info(f"Item count decreased")
                    elif itemDetails['Effect'] == 'Strength':
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
                        print(f"{nHealth} = {GVars.Health} - {GVars.Health - nHealth}")
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
                elif itemType == 'Spawner':
                    GVars.enemies[GVars.itemCopies[item]['Spawn']]['Exists'] = True
                    GVars.enemies[GVars.itemCopies[item]['Spawn']]['Health'] = random.choice(GVars.enemies[GVars.itemCopies[item]['Spawn']]['HRange'])
                    enemyRoomOptions = random.choice(self.rooms)
                    GVars.enemies[GVars.itemCopies[item]['Spawn']]['Room'] = enemyRoomOptions['Location']
                    GVars.enemies[GVars.itemCopies[item]['Spawn']]['Location'] = 'LAUNCH SITE'
                    itemDetails['Count'] -= 1
                    if itemDetails['Count'] == 0:
                        GVars.inventory[item] -= 1
                        del GVars.itemCopies[item]
                        GVars.equipped = ''
                    logging.info(f"Enemy spawned")
                elif itemType == 'Instructions':
                    self.instructions = QWidget()
                    self.instructions_layout = QVBoxLayout(self.instructions)
                    self.instructions_label = QLabel(f"{itemDetails['Instructions']}")
                    self.instructions_label.setWordWrap(True)
                    self.instructions_layout.addWidget(self.instructions_label, alignment=Qt.AlignLeft)

                    self.cancel = QPushButton('Continue')
                    self.cancel.setFixedWidth(128)
                    self.cancel.setStyleSheet(main.cssMain)
                    self.instructions_layout.addWidget(self.cancel)
                    self.cancel.clicked.connect(self.cancel_action)

                    self.instructions_spacer = QWidget()
                    self.instructions_layout.addWidget(self.instructions_spacer, stretch=1)
                    self.columns.insertWidget(1, self.instructions, alignment=Qt.AlignLeft, stretch=1)
                else:
                    logging.error(f"Item {GVars.equipped} not found or has no properties")
                    self.cancel_action()

                if itemType in ['Container', 'Food', 'Effect', 'Spawner']:
                    self.end_of_turn()
                    self.cancel_action()
            except Exception as e:
                logging.exception(f"Something went wrong with item use: {e}")
                self.cancel_action()
        #equip item
        elif choice == 4:
            self.active_popup = True
            self.equipList = QWidget()
            self.equipListLayout = QVBoxLayout(self.equipList)
            self.equipListLayout.setContentsMargins(0,0,0,0)
            self.equipListLayout.setSpacing(0)
            for item, count in GVars.inventory.items():
                self.itemLabel = QLabel(f"{item} x {count}")
                self.itemLabel.setFixedWidth(128)
                self.equipListLayout.addWidget(self.itemLabel)

            self.equipInput = QLineEdit()
            self.equipInput.setFixedWidth(128)
            self.equipInput.setStyleSheet(main.cssMain)
            self.equipInput.returnPressed.connect(lambda: (
                    (lambda lbl=QLabel("Failed to equip"):
                        (self.equipListLayout.insertWidget(0, lbl, alignment=Qt.AlignLeft),
                        QTimer.singleShot(1000, lambda: (self.equipListLayout.removeWidget(lbl), lbl.deleteLater())))
                    )()
                ) if not GFuncs.func_equip_iem(self.equipInput.text().strip().title()) else (
                    (lambda lbl=QLabel("Equipped"):
                        (self.equipListLayout.insertWidget(0, lbl, alignment=Qt.AlignLeft),
                        QTimer.singleShot(1000, lambda: (self.equipListLayout.removeWidget(lbl), 
                                                         lbl.deleteLater(), 
                                                         self.Equipped.setText(f"Equipped: [{GVars.equipped}]"),
                                                         self.cancel_action(),
                                                         setattr(self, 'tip', 1) if tip == 2 else None,
                                                         self.clearLayout(self.page),
                                                         self.initialisation(self.page))))
                    )()
                )
            )
            self.equipListLayout.addWidget(self.equipInput)

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(main.cssMain)
            self.equipListLayout.addWidget(self.cancel)
            self.cancel.clicked.connect(self.cancel_action)

            self.roomsSpacer = QWidget()
            self.equipListLayout.addWidget(self.roomsSpacer, stretch=1)
            self.columns.insertWidget(1, self.equipList, alignment=Qt.AlignLeft, stretch=1)
        #store item
        elif choice == 5:
            self.active_popup = True
            self.storeWidget = QWidget()
            self.storeWidgetLayout = QVBoxLayout(self.storeWidget)
            self.title = QLabel("Store what item? --> ")
            self.storeWidgetLayout.addWidget(self.title, alignment=Qt.AlignLeft)
            for item in GVars.inventory.keys():
                self.itemLabel = QLabel(item)
                self.storeWidgetLayout.addWidget(self.itemLabel, alignment=Qt.AlignLeft)

            self.storeInput = QLineEdit()
            self.storeInput.setFixedWidth(128)
            self.storeInput.setStyleSheet('background-color: #ffeb88')
            self.storeInput.returnPressed.connect(lambda: self.method_handle_dropables('Store', self.storeInput.text().strip().title()))
            self.storeWidgetLayout.addWidget(self.storeInput, alignment=Qt.AlignLeft)

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(main.cssMain)
            self.storeWidgetLayout.addWidget(self.cancel)
            self.cancel.clicked.connect(self.cancel_action)

            self.roomsSpacer = QWidget()
            self.storeWidgetLayout.addWidget(self.roomsSpacer, stretch=1)
            self.columns.insertWidget(1, self.storeWidget, alignment=Qt.AlignLeft)
        #drop container
        elif choice == 6:
            self.active_popup = True
            self.dropWidget = QWidget()
            self.dropWidgetLayout = QVBoxLayout(self.dropWidget)
            self.dropTitle = QLabel('Drop What? --> ')
            self.dropWidgetLayout.addWidget(self.dropTitle, alignment=Qt.AlignLeft)
            for item in GVars.itemProperties:
                if item['Item'] in GVars.inventory.keys() and item['Type'] == 'Container':
                    self.itemLabel = QLabel(item['Item'])
                    self.dropWidgetLayout.addWidget(self.itemLabel, alignment=Qt.AlignLeft)
                
            self.dropInput = QLineEdit()
            self.dropInput.setFixedWidth(128)
            self.dropInput.setStyleSheet(main.cssMain)
            self.dropInput.returnPressed.connect(lambda: self.method_handle_dropables('Drop', self.dropInput.text().strip().title()))
            self.dropWidgetLayout.addWidget(self.dropInput, alignment=Qt.AlignLeft)

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(main.cssMain)
            self.dropWidgetLayout.addWidget(self.cancel)
            self.cancel.clicked.connect(self.cancel_action)

            self.dropSpacer = QWidget()
            self.dropWidgetLayout.addWidget(self.dropSpacer, stretch=1)
            self.columns.insertWidget(1, self.dropWidget, alignment=Qt.AlignLeft)
        #menu
        elif choice == 7:
            self.open_menu()
        #inventory
        elif choice == 8:
            self.active_popup = True
            logging.info('inventory loaded')
            self.invList = QWidget()
            self.invListLayout = QGridLayout(self.invList)
            for pos, (item, count) in enumerate(GVars.inventory.items()):
                self.invLabel = QLabel(f"{item} x {count}")
                self.invListLayout.addWidget(self.invLabel)
            
            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(main.cssMain)
            self.invListLayout.addWidget(self.cancel, len(GVars.inventory), 0)
            self.cancel.clicked.connect(self.cancel_action)

            self.roomsSpacer = QWidget()
            self.invListLayout.addWidget(self.roomsSpacer, len(GVars.inventory)+2, 0)
            self.invListLayout.setRowStretch(len(GVars.inventory)+2, 1)
            self.columns.insertWidget(1, self.invList, alignment=Qt.AlignLeft)
        #help
        elif choice == 9:
            self.active_popup = True
            logging.info('help menu loaded')
            self.helpList = QWidget()
            self.helpListLayout = QVBoxLayout(self.helpList)
            self.helpListLayout.addWidget(QLabel('1 = Enter a room with a door leading to your current room'))
            self.helpListLayout.addWidget(QLabel('2 = Open a storage container in your current room and collect the stored item'))
            self.helpListLayout.addWidget(QLabel('3 = Use currently equipped item'))
            self.helpListLayout.addWidget(QLabel('4 = Equip an item from your inventory'))
            self.helpListLayout.addWidget(QLabel('5 = Store an item in your inventory in another item of type "dropable" in your inventory'))
            self.helpListLayout.addWidget(QLabel('6 = Drop an item of type "dropable" from your inventory into your current room'))
            self.helpListLayout.addWidget(QLabel('7 = Open the main menu'))
            self.helpListLayout.addWidget(QLabel('8 = View the current contents of your inventory'))
            self.helpListLayout.setContentsMargins(0,0,0,0)

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(main.cssMain)
            self.helpListLayout.addWidget(self.cancel)
            self.cancel.clicked.connect(self.cancel_action)

            self.roomsSpacer = QWidget()
            self.helpListLayout.addWidget(self.roomsSpacer)
            self.columns.insertWidget(1, self.helpList, alignment=Qt.AlignLeft, stretch=1)
        #jumping
        elif choice == 'Jump':
            if GVars.room == 'ROOF':
                GVars.ending = 'Suicidal'
                self.clearLayout(self.page)
                self.ending_credits()
        #crafting
        elif choice == 'Craft':
            self.active_popup = True
            self.craftWidget = QWidget()
            self.craftLayout = QVBoxLayout(self.craftWidget)
            self.craftTitle = QLabel('Craft What? --> ')
            self.craftLayout.addWidget(self.craftTitle, alignment=Qt.AlignLeft)

            for craft, req in GVars.craftables.items():
                self.craftLabel = QLabel(craft)
                self.craftLabel.setToolTip(f"Requirements: {req}")
                self.craftLayout.addWidget(self.craftLabel, alignment=Qt.AlignLeft)
            
            self.craftInput = QLineEdit()
            self.craftInput.setFixedWidth(128)
            self.craftInput.setStyleSheet(main.cssMain)
            self.craftInput.returnPressed.connect(lambda: self.handle_crafting(self.craftInput.text().strip().title()))
            self.craftLayout.addWidget(self.craftInput, alignment=Qt.AlignLeft)

            self.cancel = QPushButton('Cancel')
            self.cancel.setStyleSheet(main.cssMain)
            self.cancel.setFixedWidth(128)
            self.cancel.clicked.connect(self.cancel_action)
            self.craftLayout.addWidget(self.cancel, alignment=Qt.AlignLeft)

            self.spacer = QWidget()
            self.craftLayout.addWidget(self.spacer, stretch=1)

            self.columns.insertWidget(1, self.craftWidget, alignment=Qt.AlignLeft)

        #end of turn screen update
        if not getattr(self, 'active_popup', False):
            self.cancel_action()

            self.clearLayout(self.page)
            self.initialisation(self.page)
        else:
            self.active_popup = False

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clearLayout(item.layout())

    def cancel_action(self):
        for attr in temp_widgets:
            if hasattr(self, attr):
                widget = getattr(self, attr)
                if widget is not None:
                    if widget.parent() is not None:  
                        try:
                            self.columns.removeWidget(widget)  # remove from layout
                        except Exception:
                            self.first_column_layout.removeWidget(widget)
                    widget.deleteLater()
                    setattr(self, attr, None)

        # Reset option buttons
        for btn in getattr(self, 'button_options', []):
            if btn:
                btn.setEnabled(True)
                btn.setStyleSheet(main.cssMain)

        self.active_popup = False

    def handle_crafting(self, craft):
        # Check if crafting requirements are met
        for craftable, req in GVars.craftables.items():
            if craftable == craft:
                crafting = {craftable : req}
                for item in req:
                    if item in GVars.inventory.keys():
                        if next(det['Type'] for det in GVars.itemProperties if det['Item'] == item) == 'Food' and GVars.itemCopies.get(item, {}).get('Cut', False):
                            continue
                        elif next(det['Type'] for det in GVars.itemProperties if det['Item'] == item) not in ['Recipe', 'Spawner', 'Food']:
                            continue
                        else:
                            logging.error(f"Crafting requirement {item} not met due to incorrect type or not cut")
                            return
                    else:
                        logging.info(f"Crafting requirements for {craft} not met")
                        return
        
        # All requirements met, proceed with crafting
        for reqs in crafting.values():
            for item in reqs:
                GVars.inventory[item] -= 1

                if item in GVars.itemCopies.keys():
                    del GVars.itemCopies[item]

                if GVars.inventory[item] == 0:
                    del GVars.inventory[item]
                    if GVars.equipped == item:
                        GVars.equipped = ''

        key = list(crafting.keys())[0]
        if key in GVars.inventory.keys():
            GVars.inventory[key] += 1
        else:
            GVars.inventory[key] = 1

        self.cancel_action()
                
    def method_enter_room(self, room_input, addon=False):
        global tip
        room = room_input.strip().upper()
        doors = next(loc['Doors'] for loc in self.roomAttributes if loc['Location'] == GVars.room) if not addon else None

        if doors and room not in doors:
            errorMsg = QLabel(f"Invalid Room...")
            logging.error(f"Could not enter room {room} due to being invalid or bugged")
            if hasattr(self, 'roomsListLayout'):
                self.roomsListLayout.addWidget(errorMsg, len(doors)+2, 0)
            return

        # Update current room
        global prevroom
        prevroom = GVars.room
        GVars.room = room

        if GVars.realm == 'Overworld':
            if GVars.room != 'VEHICLE':
                if GVars.room.endswith(' PORTAL'):
                    for modname, module in GVars.loadedExpansions.items():
                        if hasattr(module, 'realm'):
                            module.realm(GVars.room, self)
                else:
                    self.options = next(loc for loc in self.rooms if loc['Location'] == GVars.room)
                desc = self.options.get('Description', 'No description available')
                self.Description.setText(desc)
                self.Description.setWordWrap(True)
                self.Description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.Description.setMaximumHeight(100)

                self.button_options.clear()
                for key, option in self.options.items():
                    if key not in ['Location', 'Description']:
                        btn = QPushButton(option)
                        btn.setStyleSheet(main.cssMain)
                        btn.setFixedWidth(128)
                        self.content.addWidget(btn, alignment=Qt.AlignLeft)
                        btn.clicked.connect(lambda checked, b=btn, k=key, o=option: self.handle_option_click(k, o, b))
                        self.button_options.append(btn)
                self.content.addWidget(self.spacerOption, stretch=1)
                tip += 1 if tip == 0 else None
                logging.info(f"room {GVars.room} entered...")

            elif GVars.room == 'VEHICLE':
                # VEHICLE / addon logic
                if not GVars.expansions:
                    self.clearLayout(self.page)
                    GVars.ending = 'Speedster'
                    self.ending_credits()
                else:
                    self.addon_widget = QWidget()
                    self.addon_layout = QVBoxLayout(self.addon_widget)
                    self.addon_travel = QLabel('Which Location? -> ')
                    self.addon_layout.addWidget(self.addon_travel, alignment=Qt.AlignLeft)

                    for location in GVars.addonLocations:
                        lbl = QLabel(location)
                        self.addon_layout.addWidget(lbl, alignment=Qt.AlignLeft)

                    self.addon_input = QLineEdit()
                    self.addon_input.setFixedWidth(128)
                    self.addon_input.setStyleSheet(main.cssMain)
                    self.addon_layout.addWidget(self.addon_input, alignment=Qt.AlignLeft)

                    # Inline connection to set module and update room/attributes/lootBoxes
                    self.addon_input.returnPressed.connect(lambda checked=False: self.enter_addon(new_room=self.addon_input.text().strip().upper()))

                    self.spacer = QWidget()
                    self.addon_layout.addWidget(self.spacer, stretch=1)

                    self.columns.insertWidget(2, self.addon_widget, alignment=Qt.AlignLeft)
        else:
            for modname, module in GVars.loadedExpansions.items():
                if hasattr(module, 'realm_addon') and modname == GVars.realm:
                    module.realm_addon(GVars.room, self)

        if not GVars.ending:
            self.end_of_turn()

        # Refresh main UI
        if not GVars.ending and (GVars.room not in GVars.vehicleVariants or not GVars.expansions):
            self.cancel_action()
            self.clearLayout(self.page)
            self.initialisation(self.page)
            self.active_popup = False
        
    def method_open_loot(self, storage):
        global tip
        if sum(GVars.inventory.values()) < GVars.inventoryLen:
            STORAGE = storage.upper()
            Storage = storage.title()
            dropable = [d for d in GVars.dropables if d['Storage'] == STORAGE or d['Storage'] == Storage]
            if not dropable:
                if storage == 'DECORATED CHEST' and 'Key' not in GVars.inventory:
                    logging.warning(f"Dependency of key not met. {GVars.inventory}")
                    time.sleep(1)
                    return
                
                opening = next((store for store in self.lootBoxes if store['Storage'] == STORAGE), (store for store in self.lootBoxes if store['Storage'] == Storage))
                loot = random.choices(
                    population= opening['Loot'],
                    weights= [0.25 if item == 'Cheese' else 1.0 for item in opening['Loot']], 
                    k=1
                    )[0]
                opening['Loot'].remove(loot)
                logging.debug(f"Loot {loot} removed from lootbox {opening['Storage']}")
                if loot in GVars.inventory.keys():
                    GVars.inventory[loot] += 1
                else:
                    GVars.inventory[loot] = 1
                tip += 1 if tip == 1 else None
                logging.info(f"item {loot} added to inventory")

                locationStorage = next(loc['Storage'] for loc in self.roomAttributes if loc['Location'] == GVars.room)
                if opening['Storage'] in locationStorage:
                    locationStorage.remove(opening['Storage'])
                else:
                    logging.warning(f"Storage {opening['Storage']} was not in room storage when prompted to be removed")
            else:
                opening = next(store for store in self.lootBoxes if store['Storage'] == storage)
                for item in opening['Loot']:
                    if item in GVars.inventory.keys():
                        GVars.inventory[item] += 1
                    else:
                        GVars.inventory[item] = 1
                tip += 1 if tip == 1 else None
                logging.info(f"items {opening['Loot']} added to inventory")
                GVars.inventory[opening['Storage']] = GVars.inventory.get(opening['Storage'], 0) + 1
                logging.info(f"{opening['Storage']} added to inventory")

                locationStorage = next(loc['Storage'] for loc in self.roomAttributes if loc['Location'] == GVars.room)
                if opening['Storage'] in locationStorage:
                    locationStorage.remove(opening['Storage'])
                else:
                    logging.warning(f"Storage {opening['Storage']} was not in room storage when prompted to be removed")

            if storage == 'DECORATED CHEST' and 'Key' in GVars.inventory.keys():
                GVars.inventory['Key'] -= 1
                if GVars.inventory['Key'] <= 0:
                    del GVars.inventory['Key']
                logging.info(f"Key removed from inventory")

            self.end_of_turn()
            self.cancel_action()
            self.clearLayout(self.page)
            self.initialisation(self.page)

    def method_handle_dropables(self, action, item):
        global tip

        if action == 'Store':
            self.dropList = QWidget()
            self.dropListLayout = QVBoxLayout(self.dropList)
            self.titleStore = QLabel('In What? --> ')
            self.dropListLayout.addWidget(self.titleStore, alignment=Qt.AlignLeft)
            for it in GVars.itemProperties:
                if it['Type'] == 'Container' and it['Item'] in GVars.inventory.keys():
                    dropable = it['Item']
                    self.itemLabel = QLabel(dropable)
                    self.dropListLayout.addWidget(self.itemLabel, alignment=Qt.AlignLeft) 
            
            self.dropInput = QLineEdit()
            self.dropInput.setFixedWidth(128)
            self.dropInput.setStyleSheet(main.cssMain)
            self.dropInput.returnPressed.connect(lambda: (
                (setattr(GVars, 'ending', 'Dumbass') or True) and self.ending_credits()
                if item == self.dropInput.text().strip().title() else (
                    any(d['Loot'].append(item)
                        for d in GVars.dropables
                        for p in GVars.itemProperties
                        if d['Storage'] == self.dropInput.text().strip().title()
                        and p['Item'] == self.dropInput.text().strip().title()
                        and len(d['Loot']) < p['Slots']
                        and item not in d['Loot']
                    ) and (lambda: (
                        GVars.inventory.__setitem__(item, GVars.inventory.get(item, 1) - 1),
                        GVars.inventory.pop(item) if GVars.inventory.get(item, 0) <= 0 else None
                    ))(),
                ),
                self.cancel_action(),
                logging.info(f"Dropable {self.dropInput.text().strip().title()} has stored {item}"),
                setattr(self, 'tip', 1) if tip == 4 else None
            ))
            self.dropListLayout.addWidget(self.dropInput, alignment=Qt.AlignLeft)

            # Add Cancel button right after doors
            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(main.cssMain)
            self.dropListLayout.addWidget(self.cancel)
            self.cancel.clicked.connect(self.cancel_action)

            self.roomsSpacer = QWidget()
            self.dropListLayout.addWidget(self.roomsSpacer, stretch=1)
            self.columns.insertWidget(2, self.dropList, alignment=Qt.AlignLeft)
        elif action == 'Drop':
            for room in self.roomAttributes:
                if room['Location'] == GVars.room:
                    room['Storage'].append(item)
            GVars.inventory[item] -= 1
            logging.info(f"Item {item} dropped")
            tip += 1 if tip == 5 else None
        self.clearLayout(self.page)
        self.initialisation(self.page)
        return

    def reveal_room_name_effect(self, room_name: str, flicker_count: int = 2, interval: int = 40):
        """
        Animates the room name label with a sci-fi flicker effect.
        - room_name: The final room name to display.
        - flicker_count: How many random flickers per character.
        - interval: Milliseconds between flickers.
        """
        self._reveal_index = 0
        self._reveal_flicker = 0
        self._reveal_final = room_name
        self._reveal_display = ""
        self._reveal_timer = QTimer(self)
        self._reveal_timer.setInterval(interval)

        def update_label():
            if self._reveal_index < len(self._reveal_final):
                if self._reveal_flicker < flicker_count:
                    # Flicker random char
                    flicker_char = random.choice(string.ascii_uppercase + string.digits + " ")
                    self.Location.setText(self._reveal_display + flicker_char)
                    self._reveal_flicker += 1
                else:
                    # Reveal real char
                    self._reveal_display += self._reveal_final[self._reveal_index]
                    self.Location.setText(self._reveal_display)
                    self._reveal_index += 1
                    self._reveal_flicker = 0
            else:
                self.Location.setText(self._reveal_final)
                self._reveal_timer.stop()

        self._reveal_timer.timeout.connect(update_label)
        self._reveal_timer.start()
                
    def open_menu(self):
        if not self.isVisible():
            self.show()
        music.music.fadeout(1000)
        music.music.load(musVars.musCredits)
        self.app_window.open_menu()
        self.close()
        music.music.play(-1, fade_ms=1000)

    def end_of_turn(self):
        #realm vehicle check
        #check for no count in inventory
        items_to_remove = [item for item, count in GVars.inventory.items() if count <= 0]
        for item in items_to_remove:
            del GVars.inventory[item]
        #Enemy movement + battle checks
        for enemy_name, enemy_data in GVars.enemies.items():
            if enemy_data['Location'] == GVars.expansionLoc:
                if not (enemy_data['Exists'] and not enemy_data['Defeated']):
                    continue

                current_room = enemy_data['Room']  # enemy's room before movement
                next_room = current_room  # default to no movement

                # --- Determine movement ---
                if enemy_data.get('Follow', False):
                    playerDoorsC = next((room['Doors'] for room in self.roomAttributes if room['Location'] == GVars.room), [])
                    playerDoorsP = next((room['Doors'] for room in self.roomAttributes if room['Location'] == prevroom), [])
                    enemyDoors = next((room['Doors'] for room in self.roomAttributes if room['Location'] == current_room), [])

                    matchC = next((door for door in playerDoorsC if door in enemyDoors), None)
                    matchP = next((door for door in playerDoorsP if door in enemyDoors), None)

                    if matchC:
                        next_room = matchC
                    elif matchP:
                        next_room = matchP
                    else:
                        # Random movement respecting restrictions
                        attempt = 0
                        while True:
                            next_room = random.choice(enemyDoors)
                            if next_room in enemy_data['Restrictions'] or any(other['Room'] == next_room for other in GVars.enemies.values() if other != enemy_data):
                                attempt += 1
                                if attempt == 10:
                                    logging.critical(f"Enemy {enemy_name} cannot find valid door, staying in room")
                                    next_room = current_room
                                    break
                                continue
                            break

                elif enemy_data['Room'] == current_room:
                    enemyDoors = next((room['Doors'] for room in self.roomAttributes if room['Location'] == current_room), [])
                    attempt = 0
                    while True:
                        next_room = random.choice(enemyDoors)
                        if next_room in enemy_data['Restrictions'] or any(other['Room'] == next_room for other in GVars.enemies.values() if other != enemy_data):
                            attempt += 1
                            if attempt == 10:
                                logging.critical(f"Enemy {enemy_name} cannot find valid door, staying in room")
                                next_room = current_room
                                break
                            continue
                        break

                # Apply movement
                enemy_data['Room'] = next_room

                # --- Single battle check: pass-through or end-up-in-room ---
                if current_room == GVars.room or next_room == GVars.room:
                    logging.info(f"Opening battle with {enemy_name}")
                    self.method_open_window(enemy=enemy_name)
        #odd case demon is dead
        if all(enemy['Defeated'] for enemy in GVars.enemies.values()):
            logging.debug(f"Game ended")
            self.clearLayout(self.page)
            self.ending_credits()
        #strength buff
        if sum(GVars.inventory.values()) > 10:
            inv_overload = sum(GVars.inventory.values())-10
            GVars.maxHealth = (GVars.inventoryLen*10)-(10*inv_overload)
            logging.debug(f"Inventory buff managed {GVars.maxHealth}")
        #death (normal)
        if GVars.Health <= 0:
            GVars.ending = 'Slaughtered' if GVars.Health > -5 else 'Poked' 
            self.clearLayout(self.page)
            self.ending_credits()
        #death by cheese
        if GVars.cheeseTolerance > 3:
            GVars.ending = 'Cheesed'
            GVars.Health = 0
            self.clearLayout(self.page)
            self.ending_credits()
        #add-on conditions
        for modName, module in GVars.loadedExpansions.items():
            if hasattr(module, 'conditions'):
                module.conditions()

