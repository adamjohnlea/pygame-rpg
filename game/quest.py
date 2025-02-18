import json
from pathlib import Path

class Quest:
    def __init__(self, quest_data):
        self.id = quest_data['id']
        self.name = quest_data['name']
        self.description = quest_data['description']
        self.objectives = quest_data['objectives']
        self.rewards = quest_data['rewards']
        self.status = 'available'  # available, accepted, completed, rewarded

    def accept(self):
        if self.status == 'available':
            self.status = 'accepted'
            return True
        return False

    def check_objective_completion(self, objective_id):
        for objective in self.objectives:
            if objective['id'] == objective_id:
                return objective['completed']
        return False

    def complete_objective(self, objective_id):
        if self.status != 'accepted':
            return False
        for objective in self.objectives:
            if objective['id'] == objective_id:
                objective['completed'] = True
                break
        self._update_status()
        return True

    def _update_status(self):
        if self.status == 'rewarded':
            return

        all_completed = all(obj['completed'] for obj in self.objectives)
        if all_completed:
            self.status = 'completed'
        elif any(obj['completed'] for obj in self.objectives):
            self.status = 'in_progress'

    def is_completed(self):
        return self.status == 'completed'

    def get_progress(self):
        completed = sum(1 for obj in self.objectives if obj['completed'])
        total = len(self.objectives)
        return completed, total

    def get_reward_description(self):
        """Returns a human-readable description of the quest rewards"""
        rewards = []
        if 'gold' in self.rewards:
            rewards.append(f"{self.rewards['gold']} gold")
        if 'items' in self.rewards:
            for item in self.rewards['items']:
                qty = item.get('quantity', 1)
                rewards.append(f"{qty}x {item['id']}")
        if 'stats' in self.rewards:
            for stat, value in self.rewards['stats'].items():
                rewards.append(f"+{value} {stat}")
        return ", ".join(rewards)

class QuestManager:
    def __init__(self):
        self.quests = {}
        self.active_quests = []
        self.available_quests = []
        self.pending_rewards = []  # List to track rewards that need to be shown
        self.load_quests()

    def load_quests(self):
        quest_file = Path('data/quests.json')
        if quest_file.exists():
            with open(quest_file) as f:
                quest_data = json.load(f)
                for quest in quest_data['quests']:
                    new_quest = Quest(quest)
                    self.quests[quest['id']] = new_quest
                    self.available_quests.append(quest['id'])

    def accept_quest(self, quest_id):
        if quest_id in self.available_quests:
            quest = self.quests[quest_id]
            if quest.accept():
                self.available_quests.remove(quest_id)
                self.active_quests.append(quest_id)
                return True
        return False

    def complete_objective(self, quest_id, objective_id):
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            return quest.complete_objective(objective_id)
        return False

    def get_active_quests(self):
        return [self.quests[qid] for qid in self.active_quests]

    def get_available_quests(self):
        return [self.quests[qid] for qid in self.available_quests]

    def get_completed_quests(self):
        return [quest for quest in self.quests.values() if quest.status == 'completed']

    def check_room_objectives(self, room_type):
        for quest_id in self.active_quests:
            quest = self.quests[quest_id]
            for objective in quest.objectives:
                if (objective['type'] == 'visit_room' and 
                    objective['target'] == room_type and 
                    not objective['completed']):
                    quest.complete_objective(objective['id'])

    def check_purchase_objectives(self, item_id):
        for quest_id in self.active_quests:
            quest = self.quests[quest_id]
            for objective in quest.objectives:
                if (objective['type'] in ['purchase', 'acquire_item'] and 
                    (objective['type'] == 'purchase' or objective.get('target') == item_id) and 
                    not objective['completed']):
                    quest.complete_objective(objective['id'])

    def apply_rewards(self, player):
        """Apply quest rewards and return a list of reward messages"""
        for quest in self.get_completed_quests():
            if quest.status == 'completed':
                # Create reward message
                reward_message = f"Quest Complete: {quest.name}\nRewards: {quest.get_reward_description()}"
                
                # Apply gold reward
                if 'gold' in quest.rewards:
                    player.stats['gold'] += quest.rewards['gold']
                    print(f"Applied gold reward: +{quest.rewards['gold']}")  # Debug print
                
                # Apply item rewards
                if 'items' in quest.rewards:
                    for item in quest.rewards['items']:
                        player.inventory.add_item(item)
                
                # Apply stat rewards
                if 'stats' in quest.rewards:
                    for stat, value in quest.rewards['stats'].items():
                        if stat in player.stats:
                            player.stats[stat] += value
                
                # Add message to pending rewards
                print(f"Adding reward message: {reward_message}")  # Debug print
                self.pending_rewards.append(reward_message)
                quest.status = 'rewarded'

    def has_pending_rewards(self):
        return len(self.pending_rewards) > 0

    def get_next_reward_message(self):
        if self.pending_rewards:
            return self.pending_rewards.pop(0)
        return None