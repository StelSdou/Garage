import copy
from collections import deque
from src.world.garage_world import GarageWorld

class Planner:
    def __init__(self, initial_world: GarageWorld, goals: dict):
        self.initial_world = initial_world
        self.goals = goals

    def is_goal_achieved(self, world: GarageWorld) -> bool:
        for vehicle in world.vehicles:
            if vehicle.license_plate in self.goals:
                target_location = self.goals[vehicle.license_plate]
                if vehicle.location != target_location:
                    return False
        return True

    def get_possible_actions(self, world: GarageWorld):
        valid_actions = []
        
        for vehicle in world.vehicles:
            if vehicle.location != "Finished":
                valid_actions.append(f"move {vehicle.brand} to Finished")
            
            if "filter" in vehicle.problem.lower():
                valid_actions.append(f"replace filter on the {vehicle.brand}")
                
            if "oil" in vehicle.problem.lower():
                valid_actions.append(f"pour oil into the {vehicle.brand}")

        return valid_actions

    def solve(self):
        print("[+] Εκκίνηση Planner (BFS Search)...")
        
        queue = deque([(self.initial_world, [])])
        visited_states = set()

        while queue:
            current_world, path = queue.popleft()

            if self.is_goal_achieved(current_world):
                return path

            possible_actions = self.get_possible_actions(current_world)

            for action in possible_actions:
                world_copy = copy.deepcopy(current_world)
                
                try:
                    world_copy.handle_command(action)
                    
                    state_snapshot = world_copy.show_world_state()
                    
                    if state_snapshot not in visited_states:
                        visited_states.add(state_snapshot)
                        queue.append((world_copy, path + [action]))
                        
                except Exception:
                    continue

        return None

class ActionPlanner:
    def create_plan(self, intent: str) -> list:
        """
        Μετατρέπει ένα υψηλού επιπέδου intent σε μια 
        ακολουθία βημάτων (action sequence).
        """
        if intent == "inspect":
            return ["resolve_vehicle", "inspect_visual"]
            
        elif intent == "scan":
            return ["resolve_vehicle", "borrow_obd", "connect_and_scan", "return_obd"]
            
        elif intent == "battery":
            return ["resolve_vehicle", "borrow_tester", "test_voltage", "return_tester"]
            
        elif intent == "lift":
            return ["resolve_vehicle", "find_suitable_lift", "check_weight_precondition", "execute_lift"]
            
        elif intent == "filter":
            return ["resolve_vehicle", "check_filter_stock", "verify_compatibility", "install_filter"]
            
        elif intent == "oil":
            return ["resolve_vehicle", "check_oil_stock", "pour_fluid_amount"]
            
        elif intent == "wrench":
            return ["resolve_vehicle", "borrow_torque_wrench", "verify_torque_limit", "tighten_bolts", "return_wrench"]
            
        elif intent == "move":
            return ["resolve_vehicle", "verify_destination", "update_location"]
            
        elif intent == "show_state":
            return ["print_full_state"]
            
        return ["unknown_action"]