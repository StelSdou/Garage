from world.vehicle import StandardCar, SUV, Van
from world.tools import Obd2Scanner, BatteryTester, TorqueWrench
from world.machines import StandardLift, HeavyDutyLift
from world.equipment import Oils, Filters
from world.garage_world import GarageWorld


world = GarageWorld()

# Vehicles
world.add_vehicle(StandardCar(
    problem="engine light",
    color="black",
    license_plate="ABC123",
    brand="BMW",
    owner_name="Nikos",
    weight=1.5,
    num_doors=4,
    is_hatchback=False
))

world.add_vehicle(StandardCar(
    problem="brake noise",
    color="red",
    license_plate="AUD111",
    brand="Audi",
    owner_name="Giorgos",
    weight=1.4,
    num_doors=5,
    is_hatchback=True
))

world.add_vehicle(SUV(
    problem="suspension noise",
    color="white",
    license_plate="SUV222",
    brand="Toyota",
    owner_name="Maria",
    weight=2.1,
    weight_tons=2.1,
    has_4x4=True
))

world.add_vehicle(Van(
    problem="oil leak",
    color="blue",
    license_plate="VAN333",
    brand="Mercedes",
    owner_name="Kostas",
    weight=2.8,
    weight_tons=2.8,
    height=2.4
))

# Tools
world.add_tool(Obd2Scanner(tool_id="OBD-01"))
world.add_tool(BatteryTester(tool_id="BAT-01"))
world.add_tool(TorqueWrench(tool_id="TORQUE-01"))

# Machines
world.add_machine(StandardLift(machine_id="Ramp A"))
world.add_machine(HeavyDutyLift(machine_id="Ramp B", _max_lifting_capacity=5.0))

# Equipment
world.add_equipment(Oils(
    quality="High",
    reused=False,
    quantity=10,
    part_number="OIL-5W30",
    price=12.0,
    liters=20.0,
    viscosity="5W-30"
))

world.add_equipment(Filters(
    quality="OEM",
    reused=False,
    quantity=5,
    part_number="FILTER-AIR-01",
    price=18.0,
    compatible_brands=["BMW", "Audi"],
    filter_type="Air Filter"
))

commands = [
    "inspect the black BMW",
    "scan the black BMW with obd2",
    "check battery of the red Audi",
    "lift the white SUV",
    "replace filter on the red Audi",
    "pour oil into the black BMW",
    "move BMW to Finished",
    "repair the black BMW",
    "use torque wrench on the blue Mercedes",
    "move the blue Mercedes to Ramp B"
]

for command in commands:
    print("\n==============================")
    print("Input:", command)
    print(world.handle_command(command))