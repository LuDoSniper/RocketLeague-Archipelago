"""Experimental Archipelago world. Requires a compatible Archipelago source checkout."""
from BaseClasses import Item, ItemClassification, Location, Region
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule

BASE_ID = 26061000
LOCATION_NAMES = [
    "First Goal",
    "Three Career Goals",
    "First Save",
    "Three Career Saves",
    "First Assist",
    "First Win",
    "Two Career Wins",
    "Overtime Winner",
    "2v2 Victory",
    "3v3 Victory",
    "Five Career Goals",
    "Champion",
]
ITEM_NAMES = [
    "Boost",
    "Double Jump",
    "Air Roll",
    "Champion License",
    "Training Voucher",
]
LOCATION_IDS = {name: BASE_ID + idx for idx, name in enumerate(LOCATION_NAMES)}
ITEM_IDS = {name: BASE_ID + 100 + idx for idx, name in enumerate(ITEM_NAMES)}

class RocketLeagueItem(Item):
    game = "Rocket League"

class RocketLeagueLocation(Location):
    game = "Rocket League"

class RocketLeagueWorld(World):
    game = "Rocket League"
    required_client_version = (0, 4, 0)
    item_name_to_id = ITEM_IDS
    location_name_to_id = LOCATION_IDS

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        arena = Region("Arena", self.player, self.multiworld)
        menu.connect(arena)
        self.multiworld.regions.extend([menu, arena])
        for name, location_id in LOCATION_IDS.items():
            arena.locations.append(RocketLeagueLocation(self.player, name, location_id, arena))

    def create_item(self, name):
        classification = (ItemClassification.progression if name != "Training Voucher"
                          else ItemClassification.filler)
        return RocketLeagueItem(name, classification, ITEM_IDS[name], self.player)

    def create_items(self):
        # 12 locations, one locked goal event, 11 items in the random pool.
        names = ["Boost", "Double Jump", "Air Roll", "Champion License"]
        names += ["Training Voucher"] * 7
        self.multiworld.itempool += [self.create_item(name) for name in names]

    def set_rules(self):
        player = self.player
        for name in ("Overtime Winner", "2v2 Victory", "3v3 Victory"):
            set_rule(self.multiworld.get_location(name, player),
                     lambda state: state.has("Boost", player))
        set_rule(self.multiworld.get_location("Five Career Goals", player),
                 lambda state: state.has("Double Jump", player))
        set_rule(self.multiworld.get_location("Champion", player),
                 lambda state: all(state.has(item, player) for item in
                                   ("Boost", "Double Jump", "Air Roll", "Champion License")))
        goal = RocketLeagueItem("Champion Trophy", ItemClassification.progression, None, player)
        self.multiworld.get_location("Champion", player).place_locked_item(goal)
        self.multiworld.completion_condition[player] = (
            lambda state: state.has("Champion Trophy", player)
        )

    def get_filler_item_name(self):
        return "Training Voucher"
