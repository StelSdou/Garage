from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

@dataclass
class Tool(ABC):
    tool_id: str
    _condition: str = "Good"  # Good, Fair, Damaged, Requires Calibration
    _location: str = "Tool Bench"
    _is_borrowed: bool = field(default=False, init=False)

    @property
    def condition(self) -> str:
        return self._condition

    @condition.setter
    def condition(self, value: str):
        allowed_states = ["Good", "Fair", "Damaged", "Requires Calibration"]
        if value not in allowed_states:
            raise ValueError(f"Μη έγκυρη κατάσταση εργαλείου: {value}")
        self._condition = value

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, new_location: str):
        self._location = new_location

    def borrow_tool(self):
        if self._is_borrowed:
            raise RuntimeError(f"Το εργαλείο {self.tool_id} είναι ήδη σε χρήση!")
        if self.condition == "Damaged":
            raise RuntimeError(f"Αδυναμία χρήσης! Το εργαλείο {self.tool_id} είναι κατεστραμμένο.")
        self._is_borrowed = True
        print(f"Το εργαλείο {self.tool_id} δανείστηκε επιτυχώς.")

    def return_tool(self, current_location: str):
        if not self._is_borrowed:
            print(f"Το εργαλείο {self.tool_id} δεν είχε δανειστεί.")
            return
        self._is_borrowed = False
        self.location = current_location
        print(f"Το εργαλείο {self.tool_id} επιστράφηκε στη θέση {current_location}.")

    def get_details(self) -> str:
        borrowed_status = "Borrowed" if self._is_borrowed else "Available"
        return (
            f"Tool ID: {self.tool_id}, "
            f"Condition: {self.condition}, "
            f"Location: {self.location}, "
            f"Status: {borrowed_status}"
        )

    def is_usable(self) -> bool:
        return not self._is_borrowed and self.condition != "Damaged"


    def check_before_use(self) -> str:
        if self._is_borrowed:
            return f"Το εργαλείο {self.tool_id} χρησιμοποιείται ήδη."
        if self.condition == "Damaged":
            return f"Το εργαλείο {self.tool_id} είναι κατεστραμμένο."
        if self.condition == "Requires Calibration":
            return f"Το εργαλείο {self.tool_id} χρειάζεται βαθμονόμηση."
        return f"Το εργαλείο {self.tool_id} μπορεί να χρησιμοποιηθεί."

@dataclass
class ElectricalTool(Tool, ABC):
    _battery_level: int = 100  # Ποσοστό %

    @property
    def battery_level(self) -> int:
        return self._battery_level

    @battery_level.setter
    def battery_level(self, level: int):
        if not (0 <= level <= 100):
            raise ValueError("Το επίπεδο μπαταρίας πρέπει να είναι μεταξύ 0 και 100.")
        self._battery_level = level

    def charge(self):
        self.battery_level = 100
        print(f"Το εργαλείο {self.tool_id} φορτίστηκε πλήρως (100%).")

    def power_on(self) -> bool:
        if self.battery_level < 5:
            print(f"Αδυναμία ενεργοποίησης {self.tool_id}: Χαμηλή μπαταρία!")
            return False
        print(f"Το ηλεκτρικό εργαλείο {self.tool_id} τέθηκε σε λειτουργία.")
        return True

    def consume_battery(self, amount: int):
        if amount < 0:
            raise ValueError("Η κατανάλωση μπαταρίας δεν μπορεί να είναι αρνητική.")
        if self.battery_level < amount:
            raise RuntimeError(f"Το εργαλείο {self.tool_id} δεν έχει αρκετή μπαταρία.")
        self.battery_level -= amount

@dataclass
class MechanicalTool(Tool, ABC):
    material: str = "Chrome Vanadium Steel"


@dataclass
class Obd2Scanner(ElectricalTool):
    software_version: str = "v2026.1"
    supported_protocol: str = "CAN-BUS"

    def scan_error_codes(self) -> List[str]:
        if not self.power_on():
            return []
        self.consume_battery(10)
        print(f"Σάρωση μέσω πρωτοκόλλου {self.supported_protocol}...")
        return ["P0300", "P0171"]

    def clear_codes(self):
        if not self.power_on():
            return
        print("Οι κωδικοί βλαβών (DTCs) διαγράφηκαν επιτυχώς.")


@dataclass
class BatteryTester(ElectricalTool):
    max_voltage: float = 24.0

    def test_battery_health(self, vehicle_plate: str) -> str:
        if not self.power_on():
            return "Device Offline"
        self.battery_level -= 5
        print(f"Έλεγχος μπαταρίας για το όχημα {vehicle_plate}...")
        return "Υγεία Μπαταρίας: 88% (Καλή κατάσταση)"


@dataclass
class TorqueWrench(MechanicalTool):
    max_torque_nm: float = 200.0
    _current_torque_setting: float = field(default=0.0, init=False)

    def calibrate(self):
        self.condition = "Good"
        print(f"Το δυναμόκλειδο {self.tool_id} βαθμονομήθηκε επιτυχώς.")

    def set_torque(self, torque_nm: float):
        if torque_nm > self.max_torque_nm:
            raise ValueError(f"Αδυναμία ρύθμισης! Η μέγιστη ροπή είναι {self.max_torque_nm}Nm.")
        self._current_torque_setting = torque_nm
        print(f"Η ροπή ρυθμίστηκε στα {torque_nm}Nm.")


@dataclass
class OpenEndWrench(MechanicalTool):
    size_mm: int = 13

    def fasten_bolt(self):
        print(f"Σφίξιμο μπουλονιού με γερμανικό κλειδί μεγέθους {self.size_mm}mm από υλικό {self.material}.")