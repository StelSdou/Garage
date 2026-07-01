import os
from src.world.vehicle import StandardCar, SUV, Van
from src.world.tools import Obd2Scanner, BatteryTester, TorqueWrench
from src.world.machines import StandardLift, HeavyDutyLift
from src.world.equipment import Oils, Filters
from src.world.garage_world import GarageWorld

def load_problem_into_world(file_path: str) -> GarageWorld:
    """
    Διαβάζει το αρχείο .txt, κάνει parse τις οντότητες 
    και επιστρέφει ένα έτοιμο αντικείμενο GarageWorld.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Το αρχείο {file_path} δεν βρέθηκε!")

    world = GarageWorld()
    current_section = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line == "INIT":
                current_section = "INIT"
                continue
            elif line == "GOAL":
                current_section = "GOAL"
                # Στο Stage 2 θα χειριστούμε τους στόχους ξεχωριστά,
                # για την ώρα μας νοιάζει το INIT
                continue

            if current_section == "INIT":
                # Παράδειγμα line: "Vehicle: BMW, black, ABC123, engine light"
                parts = line.split(":")
                type_of_entity = parts[0].strip().lower()  # π.χ. "vehicle"
                details = [d.strip() for d in parts[1].split(",")] # [BMW, black, ABC123, engine light]

                # 1. PARSE VEHICLES
                if type_of_entity == "vehicle":
                    brand, color, plate, problem = details[0], details[1], details[2], details[3]
                    # Δημιουργούμε StandardCar ως default, ή SUV/Van αν το γράφει το brand
                    if "suv" in brand.lower():
                        v = SUV(problem=problem, color=color, license_plate=plate, brand=brand, owner_name="Unknown", weight=2.2, weight_tons=2.2, has_4x4=True)
                    elif "van" in brand.lower():
                        v = Van(problem=problem, color=color, license_plate=plate, brand=brand, owner_name="Unknown", weight=3.0, weight_tons=3.0, height=2.5)
                    else:
                        v = StandardCar(problem=problem, color=color, license_plate=plate, brand=brand, owner_name="Unknown", weight=1.4, num_doors=5, is_hatchback=True)
                    world.add_vehicle(v)

                # 2. PARSE TOOLS
                elif type_of_entity == "tool":
                    tool_id, tool_class = details[0], details[1].lower()
                    if "obd" in tool_class:
                        world.add_tool(Obd2Scanner(tool_id=tool_id))
                    elif "battery" in tool_class:
                        world.add_tool(BatteryTester(tool_id=tool_id))
                    elif "torque" in tool_class:
                        world.add_tool(TorqueWrench(tool_id=tool_id))

                # 3. PARSE MACHINES
                elif type_of_entity == "machine":
                    machine_id, machine_class = details[0], details[1].lower()
                    if "standard" in machine_class or "ramp" in machine_id.lower():
                        world.add_machine(StandardLift(machine_id=machine_id))
                    elif "heavy" in machine_class:
                        world.add_machine(HeavyDutyLift(machine_id=machine_id, _max_lifting_capacity=5.0))

    return world

class ParsedCommand:
    def __init__(self, raw_text: str, intent: str, target: str, detail: str = ""):
        self.raw_text = raw_text
        self.intent = intent    # π.χ. 'inspect', 'lift', 'scan', 'oil', 'wrench'
        self.target = target    # π.χ. 'black BMW', 'yellow Fiat'
        self.detail = detail    # π.χ. '2L' ή '180Nm'

class RuleBasedParser:
    def parse(self, command: str) -> ParsedCommand:
        cmd_lower = command.lower()
        
        # Καθαρισμός συχνών λέξεων για ευκολότερο extraction
        cleaned = cmd_lower.replace("the ", "").strip()
        
        if "inspect" in cleaned:
            target = cleaned.replace("inspect", "").strip()
            return ParsedCommand(command, "inspect", target)
            
        elif "scan" in cleaned:
            # π.χ. "scan silver volkswagen with obd2"
            target = cleaned.replace("scan", "").replace("with obd2", "").strip()
            return ParsedCommand(command, "scan", target, "obd2")
            
        elif "battery" in cleaned:
            target = cleaned.replace("check battery of", "").strip()
            return ParsedCommand(command, "battery", target)
            
        elif "lift" in cleaned:
            target = cleaned.replace("lift", "").strip()
            return ParsedCommand(command, "lift", target)
            
        elif "replace filter" in cleaned:
            target = cleaned.replace("replace filter on", "").strip()
            return ParsedCommand(command, "filter", target)
            
        elif "pour oil" in cleaned:
            # Απόσπαση ποσότητας αν υπάρχει (π.χ. 2l)
            target_part = cleaned.replace("pour oil into", "").strip()
            detail = "1L" # default
            if " " in target_part:
                parts = target_part.split()
                if "l" in parts[-1]:
                    detail = parts[-1].upper()
                    target_part = " ".join(parts[:-1])
            return ParsedCommand(command, "oil", target_part, detail)
            
        elif "torque wrench" in cleaned:
            # "use torque wrench on blue mercedes van at 180nm"
            target_part = cleaned.replace("use torque wrench on", "").strip()
            detail = "200Nm" # default
            if " at " in target_part:
                parts = target_part.split(" at ")
                target_part = parts[0].strip()
                detail = parts[1].strip().upper()
            return ParsedCommand(command, "wrench", target_part, detail)
            
        elif "move" in cleaned:
            # "move yellow fiat to finished"
            target_part = cleaned.replace("move", "").strip()
            target = target_part
            detail = "Garage"
            if " to " in target_part:
                parts = target_part.split(" to ")
                target = parts[0].strip()
                detail = parts[1].strip().title()
            return ParsedCommand(command, "move", target, detail)
            
        elif "repair" in cleaned:
            target = cleaned.replace("repair", "").strip()
            return ParsedCommand(command, "repair", target)
            
        elif "show state" in cleaned:
            return ParsedCommand(command, "show_state", "")
            
        return ParsedCommand(command, "unknown", cleaned)