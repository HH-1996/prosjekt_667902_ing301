from datetime import datetime
import random


class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit


class Floor:
    def __init__(self, level):
        self.level = level
        self.rooms = []

    def add_room(self, room):
        if room not in self.rooms:
            self.rooms.append(room)


class Room:
    def __init__(self, floor, room_size, room_name=None):
        self.floor = floor
        self.room_size = room_size
        self.room_name = room_name
        self.devices = []

    def add_device(self, device):
        if device not in self.devices:
            self.devices.append(device)
            device.room = self

    def remove_device(self, device):
        if device in self.devices:
            self.devices.remove(device)


class Device:
    def __init__(self, device_id, supplier, model_name, device_type):
        self.id = device_id
        self.supplier = supplier
        self.model_name = model_name
        self.device_type = device_type
        self.room = None

    def is_sensor(self):
        return False

    def is_actuator(self):
        return False

    def get_device_type(self):
        return self.device_type


class Sensor(Device):
    def __init__(self, device_id, supplier, model_name, device_type, unit):
        super().__init__(device_id, supplier, model_name, device_type)
        self.unit = unit

    def is_sensor(self): # type: ignore
        return True

    def last_measurement(self):
        timestamp = datetime.now().isoformat()
        value = float(round(random.uniform(10.0, 30.0), 1))
        return Measurement(timestamp, value, self.unit)


class Actuator(Device):
    def __init__(self, device_id, supplier, model_name, device_type):
        super().__init__(device_id, supplier, model_name, device_type)
        self._active = False
        self.target_value = None

    def is_actuator(self): # type: ignore
        return True

    def turn_on(self, target_value=None):
        self._active = True
        self.target_value = target_value

    def turn_off(self):
        self._active = False
        self.target_value = None

    def is_active(self):
        return self._active


class TemperatureSensor(Sensor):
    def __init__(self, device_id, supplier, model_name):
        super().__init__(device_id, supplier, model_name, "Temperature Sensor", "°C")


class MotionSensor(Sensor):
    def __init__(self, device_id, supplier, model_name):
        super().__init__(device_id, supplier, model_name, "Motion Sensor", "motion")


class SmokeDetector(Sensor):
    def __init__(self, device_id, supplier, model_name):
        super().__init__(device_id, supplier, model_name, "Smoke Detector", "smoke")


class WaterLeakSensor(Sensor):
    def __init__(self, device_id, supplier, model_name):
        super().__init__(device_id, supplier, model_name, "Water Leak Sensor", "leak")


class LightBulp(Actuator):
    def __init__(self, device_id, supplier, model_name):
        super().__init__(device_id, supplier, model_name, "Light Bulp")


class SmartLock(Actuator):
    def __init__(self, device_id, supplier, model_name):
        super().__init__(device_id, supplier, model_name, "Smart Lock")


class HeatPump(Actuator):
    def __init__(self, device_id, supplier, model_name):
        super().__init__(device_id, supplier, model_name, "Heat Pump")


class SmartCurtains(Actuator):
    def __init__(self, device_id, supplier, model_name):
        super().__init__(device_id, supplier, model_name, "Smart Curtains")


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """
    def __init__(self):
        self._floors = []
        self._devices = []


    def register_floor(self, level):
        # This method registers a new floor at the given level in the house
        # and returns the respective floor object.
        existing_floor = self._find_floor(level)
        if existing_floor is not None:
            return existing_floor
        
        floor = Floor(level)
        self._floors.append(floor)
        self._floors.sort(key=lambda f: f.level)
        return floor

    def register_room(self, floor, room_size, room_name = None):
        # This methods registers a new room with the given room areal size 
        # at the given floor. Optionally the room may be assigned a mnemonic name.
        room = Room(floor, room_size, room_name)
        floor.add_room(room)
        return room

    def get_floors(self):
        # This method returns the list of registered floors in the house.
        # The list is ordered by the floor levels, e.g. if the house has 
        # registered a basement (level=0), a ground floor (level=1) and a first floor 
        # (leve=1), then the resulting list contains these three flors in the above order.
        return self._floors

    def get_rooms(self):
        # This methods returns the list of all registered rooms in the house.
        # The resulting list has no particular order.
        rooms = []
        for floor in self._floors:
            rooms.extend(floor.rooms)
        return rooms

    def get_area(self):
        # This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        return round(sum(room.room_size for room in self.get_rooms()), 2)

    def register_device(self, room, device):
        # This methods registers a given device in a given room.

        if device.room is not None and device.room is not room:
            device.room.remove_device(device)

        if device not in self._devices:
            self._devices.append(device)

        room.add_device(device)
        return device

    def get_device(self, device_id):
        # This method retrieves a device object via its id.
        for device in self._devices:
            if device.id == device_id:
                return device
        return None

    def get_devices(self):
        # Return a list of all registered devices in the house.
        return self._devices
    
    def get_device_by_id(self, device_id):
        # Return a device object via its id by delegating to get_device().
        return self.get_device(device_id)
    
    def _find_floor(self, level):
        # Find and return a floor object by its level. 
        # Return None if no such floor exists.
        for floor in self._floors:
            if floor.level == level:
                return floor
        return None
