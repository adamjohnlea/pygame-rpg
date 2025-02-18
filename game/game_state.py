class GameState:
    def __init__(self):
        self.menu_active = False
        self.inventory_active = False
        self.shop_active = False
        self.combat_active = False
        self.current_state = "game"
        self.quest_log_active = False

    def toggle_menu(self):
        self.menu_active = not self.menu_active
        if self.menu_active:
            self.current_state = "menu"
        else:
            self.current_state = "game"

    def toggle_inventory(self):
        self.inventory_active = not self.inventory_active
        if self.inventory_active:
            self.current_state = "inventory"
        else:
            self.current_state = "game"

    def toggle_shop(self):
        self.shop_active = not self.shop_active
        if self.shop_active:
            self.current_state = "shop"
        else:
            self.current_state = "game"

    def toggle_combat(self):
        self.combat_active = not self.combat_active
        if self.combat_active:
            self.current_state = "combat"
        else:
            self.current_state = "game"

    def toggle_quest_log(self):
        self.quest_log_active = not self.quest_log_active
        if self.quest_log_active:
            self.current_state = "quest_log"
        else:
            self.current_state = "game"

    def is_menu_active(self):
        return self.menu_active

    def is_inventory_active(self):
        return self.inventory_active

    def is_shop_active(self):
        return self.shop_active

    def is_combat_active(self):
        return self.combat_active

    def is_quest_log_active(self):
        return self.quest_log_active