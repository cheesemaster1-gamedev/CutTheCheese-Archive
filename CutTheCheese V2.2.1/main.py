from sys import argv, exit
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QApplication,
    QSpacerItem,
    QSizePolicy, 
    QLineEdit as QLE,
    QCheckBox,
    QSlider,
    QComboBox
)
from PySide6.QtCore import (
    Qt,
    QObject, 
    QTimer
)
from PySide6.QtGui import (
    QKeySequence
)
import time, json, random, logging, sys, string, inspect, webbrowser
import pygame.mixer as music

from Global import (
    GlobalVariables as GVars,
    GlobalFunctions as GFuncs
)
from RESOURCES import (
    Tutorial as Trl,
    Languages_handler as lang
)
from AUDIO import musicVars as musVars
try:
    from RESOURCES.Languages_handler import (
        QLabel,
        QPushButton,
        QLineEdit
    )
except Exception as e:
    logging.exception("Failed to import translated widgets, falling back to defaults.", exc_info=e)
    try:
        from RESOURCES.Autocorrect import QLineEdit
    except Exception as e:
        logging.exception("Failed to import Autocorrect, falling back to default", exc_info=e)
    from PySide6.QtWidgets import QLabel, QPushButton
    
version = '2.1.3'
logging.debug(f"Game version: {version}")

def apply_music_volume():
    music.music.set_volume(GVars.musicVolume / 100)

rooms = [{'Location': 'OUTSIDE', 'Description': 'You stand in a quiet yard, the air crisp and fresh. The mailbox creaks gently in the breeze, leaves rustle softly beneath your feet, and distant birdsong fills the morning. The cracked pathway leads your eyes toward the old house, promising stories waiting inside.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', '7': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'CORRIDOR', 'Description': 'A dimly lit corridor stretches ahead, its scuffed wooden floor whispering secrets of countless footsteps. Doors to other rooms flank each side, some slightly ajar, revealing glimpses of shadowed interiors. The faint smell of aged wood mingles with dust in the air.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'KITCHEN', 'Description': 'The kitchen is cluttered and cozy, filled with forgotten utensils hanging on rusty hooks and mismatched plates stacked high. The fridge hums steadily in the corner, its glow casting eerie shadows over cracked countertops. The scent of stale coffee lingers faintly.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'BEDROOM', 'Description': 'This small bedroom feels lived-in yet neglected. An unmade bed lies crumpled under a thin blanket, and dusty shelves crowd the walls, housing trinkets and old books. A narrow window lets in pale light, illuminating floating dust motes dancing in the air.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'UPSTAIRS', 'Description': 'The upstairs landing creaks with every step you take. The air is thick with a mix of old wallpaper scents and faint drafts slipping through cracked windows. Doors open into rooms filled with memories and forgotten tales.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'ATTIC', 'Description': 'Low ceilings and thick cobwebs create a feeling of timeless abandonment. The dusty attic holds forgotten relics — old trunks, faded photographs, and brittle letters. The air is stale but charged with a hint of mystery, as if memories cling stubbornly here.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'BASEMENT', 'Description': 'Dim and damp, the basement holds a chilling silence and old storage. Shadows dance against the cracked walls, and the scent of mildew mingles with the faint echo of dripping water. It feels like a place where secrets hide in the dark.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'GARAGE', 'Description': 'A clean garage with tools neatly arranged and a vehicle sitting in the center of the room. The scent of oil and rubber fills the air, and sunlight filters through the dusty windows, illuminating the workbench scattered with half-finished projects.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'BATHROOM', 'Description': 'A sterile bathroom with a flickering light and a cracked mirror. The faint drip of a leaky faucet echoes softly, while the chipped tiles and worn linoleum floor tell tales of long days and forgotten nights.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'LOUNGE', 'Description': 'A cozy lounge with worn-out furniture and a dusty television. Faded photographs hang crookedly on the walls, and the faint smell of old books and pipe tobacco lingers in the air, inviting quiet reflection.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'DINING ROOM', 'Description': 'A long table dominates the room, set for a meal that never came. Dust-covered plates and tarnished cutlery hint at celebrations frozen in time, while a chandelier overhead flickers weakly, casting dancing shadows.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'TUNNELS', 'Description': 'A narrow TUNNELS, carved roughly through the rock, leads to darker places. The air grows colder and thicker with each step, and the sound of distant dripping water echoes off the uneven walls, hinting at mysteries hidden deeper underground.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'ROOF', 'Description': 'A precarious perch with a sweeping view, the wind whispers secrets as it swirls around you. The sky stretches wide and endless above, dotted with stars even in daylight, while the city hums far below, muffled and distant.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'FOREST', 'Description': 'Tall trees surround you, their branches knitting a thick canopy overhead. The undergrowth is dense with secrets and sounds — rustling leaves, distant animal calls, and the steady pulse of nature alive and watching.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'CAMPSITE', 'Description': 'A quiet clearing with a worn tent and signs of a long-abandoned fire. Scattered ashes and broken logs hint at stories shared beneath the stars, while the scent of pine and earth fills the cool night air.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'CAVES', 'Description': 'Natural caves extend into the darkness, the air cool and still. Stalactites hang like silent sentinels from the ceiling, and the faint sound of dripping water echoes through vast, shadowed chambers.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'},
        {'Location': 'CAVERNS', 'Description': 'A vast underground space with echoes that never seem to fade. The cavern walls glisten faintly with moisture, and the distant rumble of shifting earth reminds you that this place is alive, ancient, and full of untold secrets.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = show inventory', '9': '9 = help'}]
roomAttributes = [{'Location' : 'OUTSIDE', 'Doors' : ['KITCHEN', 'CORRIDOR', 'GARAGE', 'FOREST'], 'Storage' : ['MAILBOX']},
                {'Location' : 'CORRIDOR', 'Doors' : ['KITCHEN', 'BATHROOM', 'UPSTAIRS', 'OUTSIDE', 'BASEMENT'], 'Storage' : ['CABINET']},
                {'Location' : 'KITCHEN', 'Doors' : ['CORRIDOR', 'DINING ROOM', 'ATTIC', 'OUTSIDE'], 'Storage' : ['CABINET','FRIDGE']},
                {'Location' : 'ATTIC', 'Doors' : ['KITCHEN', 'UPSTAIRS', 'ROOF'], 'Storage' : ['CHEST', 'CABINET']},
                {'Location' : 'BASEMENT', 'Doors' : ['CORRIDOR', 'TUNNELS'], 'Storage' : ['FRIDGE', 'CHEST']},
                {'Location' : 'TUNNELS', 'Doors' : ['BASEMENT', 'CAVES'], 'Storage' : ['DECORATED CHEST']},
                {'Location' : 'ROOF', 'Doors' : ['ATTIC'], 'Storage' : []},
                {'Location' : 'UPSTAIRS', 'Doors' : ['ATTIC', 'CORRIDOR', 'LOUNGE', 'BEDROOM'], 'Storage' : ['CABINET', 'CHEST']},
                {'Location' : 'GARAGE', 'Doors' : ['OUTSIDE', 'VEHICLE'], 'Storage' : ['CHEST']},
                {'Location' : 'BEDROOM', 'Doors' : ['UPSTAIRS'], 'Storage' : ['CABINET', 'CHEST']},
                {'Location' : 'DINING ROOM', 'Doors' : ['KITCHEN', 'BATHROOM'], 'Storage' : ['CHEST']},
                {'Location' : 'BATHROOM', 'Doors' : ['DINING ROOM', 'CORRIDOR'], 'Storage' : []},
                {'Location' : 'LOUNGE', 'Doors' : ['UPSTAIRS'], 'Storage' : ['CABINET']},
                {'Location' : 'FOREST', 'Doors' : ['OUTSIDE', 'CAMPSITE', 'CAVES'], 'Storage' : []},
                {'Location' : 'CAMPSITE', 'Doors' : ['FOREST'], 'Storage' : ['TENT']},
                {'Location' : 'CAVES', 'Doors' : ['FOREST', 'CAVERNS', 'TUNNELS'], 'Storage' : []},
                {'Location' : 'CAVERNS', 'Doors' : ['CAVES'], 'Storage' : ['WAR CHEST']}]
lootBoxes = [{'Storage' : 'DECORATED CHEST', 'Loot' : ['Soul Orb']},
            {'Storage' : 'CHEST', 'Loot' : ['Sword', 'Potion', 'Sack', 'Revolver', 'Key', 'Belt']},
            {'Storage' : 'MAILBOX', 'Loot' : ['Box']},
            {'Storage' : 'FRIDGE', 'Loot' : ['Cheese', 'Apple']},
            {'Storage' : 'CABINET', 'Loot' : ['Cheese', 'Slingshot', 'Water Bottle', 'Ham', 'Bread', 'Recipe']},
            {'Storage' : 'WAR CHEST', 'Loot' : ['Cannon']},
            {'Storage' : 'TENT', 'Loot' : ['Stick']}]

prevroom, module = None, None
temp_widgets = ['roomsList', 'storageList', 'invList', 'helpList', 'itemsList', 'equipList', 'storeWidget', 'dropList', 'dropWidget', 'load_widget', 'toggle_widget', 'addon_widget', 'instructions', 'craftWidget', 'info_column', 'descWidget', 'settings_widget']  # Add more as needed

credits = ['Cheese Master 1 - Lead developer', 
           'Chuck B - Lead sound designer', 
           'Ethan Molyneux - Beta tester', 
           "Tech - Beta tester (thanks for the slipper)", 
           "Special thanks to the developers at OpenAI for the online chatbot ChatGPT for it's assistance in debugging as well as the developers behind SUNO for it's assistance in developing sound tracks"]
hallOfCheese = []
DBLeaderboard = {'1':'[empty]', '2':'[empty]', '3':'[empty]'}

class menu_UI(QMainWindow):
    def __init__(self):
        super().__init__()

        global cssMain, cssSelected
        cssSelected = cssMain

        self.child_window = None
        self.autocorrect_Enabled = True
        self.temp_Auto_QLE = None

        self.setWindowTitle('Cut The Cheese 2')
        self.setStyleSheet(cssSelected)
        self.menu_widget = QWidget()
        self.setMinimumSize(720, 640)
        self.setCentralWidget(self.menu_widget)
        self.page = QVBoxLayout(self.menu_widget)

        music.init()
        music.music.load(musVars.musCredits)
        music.music.play(loops=-1, fade_ms=1000)
        apply_music_volume()
        self.info_column = None
        
        self.initialisation()

    def initialisation(self):
        global cssMain, cssSelected
        cssSelected = cssMain

        self.upper_content = QWidget()
        self.upper_content_layout = QVBoxLayout(self.upper_content)
        self.page.addWidget(self.upper_content)
        self.lower_content = QWidget()
        self.lower_content_layout = QHBoxLayout(self.lower_content)
        self.page.addWidget(self.lower_content)

        self.game_Title = QLabel(f'Cut The Cheese  ---  Version {version}')
        self.game_Title.setStyleSheet("""
                                     font-size: 24px;
                                     font-weight: bold;
                                      """)
        self.upper_content_layout.addWidget(self.game_Title, alignment=Qt.AlignLeft)
        self.upper_content.setStyleSheet("""background-color: #b27f00;
                                         border-radius: 10px;""")

        self.first_column = QWidget()
        self.first_column_layout = QVBoxLayout(self.first_column)
        self.second_column = QWidget()
        self.second_column_layout = QVBoxLayout(self.second_column)

        self.resume = QPushButton('Resume')
        self.resume.setStyleSheet(cssSelected)
        self.resume.setFixedWidth(128)
        self.first_column_layout.addWidget(self.resume, alignment=Qt.AlignLeft)
        self.resume.setEnabled(self.child_window is not None)
        self.resume.clicked.connect(self.resume_current_game)

        self.load = QPushButton('Load Game')
        self.load.setStyleSheet(cssSelected)
        self.load.setFixedWidth(128)
        self.first_column_layout.addWidget(self.load, alignment=Qt.AlignLeft)
        self.load.clicked.connect(lambda: self.method_menu_controls(action=0))

        self.start = QPushButton('Start New Game')
        self.start.setStyleSheet(cssSelected)
        self.start.setFixedWidth(128)
        self.first_column_layout.addWidget(self.start, alignment=Qt.AlignLeft)
        self.start.clicked.connect(lambda: self.method_menu_controls(action=1))

        self.save = QPushButton('Save Game')
        self.save.setStyleSheet(cssSelected)
        self.save.setFixedWidth(128)
        self.first_column_layout.addWidget(self.save, alignment=Qt.AlignLeft)
        self.save.clicked.connect(lambda: self.method_menu_controls(action=2))

        self.manage = QPushButton('Manage Add-Ons')
        self.manage.setStyleSheet(cssSelected)
        self.manage.setFixedWidth(128)
        self.first_column_layout.addWidget(self.manage, alignment=Qt.AlignLeft)
        self.manage.clicked.connect(lambda: self.method_menu_controls(action=3))

        self.tutorial = QPushButton('Tutorial')
        self.tutorial.setStyleSheet(cssSelected)
        self.tutorial.setFixedWidth(128)
        self.first_column_layout.addWidget(self.tutorial, alignment=Qt.AlignLeft)
        self.tutorial.clicked.connect(lambda: self.method_menu_controls(action=4))

        self.settings = QPushButton("Settings")
        self.settings.setStyleSheet(cssSelected)
        self.settings.setFixedWidth(128)
        self.first_column_layout.addWidget(self.settings, alignment=Qt.AlignLeft)
        self.settings.clicked.connect(lambda: self.method_menu_controls(action=5))

        self.report = QPushButton('Report Bug')
        self.report.setStyleSheet(cssSelected)
        self.report.setFixedWidth(128)
        self.first_column_layout.addWidget(self.report, alignment=Qt.AlignLeft)
        self.report.clicked.connect(lambda: webbrowser.open("https://itch.io/t/5366449/v2-bugs"))
        self.report.setToolTip(f"Click here if something went wrong!")

        self.suggestions = QPushButton('V3 Suggestions')
        self.suggestions.setStyleSheet(cssSelected)
        self.suggestions.setFixedWidth(128)
        self.first_column_layout.addWidget(self.suggestions, alignment=Qt.AlignLeft)
        self.suggestions.clicked.connect(lambda: webbrowser.open("https://itch.io/t/5436917/v3-ideas"))
        self.suggestions.setToolTip(f"Will take you to the V3 suggestions page to make a suggestion about the new unity build coming soon")

        self.spacer = QWidget()
        self.first_column_layout.addWidget(self.spacer, stretch=1)

        self.patchNotes = QLabel("Patch Notes / Important Stuff ->\nPlease note, The new autocorrect function can get words wrong. \nIf so, please report it and a patch should come out soon after. \nYou may also disable the autocrrect in the settings tab in the menu to the left. \n\n And remember, if you have any other issues\nplease report them using the report button under the inventory in gameplay...")
        self.patchNotes.setWordWrap(True)
        self.patchNotes.setStyleSheet(cssSelected)
        self.second_column_layout.addWidget(self.patchNotes, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.column_spacer = QWidget()
        self.lower_content_layout.addWidget(self.first_column)
        self.lower_content_layout.addWidget(self.second_column)
        self.lower_content_layout.addWidget(self.column_spacer, stretch=1)

    def method_menu_controls(self, action):
        if action == 0:
            self.lower_content_layout.removeWidget(self.second_column)
            self.second_column.hide()
            self.load_widget = QWidget()
            self.load_layout = QVBoxLayout(self.load_widget)
            self.load_Title = QLabel('LOAD GAME ->')
            self.load_layout.addWidget(self.load_Title, alignment=Qt.AlignLeft)
            for i in range(1, 4):
                try:
                    with open(f"Saves/Save{i}.json", 'r') as f:
                        data = json.load(f)
                        name = data.get("name", "Unnamed")
                        self.button = QPushButton(f"Slot {i}; {name}")
                        self.button.setFixedWidth(256)
                        self.button.setStyleSheet(cssSelected)
                        self.load_layout.addWidget(self.button, alignment=Qt.AlignLeft)
                        self.button.clicked.connect(lambda checked=False, slot=i: (GFuncs.func_load_game(slot),
                                                                                   self.method_open_window()))
                except FileNotFoundError:
                    self.button = QLabel(f"Slot {i}; [Empty]")
                    self.load_layout.addWidget(self.button, alignment=Qt.AlignLeft)
            try:
                with open(f"Saves/EmergencySave.json", 'r') as f:
                    data = json.load(f)
                    name = data.get("name", "Unnamed")
                    self.button = QPushButton(f"Emergency Save; {name}")
                    self.button.setFixedWidth(256)
                    self.button.setStyleSheet(cssSelected)
                    self.load_layout.addWidget(self.button, alignment=Qt.AlignLeft)
                    self.button.clicked.connect(lambda: (GFuncs.func_load_game(slot=8),
                                                         self.method_open_window()))
            except FileNotFoundError:
                self.button = QLabel("Emergency Save; [Empty]")
                self.load_layout.addWidget(self.button, alignment=Qt.AlignLeft)
            
            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(cssSelected)
            self.spacer = QWidget()
            self.load_layout.addWidget(self.cancel, alignment=Qt.AlignLeft)
            self.load_layout.addWidget(self.spacer, stretch=1)
            self.cancel.clicked.connect(self.cancel_action)

            self.lower_content_layout.insertWidget(1, self.load_widget, alignment=Qt.AlignLeft)
        elif action == 1:
            self.lower_content_layout.removeWidget(self.second_column)
            self.second_column.hide()
            GFuncs.func_reset_all_vars()
            logging.info(f"New game started")
            self.method_open_window()
        elif action == 2:
            self.lower_content_layout.removeWidget(self.second_column)
            self.second_column.hide()
            self.load_widget = QWidget()
            self.load_layout = QVBoxLayout(self.load_widget)
            self.load_Title = QLabel('SAVE GAME ->')
            self.load_layout.addWidget(self.load_Title, alignment=Qt.AlignLeft)

            self.name = QLineEdit()
            self.name.setPlaceholderText("Enter save name")
            self.name.setStyleSheet(cssSelected)
            self.name.setFixedWidth(256)
            self.load_layout.addWidget(self.name, alignment=Qt.AlignLeft)

            for i in range(1, 4):
                try:
                    with open(f"Saves/Save{i}.json", 'r') as f:
                        data = json.load(f)
                        name = data.get("name", "Unnamed")
                        self.button = QPushButton(f"Slot {i}; {name}")
                        self.button.setFixedWidth(256)
                        self.button.setStyleSheet(cssSelected)
                        self.load_layout.addWidget(self.button, alignment=Qt.AlignLeft)
                        self.button.clicked.connect(lambda checked=False, slot=i: self.save_file(f"Saves/Save{slot}.json", slot, self.name.text()))
                except FileNotFoundError:
                    self.button = QLabel(f"Slot {i}; [Empty]")
                    self.load_layout.addWidget(self.button, alignment=Qt.AlignLeft)
                        
            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(cssSelected)
            self.spacer = QWidget()
            self.load_layout.addWidget(self.cancel, alignment=Qt.AlignLeft)
            self.load_layout.addWidget(self.spacer, stretch=1)
            self.cancel.clicked.connect(self.cancel_action)

            self.lower_content_layout.insertWidget(1, self.load_widget, alignment=Qt.AlignLeft)
        elif action == 3:
            self.lower_content_layout.removeWidget(self.second_column)
            self.second_column.hide()
            self.toggle_widget = QWidget()
            self.toggle_layout = QVBoxLayout(self.toggle_widget)
            self.toggle_layout.addWidget(QLabel("Toggle Add-ons -> "), alignment=Qt.AlignLeft)

            from functools import partial

            # Iterate through addons
            for addon_category in GVars.addons:
                for category, packs in addon_category.items():
                    self.toggle_layout.addWidget(QLabel(f"{category.title()}:"))

                    for pack_name, details in packs.items():
                        status = details.get('Status', 'Unknown') if isinstance(details, dict) else 'Unknown'

                        # Create horizontal layout for this pack
                        pack_widget = QWidget()
                        pack_layout = QHBoxLayout(pack_widget)

                        # Local variables for each button and label
                        btn = QPushButton(f"{pack_name}")
                        btn.setFixedWidth(128)
                        btn.setStyleSheet(cssSelected)

                        status_label = QLabel(f"Status: {status}")
                        status_label.setFixedWidth(72)

                        more_info = QPushButton("More Info")
                        more_info.setFixedWidth(128)
                        more_info.setStyleSheet(cssSelected)
                        more_info.clicked.connect(lambda checked=False, pack=pack_name: self.show_More_Info(pack_name=pack))

                        pack_layout.addWidget(btn)
                        pack_layout.addWidget(status_label)
                        pack_layout.addWidget(more_info)
                        pack_layout.addStretch()
                        pack_layout.setContentsMargins(0, 0, 0, 0)
                        pack_layout.setSpacing(0)

                        self.toggle_layout.addWidget(pack_widget, alignment=Qt.AlignLeft)

                        # Safe connection using partial
                        btn.clicked.connect(partial(self.toggle_addon, pack_name, status_label))

            # Close button
            close_btn = QPushButton('Close')
            close_btn.setFixedWidth(128)
            close_btn.setStyleSheet(cssSelected)
            close_btn.clicked.connect(self.cancel_action)
            self.toggle_layout.addWidget(close_btn, alignment=Qt.AlignLeft)

            self.toggle_layout.addStretch()  # Push items to top
            self.lower_content_layout.insertWidget(1, self.toggle_widget, alignment=Qt.AlignLeft)
        elif action == 4:
            self.method_open_tutorial()
        elif action == 5:
            self.settings_widget = QWidget()
            self.settings_layout = QVBoxLayout(self.settings_widget)
            self.settings_layout.addWidget(QLabel("Settings ->"), alignment=Qt.AlignLeft)

            # Add settings options here (e.g., checkboxes, sliders)
            # For example:
            self.autocorrect_checkbox = QCheckBox("Toggle Autocorrect")
            self.autocorrect_checkbox.setChecked(self.autocorrect_Enabled)
            self.autocorrect_checkbox.setStyleSheet("""
                QCheckBox {
                    background-color: #cc9900;
                    spacing: 6px;
                }

                QCheckBox::indicator {
                    width: 14px;
                    height: 14px;
                    border: 1px solid #4a3200;
                    background-color: #ffeb88;
                }

                QCheckBox::indicator:checked {
                    background-color: #2f9e44;
                    border: 2px solid #14532d;
                }
            """)
            self.autocorrect_checkbox.clicked.connect(self.toggle_autocorrect)
            self.settings_layout.addWidget(self.autocorrect_checkbox, alignment=Qt.AlignLeft)

            self.volume_label = QLabel(f"Music Volume: {GVars.musicVolume}%")
            self.settings_layout.addWidget(self.volume_label, alignment=Qt.AlignLeft)

            self.volume_slider = QSlider(Qt.Horizontal)
            self.volume_slider.setMinimum(0)
            self.volume_slider.setMaximum(100)
            self.volume_slider.setValue(GVars.musicVolume)
            self.volume_slider.setFixedWidth(180)
            self.volume_slider.valueChanged.connect(self.change_music_volume)
            self.settings_layout.addWidget(self.volume_slider, alignment=Qt.AlignLeft)

            self.language_label = QLabel("Language")
            self.settings_layout.addWidget(self.language_label, alignment=Qt.AlignLeft)

            self.language_select = QComboBox()
            self.language_select.addItem("English", "en")
            self.language_select.setCurrentIndex(0)
            self.language_select.setFixedWidth(180)
            self.language_select.currentIndexChanged.connect(self.change_language)
            self.settings_layout.addWidget(self.language_select, alignment=Qt.AlignLeft)

            self.close_btn = QPushButton('Close')
            self.close_btn.setFixedWidth(128)
            self.close_btn.setStyleSheet(cssSelected)
            self.close_btn.clicked.connect(self.cancel_action)
            self.settings_layout.addWidget(self.close_btn, alignment=Qt.AlignLeft)

            self.settings_layout.addStretch()  # Push items to top
            self.lower_content_layout.insertWidget(1, self.settings_widget, alignment=Qt.AlignLeft)
            self.lower_content_layout.removeWidget(self.second_column)
            self.second_column.hide()
    
    def toggle_autocorrect(self, state):
        global QLineEdit

        self.autocorrect_Enabled = self.autocorrect_checkbox.isChecked()

        if self.autocorrect_Enabled:
            logging.info("Autocorrect enabled")
            from RESOURCES.Autocorrect import QLineEdit as AutoQLineEdit
            QLineEdit = AutoQLineEdit
        else:
            QLineEdit = QLE
            logging.info("Autocorrect disabled")

        self.second_column.show()
        self.clearLayout(self.page)
        self.initialisation()

    def change_music_volume(self, value):
        GVars.musicVolume = value
        apply_music_volume()
        self.volume_label.setText(f"Music Volume: {value}%")
        logging.info(f"Music volume set to {value}%")

    def change_language(self, index):
        language_code = self.language_select.itemData(index)
        if not language_code:
            return

        GVars.selectedLang = language_code
        logging.info(f"Language set to {self.language_select.currentText()} ({language_code})")

    def show_More_Info(self, pack_name):
        if self.info_column:
            self.lower_content_layout.removeWidget(self.info_column)
            self.info_column.deleteLater()
            self.info_column = None
        
        self.info_column = QWidget()
        self.info_column.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.info_layout = QVBoxLayout(self.info_column)
        
        self.info_layout.setContentsMargins(8, 8, 8, 8)
        self.info_layout.setSpacing(6)

        self.info_title = QLabel(f"{pack_name} - More Info")
        self.info_title.setWordWrap(True)
        self.info_title.setStyleSheet('font-weight: bold; font-size: 16px;')
        for modname, module in GVars.loadedExpansions.items():
            if modname == pack_name:
                if hasattr(module, 'Creator'):
                    self.Creator = module.Creator
                elif hasattr(module, 'creator'):
                    self.Creator = module.creator
                else:
                    self.Creator = "Cheese Master 1"

                if hasattr(module, 'Expansion'):
                    self.type = 'Expansion'
                    self.template = True
                elif hasattr(module, 'expansion'):
                    self.type = 'Expansion'
                    self.template = False
                elif hasattr(module, 'Extension'):
                    self.type = 'Extension'
                    self.template = True
                elif hasattr(module, 'extension'):
                    self.type = 'Extension'
                    self.template = False
                elif hasattr(module, 'Realm'):
                    self.type = 'Realm'
                    self.template = True
                elif hasattr(module, 'realm'):
                    self.type = 'Realm'
                    self.template = False
                else:
                    self.type = 'Unknown'
                    self.template = False

                if hasattr(module, 'version'):
                    self.version = module.version
                else:
                    self.version = 'None found'

                if hasattr(module, 'Description'):
                    self.description = module.Description
                elif hasattr(module, 'description'):
                    self.description = module.description
                else:
                    self.description = "No description available."

                self.info_Creator = QLabel(f"Creator: {self.Creator}")
                if self.template:
                    self.info_Template = QLabel(f"Template Developer: Cheese Master 1")
                else:
                    self.info_Template = None
                self.template_type = QLabel(f"Addon Type: {self.type}")
                self.version_info = QLabel(f"Version: {self.version}")
                self.info_layout.addWidget(self.info_title, alignment=Qt.AlignLeft)
                self.info_layout.addWidget(self.info_Creator, alignment=Qt.AlignLeft)
                if self.template:
                    self.info_layout.addWidget(self.info_Template, alignment=Qt.AlignLeft)
                self.info_layout.addWidget(self.version_info, alignment=Qt.AlignLeft)
                self.info_layout.addWidget(self.template_type, alignment=Qt.AlignLeft)
                self.info_description = QLabel(f"Description: {self.description}")
                self.info_description.setWordWrap(True)
                self.info_description.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
                self.info_description.adjustSize()
                self.info_description.setMinimumHeight(40)
                self.info_layout.addWidget(self.info_description, alignment=Qt.AlignLeft)
                self.close_btn = QPushButton('Close')
                self.close_btn.setFixedWidth(128)
                self.close_btn.setStyleSheet(cssSelected)
                self.close_btn.clicked.connect(self.cancel_action_singular)
                self.info_layout.addWidget(self.close_btn, alignment=Qt.AlignLeft)
                self.spacer = QWidget()
                self.info_layout.addWidget(self.spacer, stretch=1)
                self.lower_content_layout.insertWidget(2, self.info_column, alignment=Qt.AlignLeft)
        return

    def cancel_action(self):
        for attr in temp_widgets:
            if hasattr(self, attr):
                widget = getattr(self, attr)
                if widget:
                    self.first_column_layout.removeWidget(widget)
                    self.lower_content_layout.removeWidget(widget)
                    widget.deleteLater()
                    setattr(self, attr, None)

        # Reset option buttons
        for btn in getattr(self, 'button_options', []):
            if btn:
                btn.setEnabled(True)
                btn.setStyleSheet(cssSelected)  # Default cheddar

        # Clear any "clicked" button reference
        if hasattr(self, 'selected_button') and self.selected_button:
            self.selected_button = None

        if self.lower_content_layout.indexOf(self.second_column) == -1:
            self.lower_content_layout.insertWidget(1, self.second_column, alignment=Qt.AlignLeft)
        self.second_column.show()

    def cancel_action_singular(self):
        for attr in ['info_column']:
            if hasattr(self, attr):
                widget = getattr(self, attr)
                if widget:
                    self.first_column_layout.removeWidget(widget)
                    widget.deleteLater()
                    setattr(self, attr, None)

        # Reset option buttons
        for btn in getattr(self, 'button_options', []):
            if btn:
                btn.setEnabled(True)
                btn.setStyleSheet(cssSelected)  # Default cheddar

        # Clear any "clicked" button reference
        if hasattr(self, 'selected_button') and self.selected_button:
            self.selected_button = None

    def method_open_tutorial(self):
        GFuncs.func_load_game(4)
        if self.child_window is None or not self.child_window.isVisible():
            music.music.fadeout(1000)
            music.music.load(musVars.musPeaceful if GVars.room not in GVars.darkRooms else musVars.musEerie)
            self.child_window = Trl.Tutorial_UI(app_window=self)
            self.child_window.show()
            self.hide()
            music.music.play(loops=-1, fade_ms=1000)
            apply_music_volume()

    def method_open_window(self):
        #open Application_UI
        if self.child_window is None or not self.child_window.isVisible():
            music.music.fadeout(1000)
            music.music.load(musVars.musPeaceful if GVars.room not in GVars.darkRooms else musVars.musEerie)
            self.child_window = main_UI(app_window=self)
            self.child_window.show()
            self.hide()
            music.music.play(loops=-1, fade_ms=1000)
            apply_music_volume()

    def resume_current_game(self):
        if self.child_window is None:
            return

        music.music.fadeout(1000)
        music.music.load(musVars.musPeaceful if GVars.room not in GVars.darkRooms else musVars.musEerie)
        self.child_window.show()
        self.hide()
        music.music.play(loops=-1, fade_ms=1000)
        apply_music_volume()
    
    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clearLayout(item.layout())

    def open_menu(self):
        self.setStyleSheet(cssSelected)
        self.clearLayout(self.page)
        self.initialisation()
        self.show()
        music.music.load(musVars.musCredits)
        music.music.play(loops=-1, fade_ms=1000)
        apply_music_volume()

    def save_file(self, filename, slot, name):
        self.confirm_text = QLabel('Confirm Y/N? -> ')
        self.confirm = QLE()
        self.confirm.setFixedWidth(128)
        self.confirm.setStyleSheet(cssSelected)
        self.confirm.returnPressed.connect(lambda checked=False: [GFuncs.func_save_to_file(filename=filename, name=name, confirm=self.confirm.text().strip().upper()),
                                                                self.cancel_action()])
        
        self.load_layout.insertWidget(6, self.confirm_text, alignment=Qt.AlignLeft)
        self.load_layout.insertWidget(7, self.confirm, alignment=Qt.AlignLeft)

    def toggle_addon(self, pack_name, status_label):
        found = False

        for addon_category in GVars.addons:
            for category, packs in addon_category.items():
                if pack_name not in packs:
                    continue

                details = packs[pack_name]
                current_status = details.get('Status', 'Off')
                location = details.get('Location', 'Unknown')
                realm = details.get('Realm', None)

                # Toggle the status
                new_status = 'On' if current_status == 'Off' else 'Off'
                packs[pack_name] = {'Status': new_status, 'Location': location}

                # Handle Expansions
                if category == 'Expansions':
                    if new_status == 'On' and location not in GVars.addonLocations:
                        if realm:
                            for modname, module in GVars.loadedExpansions.items():
                                if hasattr(module, 'expansions') and realm == modname:
                                    if module.expansions == []:
                                        module.expansions.append(realm.upper())
                                    module.expansions.append(location)

                        else:
                            GVars.addonLocations.append(location)
                            GVars.expansions = True

                        # Load the module if it exists
                        module = GVars.loadedExpansions.get(pack_name)
                        if module and hasattr(module, 'func_Var_Loader'):
                            try:
                                module.func_Var_Loader()
                            except Exception as e:
                                logging.exception(f"Error loading {pack_name}: {e}")
                    else:
                        if not realm:
                            if location in GVars.addonLocations:
                                GVars.addonLocations.remove(location)
                                if GVars.addonLocations == ['HOUSE']:
                                    GVars.expansions = False
                                module = GVars.loadedExpansions.get(pack_name)
                                if module and hasattr(module, 'func_Var_Unloader'):
                                    try:
                                        module.func_Var_Unloader()
                                    except Exception as e:
                                        logging.exception(f"Error unloading {pack_name}: {e}")
                        else:
                            for modname, module in GVars.loadedExpansions.items():
                                if hasattr(module, 'expansions') and realm == modname:
                                    if location in module.expansions:
                                        module.expansions.remove(location)
                                        if len(module.expansions) == 1:
                                            module.expansions = []
                                    if hasattr(module, 'func_Var_Unloader'):
                                        try:
                                            module.func_Var_Unloader()
                                        except Exception as e:
                                            logging.exception(f"Error unloading {pack_name}: {e}")

                # Handle realms
                elif category == 'Realms':
                    module = GVars.loadedExpansions.get(pack_name, None)
                    if module:
                        try:
                            if new_status == 'On' and hasattr(module, 'func_Var_Loader'):
                                module.func_Var_Loader()
                            elif new_status == 'Off' and hasattr(module, 'func_Var_Unloader'):
                                module.func_Var_Unloader()
                        except Exception as e:
                            logging.exception(f"Error toggling {pack_name}: {e}")

                # Handle Extensions
                elif category == 'Extensions':
                    module = GVars.loadedExpansions.get(pack_name)
                    if module:
                        try:
                            if new_status == 'On' and hasattr(module, 'func_Var_Loader'):
                                module.func_Var_Loader()
                            elif new_status == 'Off' and hasattr(module, 'func_Var_Unloader'):
                                module.func_Var_Unloader()
                        except Exception as e:
                            logging.exception(f"Error toggling {pack_name}: {e}")

                # Update status label
                status_label.setText(f"Status: {new_status}")
                logging.debug(f"Toggled {pack_name} to {new_status}")
                found = True
                break
            if found:
                break

        if not found:
            logging.error(f"Pack {pack_name} not found.")
            status_label.setText("Not found")

class main_UI(QWidget):
    def __init__(self, app_window):
        super().__init__()

        global cssSelected
        self.appWindow = app_window
        self.child_window = None
        varLoading = []
        self.ending_ending = False

        for dictionary in GVars.addons:
            for typ, values in dictionary.items():
                for pack, data in values.items():
                    if data['Status'] == 'On':
                        varLoading.append(pack)
        for modname, module in GVars.loadedExpansions.items():
            if modname in varLoading and hasattr(module, 'func_Var_Loader'):
                module.func_Var_Loader()


        for modname, module in GVars.loadedExpansions.items():
            if hasattr(module, 'addon'):
                first_addon = next(iter(module.addon.values()))
                location = first_addon.get('Location', None)
                if location == GVars.expansionLoc:
                    self.rooms = module.rooms
                    self.roomAttributes = module.roomAttributes
                    self.lootBoxes = module.lootBoxes
                    cssSelected = module.cssModule if hasattr(module, 'cssModule') else cssSelected
                    break
        else:
            self.rooms = rooms
            self.roomAttributes = roomAttributes
            self.lootBoxes = lootBoxes

        self.setWindowTitle('Cut The Cheese 2')
        self.setStyleSheet(cssSelected)
        self.setMinimumSize(720, 640)
        self.page = QVBoxLayout()
        self.setLayout(self.page)

        self.initialisation(self.page)

    def initialisation(self, layout):
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
                    module._realm(GVars.room, self)
                    self.Location.setText(GVars.room)
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

        self.stats_layout.setContentsMargins(4, 4, 4, 4)
        self.stats_layout.setSpacing(4)

        self.stats_layout.addWidget(self.Health, alignment=Qt.AlignLeft)
        self.stats_layout.addWidget(self.Equipped, alignment=Qt.AlignLeft)
        self.stats_layout.addWidget(self.Wearing, alignment=Qt.AlignLeft)
        self.stats_layout.addWidget(self.Description, alignment=Qt.AlignLeft)

        for modname, module in GVars.loadedExpansions.items():
            for categories in GVars.addons:
                for category, packs in categories.items():
                    for packname, items in packs.items():
                        if packname == modname and items.get('Status', 'Off') == 'On':
                            if  hasattr(module, 'add_label'):
                                module.add_label(self=self, layout=self.stats_layout)
        
        self.page.addWidget(self.stats_Widget)
        self.page.addWidget(self.column_widget)

        self.button_options = []

        self.otherOption = QLineEdit()
        self.otherOption.setStyleSheet(cssSelected)
        self.content.addWidget(self.otherOption, alignment=Qt.AlignLeft)
        self.otherOption.returnPressed.connect(lambda: self.handle_runtime(choice=self.otherOption.text().strip().title()))

        for key, option in self.options.items():
            if key != 'Location' and key != 'Description' and key != '8':
                if key != '9':
                    self.option = QPushButton(option)
                    self.option.setStyleSheet(cssSelected)
                    self.option.setFixedWidth(128)
                    self.content.addWidget(self.option, alignment=Qt.AlignLeft)
                    self.option.clicked.connect(lambda checked, btn=self.option, k=key, o=option: self.handle_option_click(k, o, btn))
                    self.button_options.append(self.option)

                else:
                    self.option = QPushButton('8 = help')
                    self.option.setStyleSheet(cssSelected)
                    self.option.setFixedWidth(128)
                    self.content.addWidget(self.option, alignment=Qt.AlignLeft)
                    self.option.clicked.connect(lambda checked, btn=self.option, k='8', o=option: self.handle_option_click(k, o, btn))
                    self.button_options.append(self.option)


        self.spacerOption = QWidget()
        self.content.addWidget(self.spacerOption, stretch=1)

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.columns.addItem(self.spacer)

        self.right_side = QWidget()
        self.right_layout = QVBoxLayout(self.right_side)

        self.inv_widget = QWidget()
        self.inv_widget.setObjectName('inv_widget')
        self.inv_widget.setMinimumWidth(128)
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
        self.right_layout.addWidget(self.inv_widget, alignment=Qt.AlignRight)

        self.report = QPushButton('Report Bug')
        self.report.setStyleSheet(cssSelected)
        self.report.setFixedWidth(128)
        self.right_layout.addWidget(self.report, alignment=Qt.AlignRight)
        self.report.clicked.connect(lambda: webbrowser.open("https://itch.io/t/5366449/v2-bugs"))
        self.report.setToolTip(f"Click here if something went wrong!")

        #self.spacer = QWidget()
        #self.right_layout.addWidget(self.spacer, stretch=1)

        self.columns.addWidget(self.right_side, alignment=Qt.AlignRight)
               
    def handle_option_click(self, key=0, option='', button=None):
        self.cancel_action()
        
        # Reset all buttons: enable and set normal style
        for btn in self.button_options:
            btn.setEnabled(True)
            btn.setStyleSheet(cssSelected)  # normal style

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
            self.input.setStyleSheet(cssSelected)
            self.roomsListLayout.addWidget(self.input, len(doors), 0)
            self.input.returnPressed.connect(lambda: self.method_enter_room(self.input.text().upper()))

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(cssSelected)
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
            self.input.setStyleSheet(cssSelected)
            self.storageListLayout.addWidget(self.input, len(storageData), 0)
            self.input.returnPressed.connect(lambda: self.method_open_loot(self.input.text().strip()))
            
            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(cssSelected)
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
                    self.itemInput.setStyleSheet(cssSelected)
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
                    self.cancel.setStyleSheet(cssSelected)
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
                elif itemType == 'Beverage':
                    nHealth = GVars.Health + int(itemDetails['Health'])
                    print(GFuncs.t(f"Health: {nHealth} = {GVars.Health} + {int(itemDetails['Health'])}"))
                    if nHealth > GVars.maxHealth:
                        GVars.Health = GVars.maxHealth
                        logging.info(f"Maxhealth {GVars.maxHealth} reached")
                    else:
                        GVars.Health = nHealth

                    itemDetails['Count'] -= 1
                    if itemDetails['Count'] == 0:
                        GVars.inventory[item] -= 1
                        del GVars.itemCopies[item]
                        GVars.equipped = ''
                    logging.info(f"Item count decreased")
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
                    self.cancel.setStyleSheet(cssSelected)
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
                self.kcancel_action()
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
            self.equipInput.setStyleSheet(cssSelected)
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
                                                         self.cancel_action())))
                    )()
                )
            )
            self.equipListLayout.addWidget(self.equipInput)

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(cssSelected)
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
            self.cancel.setStyleSheet(cssSelected)
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
            self.dropInput.setStyleSheet(cssSelected)
            self.dropInput.returnPressed.connect(lambda: self.method_handle_dropables('Drop', self.dropInput.text().strip().title()))
            self.dropWidgetLayout.addWidget(self.dropInput, alignment=Qt.AlignLeft)

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(cssSelected)
            self.dropWidgetLayout.addWidget(self.cancel)
            self.cancel.clicked.connect(self.cancel_action)

            self.dropSpacer = QWidget()
            self.dropWidgetLayout.addWidget(self.dropSpacer, stretch=1)
            self.columns.insertWidget(1, self.dropWidget, alignment=Qt.AlignLeft)
        #menu
        elif choice == 7:
            self.open_menu()
        #help
        elif choice == 8:
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
            #self.helpListLayout.addWidget(QLabel('8 = View the current contents of your inventory'))
            self.helpListLayout.setContentsMargins(0,0,0,0)

            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(cssSelected)
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
            self.craftInput.setStyleSheet(cssSelected)
            self.craftInput.returnPressed.connect(lambda: self.handle_crafting(self.craftInput.text().strip().title()))
            self.craftLayout.addWidget(self.craftInput, alignment=Qt.AlignLeft)

            self.cancel = QPushButton('Cancel')
            self.cancel.setStyleSheet(cssSelected)
            self.cancel.setFixedWidth(128)
            self.cancel.clicked.connect(self.cancel_action)
            self.craftLayout.addWidget(self.cancel, alignment=Qt.AlignLeft)

            self.spacer = QWidget()
            self.craftLayout.addWidget(self.spacer, stretch=1)

            self.columns.insertWidget(1, self.craftWidget, alignment=Qt.AlignLeft)
        #item description
        elif choice == 'Description':
            self.active_popup = True
            self.descWidget = QWidget()
            self.descLayout = QVBoxLayout(self.descWidget)
            self.descTitle = QLabel('Item Description')
            self.descLayout.addWidget(self.descTitle, alignment=Qt.AlignLeft)

            item_desc = next(
                (det['Description'] for det in GVars.itemProperties
                if det.get('Description') is not None and det.get('Item') == GVars.equipped),
                "No description available."
            )
            self.itemLabel = QLabel(f"{GVars.equipped}: {item_desc}")
            self.itemLabel.setWordWrap(True)
            self.descLayout.addWidget(self.itemLabel, alignment=Qt.AlignLeft)

            self.cancel = QPushButton('Cancel')
            self.cancel.setStyleSheet(cssSelected)
            self.cancel.setFixedWidth(128)
            self.cancel.clicked.connect(self.cancel_action)
            self.descLayout.addWidget(self.cancel, alignment=Qt.AlignLeft)

            self.spacer = QWidget()
            self.descLayout.addWidget(self.spacer, stretch=1)

            self.columns.insertWidget(1, self.descWidget, alignment=Qt.AlignLeft, stretch=1)
        
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
                btn.setStyleSheet(cssSelected)

        self.active_popup = False

    def handle_crafting(self, craft):
        # Check if crafting requirements are met
        req = GVars.craftables.get(craft, None)
        if req is not None:
            crafting = {craft : req}
            for item in req:
                if item in GVars.inventory.keys():
                    if next(det['Type'] for det in GVars.itemProperties if det['Item'] == item) == 'Food' and GVars.itemCopies.get(item, {}).get('Cut', False):
                        continue
                    elif next(det['Type'] for det in GVars.itemProperties if det['Item'] == item) not in ['Recipe', 'Spawner', 'Food']:
                        continue
                    else:
                        logging.error(f"Crafting requirement {item} not met due to incorrect type or not cut")
                        self.craftLayout.removeWidget(self.spacer)
                        self.errorLabel = QLabel(f"Crafting requirements for {craft} not met.\nThis could be an uncut food item\nOr an item type mismatch...\n\nIf the item is cut and you beleive it is the right type, \nreport it by clicking the button below the inventory tab")
                        self.craftLayout.addWidget(self.errorLabel, alignment=Qt.AlignLeft)
                        self.craftLayout.addWidget(self.spacer, stretch=1)
                        return
                else:
                    logging.info(f"Crafting requirements for {craft} not met")
                    self.craftLayout.removeWidget(self.spacer)
                    self.errorLabel = QLabel(f"Crafting requirements for {craft} not met.\n An item missing from inventory...")
                    self.craftLayout.addWidget(self.errorLabel, alignment=Qt.AlignLeft)
                    self.craftLayout.addWidget(self.spacer, stretch=1)
                    return
        else:
            logging.error(f"Crafting recipe for {craft} not found")
            self.craftLayout.removeWidget(self.spacer)
            self.errorLabel = QLabel(f"Crafting recipe for {craft} not found...\n\nIf that is not what you typed, \nreport this by clicking the button below the inventory tab...\nUnless you typed gibberish, then stop doing that...")
            self.craftLayout.addWidget(self.errorLabel, alignment=Qt.AlignLeft)
            self.craftLayout.addWidget(self.spacer, stretch=1)
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

        self.clearLayout(self.page)
        self.initialisation(self.page)
        self.cancel_action()
                
    def method_enter_room(self, room_input, addon=False):
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
                            module._realm(GVars.room, self)
                else:
                    self.options = next(loc for loc in self.rooms if loc['Location'] == GVars.room)
                desc = self.options.get('Description', 'No description available')
                self.Description.setText(desc)
                self.Description.setWordWrap(True)
                self.Description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.Description.setMaximumHeight(100)

                if GVars.room in GVars.darkRooms:
                    music.music.fadeout(1000)
                    music.music.load(musVars.musPeaceful if GVars.room not in GVars.darkRooms else musVars.musEerie)
                    music.music.play(-1, fade_ms=1000)
                    apply_music_volume()
                elif prevroom in GVars.darkRooms and GVars.room not in GVars.darkRooms:
                    music.music.fadeout(1000)
                    music.music.load(musVars.musPeaceful)
                    music.music.play(-1, fade_ms=1000)
                    apply_music_volume()

                self.button_options.clear()
                for key, option in self.options.items():
                    if key not in ['Location', 'Description']:
                        btn = QPushButton(option)
                        btn.setStyleSheet(cssSelected)
                        btn.setFixedWidth(128)
                        self.content.addWidget(btn, alignment=Qt.AlignLeft)
                        btn.clicked.connect(lambda checked, b=btn, k=key, o=option: self.handle_option_click(k, o, b))
                        self.button_options.append(btn)
                self.content.addWidget(self.spacerOption, stretch=1)
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
                    self.addon_input.setStyleSheet(cssSelected)
                    self.addon_layout.addWidget(self.addon_input, alignment=Qt.AlignLeft)

                    # Inline connection to set module and update room/attributes/lootBoxes
                    self.addon_input.returnPressed.connect(lambda checked=False: self.enter_addon(new_room=self.addon_input.text().strip().upper()))

                    self.spacer = QWidget()
                    self.addon_layout.addWidget(self.spacer, stretch=1)

                    self.columns.insertWidget(2, self.addon_widget, alignment=Qt.AlignLeft)
        else:
            for modname, module in GVars.loadedExpansions.items():
                if hasattr(module, 'realm_addon') and hasattr(module, 'realm') and modname == GVars.realm:
                    module.realm_addon(GVars.room, self)
                    module._realm(GVars.room, self)

        if not GVars.ending:
            self.end_of_turn()

        # Refresh main UI
        if (not GVars.ending or not self.ending_ending) and (GVars.room not in GVars.vehicleVariants or not GVars.expansions):
            self.cancel_action()
            self.clearLayout(self.page)
            self.initialisation(self.page)
            self.active_popup = False
        
    def method_open_loot(self, storage):
        try:
            #if any(storage == drop['Storage'] for drop in GVars.dropables):
            #    storage = 
            if sum(GVars.inventory.values()) < GVars.inventoryLen:
                STORAGE = storage.upper()
                Storage = storage.title()
                dropable = [d for d in GVars.dropables if d['Storage'] == STORAGE or d['Storage'] == Storage]
                if not dropable:
                    for room in self.roomAttributes:
                        if room['Location'] == GVars.room:
                            if Storage not in room['Storage'] and STORAGE not in room['Storage']:
                                logging.error(f"Storage {storage} not found in room {GVars.room}")
                                errorMsg = QLabel(f"Storage not found...")
                                errorMsg.setFixedWidth(128)
                                self.storageListLayout.addWidget(errorMsg, 0, 0)
                                return

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
        except Exception as e:
            logging.exception(f"Something went wrong with opening loot: {e}")
            self.error = QLabel(f"Something went wrong...")
            self.error.setFixedWidth(128)
            self.storageListLayout.addWidget(self.error, 0, 0)

            #self.cancel_action()
            self.clearLayout(self.page)
            self.initialisation(self.page)

    def ending_credits(self):
        self.ending_ending = True
        self.clearLayout(self.page)
        self.setStyleSheet("""
                           font-size: 16px;
                           background-color: #cc9900;
                           """)
        if GVars.Health > 0:    
            self.ending = QLabel(f"\n\nYOU WIN!!!\nYou won the {GVars.ending} way!\n\n\n")
        elif GVars.Health <= 0:
            self.ending = QLabel(f"\n\nGAME OVER...\nYou  were...  {GVars.ending}...\n\n\n")
        self.ending.setAlignment(Qt.AlignCenter)
        self.page.addWidget(self.ending)
        for credit in credits:
            self.creditLabel = QLabel(credit)
            self.creditLabel.setWordWrap(True)  # allow multi-line wrap
            self.creditLabel.setAlignment(Qt.AlignCenter)  # center horizontally
            self.creditLabel.setStyleSheet("margin-bottom: 10px;")  # add some vertical spacing
            self.page.addWidget(self.creditLabel)
        self.page.addWidget(QLabel('\nHall Of Cheese'), alignment=Qt.AlignCenter)
        for name in hallOfCheese:
            self.hallLabel = QLabel(name)
            self.hallLabel.setWordWrap(True)  # allow multi-line wrap
            self.hallLabel.setAlignment(Qt.AlignCenter)  # center horizontally
            self.hallLabel.setStyleSheet("margin-bottom: 10px;")  # add some vertical spacing
            self.page.addWidget(self.hallLabel)
        self.page.addWidget(QLabel('\n Dustbound Challenge Leaderboard'), alignment=Qt.AlignCenter)
        for rank, player in DBLeaderboard.items():
            self.leaderLabel = QLabel(f"{rank}: {player}")
            self.leaderLabel.setWordWrap(True)
            self.leaderLabel.setAlignment(Qt.AlignCenter)
            self.leaderLabel.setStyleSheet("margin-bottom: 10px;")
            self.page.addWidget(self.leaderLabel)
        if GVars.ending != 'Jokester':
            self.subtextLabel = QLabel('\n\n\nBut you should have cut the cheese...\nAs you were told...')
        else:
            self.subtextLabel = QLabel('\n\n\nYou cut the cheese...\nNice work...')
        self.subtextLabel.setAlignment(Qt.AlignCenter)
        self.page.addWidget(self.subtextLabel)

        self.spacerCredit = QWidget()
        self.page.addWidget(self.spacerCredit, stretch=1)
    
    def method_handle_dropables(self, action, item):
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
            self.dropInput.setStyleSheet(cssSelected)
            self.dropInput.returnPressed.connect(lambda: (
                # Ending check
                (setattr(GVars, 'ending', 'Dumbass') or True) and self.ending_credits()
                if item == self.dropInput.text().strip().title() else (
                    # Attempt to store item
                    (lambda: (
                        [(d['Loot'].append(item), 
                        GVars.inventory.__setitem__(item, GVars.inventory.get(item, 0) - 1),
                        GVars.inventory.pop(item) if GVars.inventory.get(item, 0) <= 0 else None
                        )
                        for d in GVars.dropables
                        for p in GVars.itemProperties
                        if d['Storage'] == self.dropInput.text().strip().title()
                        and p['Item'] == self.dropInput.text().strip().title()
                        and len(d['Loot']) < p['Slots']
                        and item in GVars.inventory
                        ]
                    ))(),
                ),
                # Cancel action
                self.cancel_action(),
                self.clearLayout(self.page),
                self.initialisation(self.page),
                # Logging
                logging.info(f"Dropable {self.dropInput.text().strip().title()} has stored {item}")
            ))
            self.dropListLayout.addWidget(self.dropInput, alignment=Qt.AlignLeft)

            # Add Cancel button right after doors
            self.cancel = QPushButton('Cancel')
            self.cancel.setFixedWidth(128)
            self.cancel.setStyleSheet(cssSelected)
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

    def enter_addon(self, new_room):
        global cssSelected
        if new_room != 'HOUSE' and not new_room.endswith('REALM'):
            for modname, module in GVars.loadedExpansions.items():
                if hasattr(module, 'rooms') and any(loc['Location'] == new_room for loc in module.rooms):
                    GVars.expansionLoc = new_room
                    GVars.room = new_room
                    self.rooms = module.rooms
                    self.roomAttributes = module.roomAttributes
                    self.lootBoxes = module.lootBoxes
                    cssSelected = module.cssModule if hasattr(module, 'cssModule') else cssSelected

                    QTimer.singleShot(50, lambda: self.initialisation(self.page))

                    self.setStyleSheet(cssSelected)
                    self.cancel_action()
                    self.clearLayout(self.page)
                    self.initialisation(self.page)
                    
                    logging.info(f"Addon {modname} entered...")
                    break
            else:
                logging.error(f"Could not find room {new_room} in any loaded addons")
                self.errorMsg = QLabel(f"Invalid Room...")
                if hasattr(self, 'addon_layout'):
                    self.addon_layout.insertWidget(len(GVars.addonLocations)+2, self.errorMsg, alignment=Qt.AlignLeft)
                    QTimer.singleShot(1000, lambda: (self.addon_layout.removeWidget(self.errorMsg),
                    self.errorMsg.deleteLater()))
                    self.addon_input.clear()
        elif new_room == 'HOUSE':
            GVars.expansionLoc = new_room
            GVars.room = 'GARAGE'
            self.rooms = rooms
            self.roomAttributes = roomAttributes
            self.lootBoxes = lootBoxes
            cssSelected = cssMain

            self.setStyleSheet(cssSelected)
            self.cancel_action()
            self.clearLayout(self.page)
            self.initialisation(self.page)  

            logging.info(f"Returned to main game from addon...")
        elif new_room.endswith('REALM'):
            for modname, module in GVars.loadedExpansions.items():
                if modname == new_room and hasattr(module, 'return_'):
                    module.return_(new_room, self)
                    
    def open_menu(self):
        if not self.isVisible():
            self.show()
        music.music.fadeout(1000)
        music.music.load(musVars.musCredits)
        self.appWindow.open_menu()
        self.hide()
        music.music.play(-1, fade_ms=1000)
        apply_music_volume()

    def end_of_turn(self):
        global prevroom
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
                    playerDoorsC = next((room['Doors'] for room in roomAttributes if room['Location'] == GVars.room), [])
                    playerDoorsP = next((room['Doors'] for room in roomAttributes if room['Location'] == prevroom), [])
                    enemyDoors = next((room['Doors'] for room in roomAttributes if room['Location'] == current_room), [])

                    matchCE = next((door for door in playerDoorsC if door in enemyDoors), None)
                    matchPE = next((door for door in playerDoorsP if door in enemyDoors), None)

                    matchC = GVars.room if GVars.room in enemyDoors else None
                    matchP = prevroom if prevroom in enemyDoors else None

                    if matchC:
                        next_room = matchC
                        #logging.debug(f"match for current room")
                    elif matchP:
                        #logging.debug(f"match for prev room")
                        next_room = matchP
                    elif matchCE:
                        #logging.debug(f"match for current doors")
                        next_room = matchCE
                    elif matchPE:
                        #logging.debug(f"match for previous doors")
                        next_room = matchPE
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
                prm = inspect.signature(module.conditions)
                if len(prm.parameters) >= 1:
                    module.conditions(self)
                else:
                    module.conditions()

    def resume_main_game(self):
        self.show()

    def method_open_window(self, enemy):
        #open Application_UI
        if self.child_window is None or not self.child_window.isVisible():
            music.music.fadeout(1000)
            music.music.load(musVars.musBoss)
            self.child_window = fighting_UI(app_window=self, enemy_name=enemy)
            self.child_window.show()
            self.hide()
            music.music.play(-1, fade_ms=1000)
            apply_music_volume()

class fighting_UI(QWidget):
    def __init__(self, app_window, enemy_name):
        super().__init__()
        self.appWindow = app_window
        self.enemy_name = enemy_name
        self.enemy_data = GVars.enemies[self.enemy_name]
        
        global cssBattle
        self.setWindowTitle(f"Battle Mode")
        self.setStyleSheet(cssBattle)
        self.setMinimumSize(720, 640)
        self.window_layout = QVBoxLayout()
        self.setLayout(self.window_layout)

        self.initialisation(self.window_layout)

    def initialisation(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clearLayout(item.layout())
        
        self.upper_content = QWidget()
        self.upper_layout = QVBoxLayout(self.upper_content)
        
        self.title = QLabel(f"BATTLE - {self.enemy_name}\n{self.enemy_name} Health: {self.enemy_data['Health']}")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.upper_layout.addWidget(self.title, alignment=Qt.AlignLeft)
        
        self.Health = QLabel(f"Health: %{GVars.Health}")
        self.Health.setStyleSheet('font-weight: bold;')
        self.Health.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Equipped = QLabel(f"Equipped: [{GVars.equipped}]")
        self.Equipped.setStyleSheet('font-weight: bold;')
        self.Equipped.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Wearing = QLabel(f"Wearing: [{GVars.wearing}]")
        self.Wearing.setStyleSheet('font-weight: bold;')
        self.Wearing.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.upper_layout.addWidget(self.Health, alignment=Qt.AlignLeft)
        self.upper_layout.addWidget(self.Equipped, alignment=Qt.AlignLeft)
        self.upper_layout.addWidget(self.Wearing, alignment=Qt.AlignLeft)

        self.lower_content = QWidget()
        self.lower_layout = QHBoxLayout(self.lower_content)
        self.options_widget = QWidget()
        self.options_layout = QVBoxLayout(self.options_widget)

        self.wait = QPushButton('0 = Wait')
        self.wait.setStyleSheet(cssBattle)
        self.wait.setFixedWidth(128)
        self.options_layout.addWidget(self.wait, alignment=Qt.AlignLeft)
        self.wait.clicked.connect(lambda: self.handle_battle_runtime(0))

        self.use = QPushButton('1 = Use Item')
        self.use.setStyleSheet(cssBattle)
        self.use.setFixedWidth(128)
        self.options_layout.addWidget(self.use, alignment=Qt.AlignLeft)
        self.use.clicked.connect(lambda: self.handle_battle_runtime(1))

        self.equip = QPushButton('2 = Equip Item')
        self.equip.setStyleSheet(cssBattle)
        self.equip.setFixedWidth(128)
        self.options_layout.addWidget(self.equip, alignment=Qt.AlignLeft)
        self.equip.clicked.connect(lambda: self.handle_battle_runtime(2))

        self.menu = QPushButton('3 = Open Menu')
        self.menu.setStyleSheet(cssBattle)
        self.menu.setFixedWidth(128)
        self.options_layout.addWidget(self.menu, alignment=Qt.AlignLeft)
        self.menu.clicked.connect(lambda: self.handle_battle_runtime(3))

        self.spacer = QWidget()
        self.options_layout.addWidget(self.spacer, stretch=1)
        self.columnSpacer = QWidget()
        self.lower_layout.addWidget(self.options_widget, alignment=Qt.AlignLeft)
        self.lower_layout.addWidget(self.columnSpacer, stretch=1)
        self.window_layout.addWidget(self.upper_content)
        self.window_layout.addWidget(self.lower_content)

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
        self.lower_layout.addWidget(self.inv_widget, alignment=Qt.AlignLeft)

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

        self.active_popup = False

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clearLayout(item.layout())

    def handle_battle_runtime(self, action):
        self.cancel_action()
        
        #wait
        if action == 0:
            QTimer.singleShot(1000, lambda: None)
            self.cancel_action()
        #use item
        elif action == 1:
            if GVars.equipped:
                for item, properties in GVars.itemCopies.items():
                    if item == GVars.equipped:
                        itemType = properties['Type']
                        itemName = properties['Item']
                        itemDetails = properties
                        break

                if itemType == 'Weapon':
                    self.enemy_data['Health'] = self.enemy_data['Health'] - int(itemDetails['Damage'])
                    itemDetails['Count'] -= 1
                    self.title.setText(f"BATTLE - {self.enemy_name}\n{self.enemy_name} Health: {self.enemy_data['Health']}")
                    
                elif itemType == 'Food':
                    nHealth = GVars.Health + itemDetails['Health']
                    self.Health.setText(f"Health: {GVars.Health}% + {itemDetails['Health']}%")
                    if nHealth > GVars.maxHealth:
                        GVars.Health = GVars.maxHealth
                    else:
                        GVars.Health = nHealth
                    QTimer.singleShot(1000, lambda: (self.Health.setText(f"Health: {GVars.Health}%")))
                    nHealth = 0
                    itemDetails['Count'] -= 1
                    
                elif itemType == 'Effect':
                    if itemDetails['Effect'] == 'Strength':
                        GVars.maxHealth += 50
                        GVars.inventoryLen += 5
                        logging.info(f"Strength buff activated")
                        itemDetails['Count'] = itemDetails['Count'] - 1
                        logging.info(f"Item count decreased")
                    elif itemDetails['Effect'] == 'Health':
                        nHealth = GVars.Health + itemDetails['Health']
                        self.Health.setText(f"Health: {GVars.Health}% + {itemDetails['Health']}%")
                        if nHealth > GVars.maxHealth:
                            GVars.Health = GVars.maxHealth
                        else:
                            GVars.Health = nHealth
                        QTimer.singleShot(1000, lambda: (self.Health.setText(f"Health: {GVars.Health}%")))
                        nHealth = 0
                        logging.info(f"Healed {itemDetails['Health']}")
                        itemDetails['Count'] = itemDetails['Count'] - 1
                    elif itemDetails['Effect'] == 'Damage':
                        nHealth = GVars.Health - random.randint(10, 15)
                        self.Health.setText(f"Health: {GVars.Health}% - {GVars.Health - nHealth}%")
                        GVars.Health = nHealth
                        logging.info(f"Took effect damage {GVars.Health - nHealth}")
                        QTimer.singleShot(1000, lambda: (self.Health.setText(f"Health: {GVars.Health}%")))
                        nHealth = 0
                        itemDetails['Count'] = itemDetails['Count'] - 1
                    elif itemDetails['Effect'] == 'Resistance':
                        GVars.resistance = 0.20
                        logging.info(f"Resistance applied")
                        itemDetails['Count'] = itemDetails['Count'] - 1
                    elif itemDetails['Effect'] == 'Weakness':
                        GVars.resistance -= 0.20
                        logging.info(f"Weakness applied")
                        itemDetails['Count'] = itemDetails['Count'] - 1
                    else:
                        self.error = QLabel(f"Cannot use {itemDetails['Item']} in battle...")
                        self.lower_layout.addWidget(self.error, alignment=Qt.AlignLeft)
                        QTimer.singleShot(1000, lambda: (self.lower_layout.removeWidget(self.error),
                                                         self.error.deleteLater()))

                else:
                    self.error = QLabel(f"Cannot use {itemDetails['Item']} in battle...")
                    self.lower_layout.addWidget(self.error, alignment=Qt.AlignLeft)
                    QTimer.singleShot(1000, lambda: (self.lower_layout.removeWidget(self.error),
                                                        self.error.deleteLater()))
                        
                if itemDetails['Count'] == 0:
                    GVars.inventory[itemName] -= 1
                    del GVars.itemCopies[itemName]
                    GVars.equipped = ''
                    if GVars.inventory[itemName] == 0:
                        del GVars.inventory[itemName]
        #equip item
        elif action == 2:
            self.equip_widget = QWidget()
            self.equip_layout = QVBoxLayout(self.equip_widget)
            self.label = QLabel(f"Equip what? -> ")
            self.equip_layout.addWidget(self.label, alignment=Qt.AlignLeft)

            for item, count in GVars.inventory.items():
                self.item_label = QLabel(item)
                self.equip_layout.addWidget(self.item_label, alignment=Qt.AlignLeft)
            
            self.input = QLineEdit()
            self.input.setFixedWidth(128)
            self.input.setStyleSheet(cssBattle) 
            self.input.returnPressed.connect(
                lambda: (
                    (lambda lbl=QLabel("Failed to equip"):
                        (self.equip_layout.insertWidget(0, lbl, alignment=Qt.AlignLeft),
                        QTimer.singleShot(1000, lambda: (self.equip_layout.removeWidget(lbl), lbl.deleteLater())))
                    )()
                ) if not GFuncs.func_equip_iem(self.input.text().strip().title()) else (
                    (lambda lbl=QLabel("Equipped"):
                        (self.equip_layout.insertWidget(0, lbl, alignment=Qt.AlignLeft),
                        QTimer.singleShot(1000, lambda: (self.equip_layout.removeWidget(lbl), 
                                                         lbl.deleteLater(), 
                                                         self.clearLayout(self.window_layout),
                                                         self.initialisation(self.window_layout))))
                    )()
                )
            )
            self.equip_layout.addWidget(self.input, alignment=Qt.AlignLeft)

            self.cancel = QPushButton('Cancel')
            self.cancel.setStyleSheet(cssBattle)
            self.cancel.setFixedWidth(128)
            self.cancel.clicked.connect(lambda: self.cancel_action())
            self.equip_layout.addWidget(self.cancel, alignment=Qt.AlignLeft)

            self.spacer = QWidget()
            self.equip_layout.addWidget(self.spacer, stretch=1)

            self.lower_layout.insertWidget(1, self.equip_widget, alignment=Qt.AlignLeft)
        #menu
        elif action == 3:
            self.open_menu()

        if action in [0, 1]:
            nHealth = GVars.Health - int(self.enemy_data['Damage']*(1-GVars.resistance))
            self.Health.setText(f"Health: {GVars.Health}% - {GVars.Health - nHealth}%")
            GVars.Health = nHealth
            QTimer.singleShot(1000, lambda: (self.Health.setText(f"Health: {GVars.Health}%")))
            nHealth = 0
        
        self.end_of_turn()

    def open_menu(self):
        self.appWindow.open_menu()
        self.hide()
    
    def open_main_ui(self):
        music.music.fadeout(1000)
        music.music.load(musVars.musPeaceful if GVars.room not in GVars.darkRooms else musVars.musEerie)
        self.appWindow.resume_main_game()
        self.hide()
        music.music.play(-1, fade_ms=1000)
        apply_music_volume()

    def end_of_turn(self):
        #double check inventory cleanup
        items_to_remove = [item for item, count in GVars.inventory.items() if count <= 0]
        for item in items_to_remove:
            del GVars.inventory[item]

            # Remove from itemCopies if it exists
            if item in GVars.itemCopies:
                del GVars.itemCopies[item]

            # Clear equipped if it was this item
            if GVars.equipped == item:
                GVars.equipped = ''
        #enemy death check
        if self.enemy_data['Health'] <= 0:
            self.enemy_data['Defeated'] = True
            self.enemy_data['Exists'] = False
            self.enemy_data['Room'] = ''
            GVars.ending = self.enemy_data['Ending']
            logging.info(f"Enemy {self.enemy_name} defeated")
            self.open_main_ui()
        #player death check
        if GVars.Health <= 0:
            GVars.ending = 'Slaughtered'
            if GVars.Health <= -5:
                GVars.ending = 'Poked'
            self.open_main_ui()
            self.appWindow.ending_credits()
        #conditions
        for modname, module in GVars.loadedExpansions.items():
            if hasattr(module, 'battle_conditions'):
                logging.info(f"Checking battle conditions for {modname}...") #\n{inspect.getsource(module.battle_conditions)}")
                module.battle_conditions()


cssBattle = """
QWidget {
    background-color: #d18c00;  /* slightly more reddish than #cc9900 */
}

QPushButton {
    background-color: #b36600;  /* just a touch redder than #b27f00 */
}

QLineEdit {
    background-color: #ffe066;  /* soft warm yellow with a hint of red */
}
"""
cssMain = """
    QWidget {
        background-color: #cc9900;
    }

    QPushButton {
        background-color: #b27f00;
    }

    QPushButton:hover {
        background-color: #d1a300;
    }
    
    QLineEdit {
        background-color: #ffeb88;
    }    
    """
cssSelected = cssMain
