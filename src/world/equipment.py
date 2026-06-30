from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

class IBillable(ABC):
    @abstractmethod
    def calculate_total_cost(self) -> float:
        pass

    @abstractmethod
    def apply_discount(self, percentage: float) -> float:
        pass


@dataclass
class Equipment(IBillable, ABC):
    quality: str
    reused: bool
    quantity: int
    part_number: str
    price: float

    def check_stock(self) -> int:
        return self.quantity

    def order_more(self, amount: int):
        if amount <= 0:
            raise ValueError("Η ποσότητα παραγγελίας πρέπει να είναι θετική!")
        self.quantity += amount
        print(f"Παραγγέλθηκαν {amount} τεμάχια για το κωδικό {self.part_number}. Νέο απόθεμα: {self.quantity}")

    def calculate_total_cost(self) -> float:
        return self.price * self.quantity

    def apply_discount(self, percentage: float) -> float:
        if not (0 <= percentage <= 100):
            raise ValueError("Η έκπτωση πρέπει να είναι μεταξύ 0% και 100%.")
        self.price -= self.price * (percentage / 100)
        return self.price
    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Η ποσότητα δεν μπορεί να είναι αρνητική.")
        if self.price < 0:
            raise ValueError("Η τιμή δεν μπορεί να είναι αρνητική.")
        if not self.part_number:
            raise ValueError("Το part number δεν μπορεί να είναι κενό.")
    
    def use_one(self):
        if self.quantity < 1:
            raise RuntimeError(f"Δεν υπάρχει διαθέσιμο απόθεμα για {self.part_number}.")
        self.quantity -= 1
        return f"Χρησιμοποιήθηκε 1 τεμάχιο από {self.part_number}. Υπόλοιπο: {self.quantity}"


# ΥΓΡΑ (FLUIDS)

@dataclass
class Fluids(Equipment, ABC):
    liters: float

    def pour_fluid(self, amount: float):
        if amount > self.liters:
            raise ValueError(f"Δεν υπάρχει αρκετό υγρό! Διαθέσιμα: {self.liters}L, Ζητήθηκαν: {amount}L.")
        self.liters -= amount
        print(f"Χρησιμοποιήθηκαν {amount}L. Απομένουν: {self.liters}L.")

    def check_expiry_date(self) -> str:
        return "Το υγρό είναι εντός ημερομηνίας λήξης."
    
    def refill(self, amount: float):
        if amount <= 0:
            raise ValueError("Η ποσότητα αναπλήρωσης πρέπει να είναι θετική.")
        self.liters += amount
        print(f"Προστέθηκαν {amount}L. Νέα ποσότητα: {self.liters}L.")


@dataclass
class Oils(Fluids):
    viscosity: str = "5W-30"


@dataclass
class BrakeFluid(Fluids):
    dot_rating: str = "DOT 4"


@dataclass
class AntifreezeFluid(Fluids):
    color_type: str = "Red (G12)"


@dataclass
class WasherFluid(Fluids):
    is_winter_mix: bool = True



# ΓΕΝΙΚΑ ΑΝΤΑΛΛΑΚΤΙΚΑ (UNIVERSAL PARTS)

@dataclass
class UniversalParts(Equipment, ABC):
    compatible_brands: List[str] = field(default_factory=list)

    def check_compatibility(self, brand: str) -> bool:
        return brand in self.compatible_brands
    
    def use_on_vehicle(self, vehicle_brand: str, vehicle_plate: str) -> str:
        if self.compatible_brands and not self.check_compatibility(vehicle_brand):
            raise RuntimeError(
                f"Το ανταλλακτικό {self.part_number} δεν είναι συμβατό με {vehicle_brand}."
            )

        self.use_one()
        return f"Το ανταλλακτικό {self.part_number} χρησιμοποιήθηκε στο όχημα {vehicle_plate}."


@dataclass
class BrakeParts(UniversalParts):
    pad_thickness_mm: float = 12.0
    material: str = "Ceramic"

    def measure_wear(self) -> str:
        if self.pad_thickness_mm < 4.0:
            return "Χρειάζεται άμεση αντικατάσταση!"
        return f"Καλή κατάσταση. Πάχος: {self.pad_thickness_mm}mm"


@dataclass
class Bearing(UniversalParts):
    pass


@dataclass
class Injectors(UniversalParts):
    pass


@dataclass
class Filters(UniversalParts):
    filter_type: str = "Air Filter"

    def replace_filter(self):
        print(f"Το φίλτρο τύπου '{self.filter_type}' αντικαταστάθηκε.")


# ΕΙΔΙΚΑ ΑΝΤΑΛΛΑΚΤΙΚΑ (PARTS)

@dataclass
class Parts(Equipment, ABC):
    oem_number: str
    is_genuine: bool = True

    def install_part(self, vehicle_plate: str):
        if self.quantity < 1:
            raise RuntimeError(f"Δεν υπάρχει απόθεμα για το ανταλλακτικό {self.part_number}!")
        self.quantity -= 1
        print(f"Το ανταλλακτικό OEM {self.oem_number} εγκαταστάθηκε στο όχημα {vehicle_plate}.")


@dataclass
class Refrigerator(Parts):
    volume_liters: int = 300


@dataclass
class FuelPump(Parts):
    pressure_bar: float = 3.5


@dataclass
class Transmission(Parts):
    gear_count: int = 6