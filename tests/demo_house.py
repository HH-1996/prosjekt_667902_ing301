from smarthouse.domain import SmartHouse

DEMO_HOUSE = SmartHouse()
from smarthouse.domain import (
    SmartHouse,
    TemperatureSensor,
    MotionSensor,
    SmokeDetector,
    WaterLeakSensor,
    LightBulp,
    SmartLock,
    HeatPump,
    SmartCurtains,
)

# Husets struktur
# 1 etasje
ground_floor = DEMO_HOUSE.register_floor(1)
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
living_room = DEMO_HOUSE.register_room(ground_floor, 25.0, "Living Room")
kitchen = DEMO_HOUSE.register_room(ground_floor, 14.2, "Kitchen")
bathroom_1 = DEMO_HOUSE.register_room(ground_floor, 8.1, "Bathroom 1")
laundry = DEMO_HOUSE.register_room(ground_floor, 7.75, "Laundry")
office = DEMO_HOUSE.register_room(ground_floor, 11.0, "Office")

# 2 etasje
second_floor = DEMO_HOUSE.register_floor(2)
master_bedroom = DEMO_HOUSE.register_room(second_floor, 18.0, "Master Bedroom")
dressing_room = DEMO_HOUSE.register_room(second_floor, 6.0, "Dressing Room")
bedroom_2 = DEMO_HOUSE.register_room(second_floor, 12.0, "Bedroom 2")
bedroom_3 = DEMO_HOUSE  .register_room(second_floor, 11.0, "Bedroom 3")
bathroom_2 = DEMO_HOUSE.register_room(second_floor, 9.0, "Bathroom 2")
hallway = DEMO_HOUSE.register_room(second_floor, 21.0, "Hallway")

# Total størrelse = 156.55

# Dingser
# IDer som er brukt i testene må være registrert her, og de må ha de riktige attributtene (type, supplier, model_name) for at testene skal passere

temp_sensor = TemperatureSensor(
    "4d8b1d62-7921-4917-9b70-bbd31f6e2e8e",
    "ClimaCore",
    "Thermo Sense X",
)

motion_sensor = MotionSensor(
    "cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5",
    "NebulaGuard Innovations",
    "MoveZ Detect 69",
)

light_bulp = LightBulp(
    "6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28",
    "Elysian Tech",
    "Lumina Glow 4000",
)

heat_pump = HeatPump(
    "5e13cabc-5c58-4bb3-82a2-3039e4480a6d",
    "NordTherm",
    "EcoHeat Pro",
)

living_smoke_detector = SmokeDetector(
    "11111111-1111-1111-1111-111111111111",
    "SafeNest",
    "SmokeSecure A1",
)

front_door_lock = SmartLock(
    "22222222-2222-2222-2222-222222222222",
    "SecureHome",
    "LockGuard 300",
)

kitchen_temp_sensor = TemperatureSensor(
    "33333333-3333-3333-3333-333333333333",
    "ClimaCore",
    "KitchenTemp Mini",
)

kitchen_leak_sensor = WaterLeakSensor(
    "44444444-4444-4444-4444-444444444444",
    "AquaSense",
    "LeakFinder Plus",
)

kitchen_curtains = SmartCurtains(
    "55555555-5555-5555-5555-555555555555",
    "ShadeLogic",
    "CurtainFlow",
)

bathroom_leak_sensor = WaterLeakSensor(
    "66666666-6666-6666-6666-666666666666",
    "AquaSense",
    "BathLeak Alert",
)

office_temp_sensor = TemperatureSensor(
    "77777777-7777-7777-7777-777777777777",
    "ClimaCore",
    "OfficeTemp One",
)

master_smoke_detector = SmokeDetector(
    "88888888-8888-8888-8888-888888888888",
    "SafeNest",
    "SmokeSecure B2",
)

bedroom_lock = SmartLock(
    "99999999-9999-9999-9999-999999999999",
    "SecureHome",
    "PrivacyLock",
)

hall_motion_sensor = MotionSensor(
    "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "NebulaGuard Innovations",
    "HallEye Motion",
)

# Registrer dingser i rom

# Stue må ha nøyaktig 3 dingser
DEMO_HOUSE.register_device(living_room, motion_sensor)
DEMO_HOUSE.register_device(living_room, temp_sensor)
DEMO_HOUSE.register_device(living_room, living_smoke_detector)

# Lyspæren må skrus på i ett rom med nøyaktig 1 dings
DEMO_HOUSE.register_device(entrance, light_bulp)

DEMO_HOUSE.register_device(office, front_door_lock)

DEMO_HOUSE.register_device(kitchen, kitchen_temp_sensor)
DEMO_HOUSE.register_device(kitchen, kitchen_leak_sensor)
DEMO_HOUSE.register_device(kitchen, kitchen_curtains)

DEMO_HOUSE.register_device(laundry, bathroom_leak_sensor)

DEMO_HOUSE.register_device(office, office_temp_sensor)

DEMO_HOUSE.register_device(master_bedroom, heat_pump)
DEMO_HOUSE.register_device(master_bedroom, master_smoke_detector)

DEMO_HOUSE.register_device(bedroom_2, bedroom_lock)

DEMO_HOUSE.register_device(hallway, hall_motion_sensor)

