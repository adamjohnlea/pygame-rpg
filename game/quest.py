import json
from pathlib import Path

class Quest:
    def __init__(self, quest_data):
        self.id = quest_data['id']
        self.name = quest_data['name']
        self.description = quest_data['description']
        self.objectives = quest_data['objectives']
        self.rewards = quest_data['rewards']
        self.status = quest_data['status']  # not_started, in_progress, completed, rewarded

    def check_objective_completion(self, objective_id):
        for objective in self.objectives:
            if objective['id'] == objective_id:
                return objective['completed']
        return False

    def complete_objective(self, objective_id):
        for objective in self.objectives:
            if objective['id'] == objective_id:
                objective['completed'] = True
                break
        self._update_status()

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

class QuestManager:
    def __init__(self):
        self.quests = {}
        self.active_quests = []
        self.load_quests()

    def load_quests(self):
        quest_file = Path('data/quests.json')
        if quest_file.exists():
            with open(quest_file) as f:
                quest_data = json.load(f)
                for quest in quest_data['quests']:
                    self.quests[quest['id']] = Quest(quest)

    def start_quest(self, quest_id):
        if quest_id in self.quests and self.quests[quest_id].status == 'not_started':
            self.quests[quest_id].status = 'in_progress'
            self.active_quests.append(quest_id)
            return True
        return False

    def complete_objective(self, quest_id, objective_id):
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            quest.complete_objective(objective_id)
            return quest.is_completed()
        return False

    def get_active_quests(self):
        return [self.quests[qid] for qid in self.active_quests]

    def get_available_quests(self):
        return [quest for quest in self.quests.values() if quest.status == 'not_started']

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