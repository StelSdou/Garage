from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

@dataclass
class Vehicle(ABC):
    problem: str
    color: str
    license_plate: str
    brand: str
    owner_name: str
    weight: float
    
    _location: str = field(default="lobby", init=False)

    def __post_init__(self):
        if self.weight <= 0:
            raise ValueError("Το βάρος του οχήματος πρέπει να είναι θετικός αριθμός!")

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, new_location: str):
        """Αλλάζει την τοποθεσία, αφού πρώτα ελέγξει αν είναι έγκυρη (Setter)."""
        allowed_zones = ["Garage Entrance", "Ramp A", "Ramp B", "Tool Bench", "Finished"]
        if new_location not in allowed_zones:
            raise ValueError(f"Σφάλμα: Η ζώνη '{new_location}' δεν υπάρχει στο συνεργείο!")
        self._location = new_location

    @abstractmethod
    def get_details(self) -> str:
        return f"Brand: {self.brand}, Color: {self.color}, Plate: {self.license_plate}"

    def identify_faults(self) -> List[str]:
        return [self.problem] if self.problem else ["No faults identified"]

    def move_to(self, new_location: str) -> str:
        old_location = self.location
        self.location = new_location
        return f"Το όχημα {self.license_plate} μετακινήθηκε από {old_location} σε {new_location}."


    def add_fault(self, fault: str) -> str:
        if not fault:
            return "Δεν δόθηκε βλάβη."
        if self.problem:
            self.problem += f", {fault}"
        else:
            self.problem = fault
        return f"Προστέθηκε βλάβη στο όχημα {self.license_plate}: {fault}"


    def repair_faults(self) -> str:
        if not self.problem:
            return f"Το όχημα {self.license_plate} δεν έχει καταγεγραμμένες βλάβες."
        old_problem = self.problem
        self.problem = ""
        return f"Οι βλάβες του οχήματος {self.license_plate} επισκευάστηκαν. Προηγούμενη βλάβη: {old_problem}"


    def matches_description(self, description: str) -> bool:
        description = description.lower()

        keywords = [
            self.license_plate.lower(),
            self.brand.lower(),
            self.color.lower(),
            self.__class__.__name__.lower()
        ]

        return any(keyword in description for keyword in keywords)


    def is_ready_for_service(self) -> bool:
        return self.location in ["Garage Entrance", "Ramp A", "Ramp B"]

@dataclass
class StandardCar(Vehicle):
    num_doors: int = 4
    is_hatchback: bool = False

    def get_details(self) -> str:
        base_details = super().get_details()
        return f"[Standard Car] {base_details}, Doors: {self.num_doors}"

    def calculate_standard_service_cost(self) -> float:
        base_cost = 100.0
        if self.is_hatchback:
            base_cost += 20.0
        return base_cost


@dataclass
class HeavyVehicle(Vehicle, ABC):
    weight_tons: float = 2.5

    @abstractmethod
    def check_lift_compatibility(self, max_lift_capacity: float = 3.5) -> bool:
        pass


@dataclass
class SUV(HeavyVehicle):
    has_4x4: bool = True
    ground_clearance: int = 200

    def get_details(self) -> str:
        base_details = super().get_details()
        return f"[SUV] {base_details}, 4x4: {self.has_4x4}"

    def check_lift_compatibility(self, max_lift_capacity: float = 3.5) -> bool:
        return self.weight_tons <= max_lift_capacity

    def inspect_drive_train(self) -> str:
        if self.has_4x4:
            return f"All-Wheel Drive (4x4) system inspected. Ground clearance is {self.ground_clearance}mm."
        return "Standard Two-Wheel Drive system inspected."


@dataclass
class Van(HeavyVehicle):
    height: float = 2.2

    def get_details(self) -> str:
        base_details = super().get_details()
        return f"[Van] {base_details}, Height: {self.height}m"

    def check_lift_compatibility(self, max_lift_capacity: float = 3.5) -> bool:
        max_height_allowed = 3.0
        return self.weight_tons <= max_lift_capacity and self.height <= max_height_allowed