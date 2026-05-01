import random
import AUDIO.musicVars as musVars

totalCheeseCount = 3
cheeseTotal = 0
selectedMus = musVars.musCredits
musicVolume = 100

resistance = 0
Health, maxHealth, inventoryLen, cheeseTolerance = 100, 100, 10, 0
gameEnd, expansions, returning, stored = False, False, False, False
equipped, ending, sendToRoom, wearing = '', '', '', ''

addons = [{'Expansions' : {}}, {'Extensions' : {}}, {'Realms' : {}}]
realm = 'Overworld'
vehicleVariants = ['VEHICLE']
darkRooms = ['CAVE', 'CAVERNS', 'BASEMENT', 'TUNNELS']
itemCopies = {}
loadedExpansions = {}
craftables = {'Sandwich' : ['Ham', 'Cheese', 'Bread'], 'Slipper' : ['Belt', 'Cannon', 'Stick'], 'Apple Juice' : ['Apple', 'Water Bottle']}
dropables = [{'Storage' : 'Sack', 'Loot' : ['Cheese']}, {'Storage' : 'Box', 'Loot' : []}]
enemies = {'Demon' : {'Health' : 0, 'Room' : '', 'Exists' : False, 'Location' : '', 'Damage' : 10, 'Restrictions' : ['VEHICLE'], 'Defeated' : False, 'Ending' : 'Demon Slayer', 'HRange' : [100, 110, 120, 130, 140, 150], 'Drop' : ''}}

itemProperties = [{'Item' : 'Sack', 'Type' : 'Container', 'Slots' : 3, 'Count' : -1, 'Description' : 'A small bundle of leather shaped like a pouch, particularly useful for carrying a few items.'},
                  {'Item' : 'Sword', 'Type' : 'Weapon', 'Damage' : 30, 'Count' : -1, 'Cutting' : True, 'Description' : 'A peice of steel, molded into the perfect shape resembling that of a longsword. It is clean enough to see your own reflection.'},
                  {'Item' : 'Revolver', 'Type' : 'Weapon', 'Damage' : 30, 'Count' : 6, 'Description' : 'A six-round barrel revolver, capable of dealing moderate damage from a distance. Best used against a moderately powerful enemy.'},
                  {'Item' : 'Slingshot', 'Type' : 'Weapon', 'Damage' : 20, 'Count' : 10, 'Description' : 'A Y-shaped piece of wood, wrapped with a strand of rubber across the gap. Not very powerful, but it can still hurt if used correctly.'},
                  {'Item' : 'Belt', 'Type' : 'Weapon', 'Damage' : 100, 'Count' : -1, 'Description' : 'Father\'s leather belt, a sleek streamlined peice of leather with a sturdy metal buckle. Can be used to strike down foes in a single blow.'},
                  {'Item' : 'Cheese', 'Type' : 'Food', 'Health' : random.randint(0,10)*10, 'Cut' : False, 'Count' : 1, 'Description' : 'A small wedge of swiss cheese, it smells slightly of mold but otherwise looks edible.'},
                  {'Item' : 'Apple', 'Type' : 'Food', 'Health' : 30, 'Cut' : False, 'Count' : 1, 'Description' : 'A fresh granny smith apple, full of vibrant green colour and a crisp texture. If you\'re lucky you might be able to turn it into cider...'},
                  {'Item' : 'Water Bottle', 'Type' : 'Beverage', 'Health' : 10, 'Count' : 1, 'Description' : 'A piece of plastic shaped in a roughly cylindrical shape filled with clean drinking water. Enough to quench both thirst and hunger for a short while.'},
                  {'Item' : 'Ham', 'Type' : 'Food', 'Health' : 15, 'Cut' : False, 'Count' : 1, 'Description' : 'A slice of cured ham, slightly salty but otherwise edible. Could be used to make a sandwich if you had the right ingredients.'},
                  {'Item' : 'Bread', 'Type' : 'Food', 'Health' : 5, 'Cut' : False, 'Count' : 1, 'Description' : 'A slice of white bread, soft and fluffy. Could be used to make a sandwich if you had the right ingredients.'},
                  {'Item' : 'Sandwich', 'Type' : 'Food', 'Health' : 40, 'Cut' : False, 'Count' : 1, 'Description' : 'A delicious ham and cheese sandwich, stacked high with layers of ham, cheese, and bread. Perfect for a quick meal on the go, all while being plenty nutricious.'},
                  {'Item' : 'Potion', 'Type' : 'Effect', 'Effect' : random.choice(['Teleport', 'Strength']), 'Count' : 1, 'Description' : 'A small vial filled with a glowing liquid. Drinking it will grant you a random effect, but be careful... you never know what might happen...'},
                  {'Item' : 'Box', 'Type' : 'Container', 'Slots' : 3, 'Count' : -1, 'Description' : 'A small cardboard box, capable of holding a few items inside. Not very secure, but better than nothing.'},
                  {'Item' : 'Soul Orb', 'Type' : 'Spawner', 'Spawn' : 'Demon', 'Count' : 1, 'Description' : 'A dark orb pulsating with an eerie purple light. It seems to contain a malevolent presence within, capable of summoning a powerful demon when activated.'},
                  {'Item' : 'Recipe', 'Type' : 'Instructions', 'Instructions' : 'Step 1: Cut Cheese\nStep 2: Cut Ham\nStep 3: Cut Bread\nStep 4: Type "craft" in the options menu\nStep 5: Type the item you want to craft and hit ENTER', 'Count' : -1, 'Description' : 'A worn piece of parchment containing instructions on how to craft various items. It seems to be quite old, but the information is still legible.'},
                  {'Item' : 'Cannon', 'Type' : 'Weapon', 'Damage' : 70, 'Count' : 1, 'Description' : 'A small handheld cannon, capable of firing powerful blasts of energy. It looks quite dangerous, so be careful when using it.'},
                  {'Item' : 'Stick', 'Type' : 'Weapon', 'Damage' : 10, 'Count' : -1, 'Description' : 'A sturdy wooden stick, roughly the size of a baseball bat. Not very powerful, but it can still be used to strike down foes.'},
                  {'Item' : 'Slipper', 'Type' : 'Weapon', 'Damage' : 200, 'Count' : 10, 'Description' : 'The fabled slipper, the killer of all behinds. Be weary of the individual who possesses this item. Not to be taken lightly.'},
                  {'Item' : 'Apple Juice', 'Type' : 'Beverage', 'Health' : 30, 'Count' : 1, 'Description' : 'A refreshing bottle of apple cider, perfect for quenching your thirst and satisfying your hunger. Made from fresh apples and a hint of cinnamon, it\'s sure to delight your taste buds.'}]

inventory, addonLocations = {}, ['HOUSE']
room = 'OUTSIDE'
expansionLoc = 'HOUSE'

tutorialMode = True
failed = False
start = True
crashed = False
selectedLang = 'en'
