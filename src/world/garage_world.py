from src.world.vehicle import StandardCar, SUV, Van
from src.world.tools import Obd2Scanner, BatteryTester, TorqueWrench
from src.world.machines import VehicleLift
from src.world.equipment import Oils, Filters, UniversalParts, Parts


class GarageWorld:
    def __init__(self):
        self.vehicles = []
        self.tools = []
        self.machines = []
        self.equipment = []
        self.action_log = []

    def add_vehicle(self, vehicle: StandardCar | SUV | Van):
        self.vehicles.append(vehicle)

    def add_tool(self, tool):
        self.tools.append(tool)

    def add_machine(self, machine):
        self.machines.append(machine)

    def add_equipment(self, item):
        self.equipment.append(item)

    def log_action(self, action: str):
        self.action_log.append(action)

    def find_vehicle(self, description: str) -> StandardCar | SUV | Van:
        matches = []

        for vehicle in self.vehicles:
            if vehicle.matches_description(description):
                matches.append(vehicle)

        if len(matches) == 0:
            raise RuntimeError(f"Δεν βρέθηκε όχημα που να ταιριάζει με: '{description}'")

        if len(matches) > 1:
            options = []
            for v in matches:
                options.append(f"{v.brand} {v.color} με πινακίδα {v.license_plate}")

            raise RuntimeError(
                "Ασαφής αναφορά. Βρέθηκαν περισσότερα από ένα οχήματα:\n"
                + "\n".join(options)
                + "\nΔώσε πιο συγκεκριμένη περιγραφή ή πινακίδα."
            )

        return matches[0]

    def find_tool(self, tool_type):
        for tool in self.tools:
            if isinstance(tool, tool_type):
                return tool

        raise RuntimeError(f"Δεν βρέθηκε εργαλείο τύπου {tool_type.__name__}.")

    def find_machine(self, machine_type):
        for machine in self.machines:
            if isinstance(machine, machine_type):
                return machine

        raise RuntimeError(f"Δεν βρέθηκε μηχάνημα τύπου {machine_type.__name__}.")

    def find_equipment(self, equipment_type):
        for item in self.equipment:
            if isinstance(item, equipment_type):
                return item

        raise RuntimeError(f"Δεν βρέθηκε εξοπλισμός τύπου {equipment_type.__name__}.")

    def inspect_vehicle(self, description: str) -> str:
        vehicle = self.find_vehicle(description)

        self.log_action(f"inspect({vehicle.license_plate})")

        return (
            f"Action sequence:\n"
            f"1. resolve vehicle: {vehicle.license_plate}\n"
            f"2. inspect vehicle\n\n"
            f"Result:\n"
            f"{vehicle.get_details()}\n"
            f"Faults: {vehicle.identify_faults()}"
        )

    def move_vehicle(self, description: str, new_location: str) -> str:
        vehicle = self.find_vehicle(description)

        self.log_action(f"move({vehicle.license_plate}, {new_location})")

        result = vehicle.move_to(new_location)

        return (
            f"Action sequence:\n"
            f"1. resolve vehicle: {vehicle.license_plate}\n"
            f"2. check if location exists\n"
            f"3. move vehicle\n\n"
            f"Result:\n"
            f"{result}"
        )

    def scan_vehicle_with_obd2(self, description: str) -> str:
        vehicle = self.find_vehicle(description)
        scanner = self.find_tool(Obd2Scanner)

        self.log_action(f"scan_obd2({vehicle.license_plate}, {scanner.tool_id})")

        scanner.borrow_tool()

        try:
            codes = scanner.scan_error_codes()
            faults = vehicle.identify_faults()
        finally:
            scanner.return_tool("Tool Bench")

        return (
            f"Action sequence:\n"
            f"1. resolve vehicle: {vehicle.license_plate}\n"
            f"2. borrow OBD2 scanner: {scanner.tool_id}\n"
            f"3. connect scanner to vehicle\n"
            f"4. scan error codes\n"
            f"5. return scanner\n\n"
            f"Result:\n"
            f"DTC Codes: {codes}\n"
            f"Vehicle faults: {faults}"
        )

    def test_vehicle_battery(self, description: str) -> str:
        vehicle = self.find_vehicle(description)
        tester = self.find_tool(BatteryTester)

        self.log_action(f"test_battery({vehicle.license_plate}, {tester.tool_id})")

        tester.borrow_tool()

        try:
            result = tester.test_battery_health(vehicle.license_plate)
        finally:
            tester.return_tool("Tool Bench")

        return (
            f"Action sequence:\n"
            f"1. resolve vehicle: {vehicle.license_plate}\n"
            f"2. borrow battery tester: {tester.tool_id}\n"
            f"3. test battery health\n"
            f"4. return battery tester\n\n"
            f"Result:\n"
            f"{result}"
        )

    def lift_vehicle(self, description: str) -> str:
        vehicle = self.find_vehicle(description)
        lift = self.find_machine(VehicleLift)

        vehicle_weight = getattr(vehicle, "weight_tons", vehicle.weight)

        self.log_action(f"lift({vehicle.license_plate}, {lift.machine_id})")

        lift.lift_car(vehicle.license_plate, vehicle_weight)

        try:
            vehicle.location = lift.machine_id
        except ValueError:
            pass

        return (
            f"Action sequence:\n"
            f"1. resolve vehicle: {vehicle.license_plate}\n"
            f"2. find available lift: {lift.machine_id}\n"
            f"3. check vehicle weight: {vehicle_weight}t\n"
            f"4. book lift\n"
            f"5. lift vehicle\n\n"
            f"Result:\n"
            f"Το όχημα {vehicle.license_plate} ανυψώθηκε στη ράμπα {lift.machine_id}."
        )

    def replace_filter_on_vehicle(self, description: str) -> str:
        vehicle = self.find_vehicle(description)
        filter_item = self.find_equipment(Filters)

        if filter_item.compatible_brands and vehicle.brand not in filter_item.compatible_brands:
            raise RuntimeError(
                f"Το φίλτρο {filter_item.part_number} δεν είναι συμβατό με {vehicle.brand}."
            )

        filter_item.use_one()
        filter_item.replace_filter()

        self.log_action(f"replace_filter({vehicle.license_plate}, {filter_item.part_number})")

        return (
            f"Action sequence:\n"
            f"1. resolve vehicle: {vehicle.license_plate}\n"
            f"2. find compatible filter: {filter_item.part_number}\n"
            f"3. check stock\n"
            f"4. replace filter\n\n"
            f"Result:\n"
            f"Το φίλτρο αντικαταστάθηκε στο όχημα {vehicle.license_plate}."
        )

    def pour_oil_to_vehicle(self, description: str, amount: float = 1.0) -> str:
        vehicle = self.find_vehicle(description)
        oil = self.find_equipment(Oils)

        oil.pour_fluid(amount)

        self.log_action(f"pour_oil({vehicle.license_plate}, {amount}L)")

        return (
            f"Action sequence:\n"
            f"1. resolve vehicle: {vehicle.license_plate}\n"
            f"2. find oil: {oil.part_number}\n"
            f"3. check available liters\n"
            f"4. pour oil\n\n"
            f"Result:\n"
            f"Προστέθηκαν {amount}L λαδιού στο όχημα {vehicle.license_plate}."
        )

    def show_world_state(self) -> str:
        lines = ["Current Garage World State:\n"]

        lines.append("Vehicles:")
        for v in self.vehicles:
            lines.append(f"- {v.brand} {v.color}, Plate: {v.license_plate}, Location: {v.location}, Problem: {v.problem}")

        lines.append("\nTools:")
        for t in self.tools:
            lines.append(f"- {t.get_details()}")

        lines.append("\nMachines:")
        for m in self.machines:
            status = "Available" if m.is_available else "Occupied"
            lines.append(f"- {m.machine_id}, Status: {status}")

        lines.append("\nEquipment:")
        for e in self.equipment:
            lines.append(f"- {e.part_number}, Quantity: {e.quantity}, Price: {e.price}")

        return "\n".join(lines)

    def handle_command(self, command: str) -> str:
        command_lower = command.lower()

        if "inspect" in command_lower:
            return self.inspect_vehicle(command)

        if "scan" in command_lower or "obd2" in command_lower:
            return self.scan_vehicle_with_obd2(command)

        if "battery" in command_lower:
            return self.test_vehicle_battery(command)

        if "lift" in command_lower or "raise" in command_lower:
            return self.lift_vehicle(command)

        if "replace filter" in command_lower or "change filter" in command_lower:
            return self.replace_filter_on_vehicle(command)

        if "oil" in command_lower:
            return self.pour_oil_to_vehicle(command)

        if "move" in command_lower and "to" in command_lower:
            parts = command_lower.split("to")
            vehicle_description = parts[0].replace("move", "").strip()
            location = parts[1].strip().title()

            location_map = {
                "Garage Entrance": "Garage Entrance",
                "Ramp A": "Ramp A",
                "Ramp B": "Ramp B",
                "Tool Bench": "Tool Bench",
                "Finished": "Finished"
            }

            if location not in location_map:
                raise RuntimeError(f"Άγνωστη τοποθεσία: {location}")

            return self.move_vehicle(vehicle_description, location_map[location])

        return "Δεν κατάλαβα την εντολή."