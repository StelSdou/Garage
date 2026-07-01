from src.parser import RuleBasedParser
from src.planner import ActionPlanner

from src.world.garage_world import GarageWorld
from src.world.vehicle import StandardCar, SUV, Van
from src.world.tools import Obd2Scanner, BatteryTester, TorqueWrench, OpenEndWrench
from src.world.machines import StandardLift, HeavyDutyLift
from src.world.equipment import Oils, Filters, BrakeParts


world = GarageWorld()

# -------------------------
# Vehicles
# -------------------------

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

world.add_vehicle(StandardCar(
    problem="no problem",
    color="silver",
    license_plate="VW222",
    brand="Volkswagen",
    owner_name="Petros",
    weight=1.3,
    num_doors=5,
    is_hatchback=True
))

world.add_vehicle(StandardCar(
    problem="weak battery",
    color="yellow",
    license_plate="FIA333",
    brand="Fiat",
    owner_name="Eleni",
    weight=1.1,
    num_doors=3,
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
    has_4x4=True,
    ground_clearance=220
))

world.add_vehicle(SUV(
    problem="transfer case warning",
    color="gray",
    license_plate="BMW444",
    brand="BMW",
    owner_name="Antonis",
    weight=2.3,
    weight_tons=2.3,
    has_4x4=True,
    ground_clearance=210
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

world.add_vehicle(Van(
    problem="transmission noise",
    color="white",
    license_plate="VAN555",
    brand="Ford",
    owner_name="Dimitris",
    weight=3.4,
    weight_tons=3.4,
    height=2.7
))


# -------------------------
# Tools
# -------------------------

world.add_tool(Obd2Scanner(
    tool_id="OBD-01",
    software_version="v2026.1",
    supported_protocol="CAN-BUS"
))

world.add_tool(Obd2Scanner(
    tool_id="OBD-02",
    _condition="Fair",
    software_version="v2025.4",
    supported_protocol="K-LINE"
))

world.add_tool(BatteryTester(
    tool_id="BAT-01",
    max_voltage=24.0
))

world.add_tool(BatteryTester(
    tool_id="BAT-02",
    _condition="Good",
    max_voltage=12.0
))

world.add_tool(TorqueWrench(
    tool_id="TORQUE-01",
    max_torque_nm=200.0
))

world.add_tool(TorqueWrench(
    tool_id="TORQUE-02",
    max_torque_nm=350.0
))

world.add_tool(OpenEndWrench(
    tool_id="WRENCH-13",
    size_mm=13
))

world.add_tool(OpenEndWrench(
    tool_id="WRENCH-17",
    size_mm=17
))


# -------------------------
# Garage machines / 4 lifts
# -------------------------

# 2 normal ramps
world.add_machine(StandardLift(
    machine_id="Ramp A",
    _max_lifting_capacity=2.2,
    suitable_for_low_cars=True
))

world.add_machine(StandardLift(
    machine_id="Ramp B",
    _max_lifting_capacity=2.2,
    suitable_for_low_cars=True
))

# 2 heavy ramps
world.add_machine(HeavyDutyLift(
    machine_id="Ramp C",
    _max_lifting_capacity=5.0,
    supports_dual_axle=True
))

world.add_machine(HeavyDutyLift(
    machine_id="Ramp D",
    _max_lifting_capacity=4.5,
    supports_dual_axle=True
))


# -------------------------
# Equipment
# -------------------------

world.add_equipment(Oils(
    quality="High",
    reused=False,
    quantity=10,
    part_number="OIL-5W30",
    price=12.0,
    liters=25.0,
    viscosity="5W-30"
))

world.add_equipment(Filters(
    quality="OEM",
    reused=False,
    quantity=8,
    part_number="FILTER-AIR-01",
    price=18.0,
    compatible_brands=["BMW", "Audi", "Volkswagen", "Fiat", "Toyota", "Mercedes", "Ford"],
    filter_type="Air Filter"
))

world.add_equipment(BrakeParts(
    quality="Premium",
    reused=False,
    quantity=6,
    part_number="BRAKE-PADS-01",
    price=45.0,
    compatible_brands=["BMW", "Audi", "Volkswagen", "Toyota"],
    pad_thickness_mm=10.0,
    material="Ceramic"
))


parser = RuleBasedParser()
planner = ActionPlanner()


commands = [
    "inspect the black BMW",
    "inspect the gray BMW SUV",
    "scan the silver Volkswagen with obd2",
    "check battery of the yellow Fiat",

    # 2 normal cars στις 2 κανονικές ράμπες
    "lift the black BMW",
    "lift the red Audi",

    # 2 βαριά οχήματα στις 2 heavy-duty ράμπες
    "lift the white Toyota SUV",
    "lift the blue Mercedes van",

    "replace filter on the silver Volkswagen",
    "pour oil into the gray BMW SUV 2L",
    "use torque wrench on the blue Mercedes van at 180Nm",
    "move the yellow Fiat to Finished",
    "repair the black BMW",
    "show state"
]


for command in commands:
    print("\n" + "=" * 70)

    parsed_command = parser.parse(command)
    action_sequence = planner.create_plan(parsed_command.intent)
    output = world.execute_command(parsed_command, action_sequence)

    print(output)