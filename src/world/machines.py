from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class GarageMachine(ABC):
    machine_id: str
    
    _is_available: bool = field(default=True, init=False)
    

    @property
    def is_available(self) -> bool:
        return self._is_available

    @is_available.setter
    def is_available(self, status: bool):
        if not isinstance(status, bool):
            raise TypeError("Η κατάσταση διαθεσιμότητας πρέπει να είναι True ή False!")
        self._is_available = status

    def book_machine(self):
        if not self.is_available:
            raise RuntimeError(f"Το μηχάνημα {self.machine_id} χρησιμοποιείται ήδη!")
        self.is_available = False
        print(f"Το μηχάνημα {self.machine_id} δεσμεύτηκε με επιτυχία.")

    def release_machine(self):
        self.is_available = True
        print(f"Το μηχάνημα {self.machine_id} είναι πλέον διαθέσιμο.")


@dataclass
class VehicleLift(GarageMachine, ABC):
    _max_lifting_capacity: float = 3.5
    last_inspection_date: str = "2026-01-01"
    _current_vehicle_plate: str | None = field(default=None, init=False)

    def __post_init__(self):
        if self._max_lifting_capacity <= 0:
            raise ValueError("Η ικανότητα ανύψωσης πρέπει να είναι θετικός αριθμός τόνων!")

    @property
    def max_lifting_capacity(self) -> float:
        return self._max_lifting_capacity

    @max_lifting_capacity.setter
    def max_lifting_capacity(self, capacity: float):
        if capacity <= 0:
            raise ValueError("Η ικανότητα ανύψωσης πρέπει να είναι θετικός αριθμός!")
        self._max_lifting_capacity = capacity

    def lift_car(self, vehicle_plate: str, vehicle_weight_tons: float):
        can_lift, message = self.can_lift_vehicle(vehicle_plate, vehicle_weight_tons)

        if not can_lift:
            raise RuntimeError(message)

        self.book_machine()
        self._current_vehicle_plate = vehicle_plate
        print(f"Το όχημα {vehicle_plate} ανυψώθηκε επιτυχώς στη ράμπα {self.machine_id}.")

    def lower_car(self, vehicle_plate: str):
        if self._current_vehicle_plate != vehicle_plate:
            raise RuntimeError(
                f"Το όχημα {vehicle_plate} δεν βρίσκεται στη ράμπα {self.machine_id}."
            )

        print(f"Το όχημα {vehicle_plate} κατέβηκε από τη ράμπα {self.machine_id}.")
        self._current_vehicle_plate = None
        self.release_machine()
    
    def can_lift_vehicle(self, vehicle_plate: str, vehicle_weight_tons: float) -> tuple[bool, str]:
        if not self.is_available:
            return False, f"Η ράμπα {self.machine_id} είναι ήδη κατειλημμένη."

        if vehicle_weight_tons > self.max_lifting_capacity:
            return False, (
                f"Το όχημα {vehicle_plate} είναι πολύ βαρύ "
                f"({vehicle_weight_tons}t > {self.max_lifting_capacity}t)."
            )

        return True, "Το όχημα μπορεί να ανυψωθεί."


def get_current_vehicle(self) -> str:
    if self._current_vehicle_plate is None:
        return f"Η ράμπα {self.machine_id} είναι άδεια."
    return f"Στη ράμπα {self.machine_id} βρίσκεται το όχημα {self._current_vehicle_plate}."


@dataclass
class StandardLift(VehicleLift):
    suitable_for_low_cars: bool = True

    def adjust_lift_pads(self):
        if self.suitable_for_low_cars:
            print(f"Τα μαξιλαράκια ανύψωσης ρυθμίστηκαν για χαμηλό προφίλ στη ράμπα {self.machine_id}.")
        else:
            print(f"Χρήση τυπικών μαξιλαριών στη ράμπα {self.machine_id}.")


@dataclass
class HeavyDutyLift(VehicleLift):
    supports_dual_axle: bool = True

    def lock_heavy_duty_safeties(self):
        if self.supports_dual_axle:
            print(f"Οι μηχανικές ασφάλειες βαρέως τύπου και διπλού άξονα ΚΛΕΙΔΩΣΑΝ στη ράμπα {self.machine_id}.")
        else:
            print(f"Οι βασικές ασφάλειες βαρέως τύπου κλείδωσαν στη ράμπα {self.machine_id}.")