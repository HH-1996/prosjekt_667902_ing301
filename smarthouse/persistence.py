import sqlite3
from typing import Optional
from smarthouse.domain import (
    Measurement,
    SmartHouse,
    TemperatureSensor,
    MotionSensor,
    LightBulp,
    SmartLock,
    HeatPump,
    Sensor,
    Actuator,
)

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file 
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    def _create_device_from_row(self, row):
        device_id, room_id, kind, category, supplier, product = row

        if category == "sensor":
            if kind == "Temperature Sensor":
                return TemperatureSensor(device_id, supplier, product)
            elif kind == "Motion Sensor":
                return MotionSensor(device_id, supplier, product)
            elif kind == "CO2 sensor":
                return Sensor(device_id, supplier, product, kind, "ppm")
            elif kind == "Humidity Sensor":
                return Sensor(device_id, supplier, product, kind, "%")
            elif kind == "Electricity Meter":
                return Sensor(device_id, supplier, product, kind, "kWh")
            elif kind == "Air Quality Sensor":
                return Sensor(device_id, supplier, product, kind, "AQI")
            elif kind == "Smart Oven":
                return Sensor(device_id, supplier, product, kind, "°C")
            else:
                return Sensor(device_id, supplier, product, kind, "")

        elif category == "actuator":
            if kind == "Light Bulp":
                return LightBulp(device_id, supplier, product)
            elif kind == "Smart Lock":
                return SmartLock(device_id, supplier, product)
            elif kind == "Heat Pump":
                return HeatPump(device_id, supplier, product)
            else:
                return Actuator(device_id, supplier, product, kind)

        return None


    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices)
        are retrieved as well.
        """
        house = SmartHouse()
        cur = self.conn.cursor()

        # 1. Load all rooms
        cur.execute("""
            SELECT id, floor, area, name
            FROM rooms
            ORDER BY floor, id
        """)
        room_rows = cur.fetchall()

        room_map = {}

        for room_id, floor_level, area, name in room_rows:
            floor_obj = house.register_floor(floor_level)
            room_obj = house.register_room(floor_obj, area, name)
            room_map[room_id] = room_obj

        # 2. Load all devices and attach them to the correct room
        cur.execute("""
            SELECT id, room, kind, category, supplier, product
            FROM devices
            ORDER BY room, id
        """)
        device_rows = cur.fetchall()

        for row in device_rows:
            device = self._create_device_from_row(row)
            if device is None:
                continue

            room_id = row[1]
            room_obj = room_map.get(room_id)

            if room_obj is not None:
                house.register_device(room_obj, device)

        # 3. Restore persisted actuator states if the table exists
        cur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'actuator_states'
        """)
        table_exists = cur.fetchone()

        if table_exists:
            cur.execute("""
                SELECT device, is_active, target_value
                FROM actuator_states
            """)
            state_rows = cur.fetchall()

            for device_id, is_active, target_value in state_rows:
                device = house.get_device_by_id(device_id)
                if device is not None and device.is_actuator():
                    if is_active:
                        device.turn_on(target_value)
                    else:
                        device.turn_off()
        cur.close()
        return house


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        if sensor is None or not sensor.is_sensor():
            return None

        cur = self.conn.cursor()
        cur.execute("""
            SELECT ts, value
            FROM measurements
            WHERE device = ?
            ORDER BY ts DESC
            LIMIT 1
        """, (sensor.id,))
        row = cur.fetchone()
        cur.close()

        if row is None:
            return None

        ts, value = row
        return Measurement(ts, value, sensor.unit)

    def _ensure_actuator_state_table(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS actuator_states (
                device TEXT PRIMARY KEY,
                is_active INTEGER NOT NULL,
                target_value REAL,
                FOREIGN KEY(device) REFERENCES devices(id)
            )
        """)
        self.conn.commit()
        cur.close()

    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        if actuator is None or not actuator.is_actuator():
            return

        self._ensure_actuator_state_table()

        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO actuator_states(device, is_active, target_value)
            VALUES (?, ?, ?)
            ON CONFLICT(device) DO UPDATE SET
                is_active = excluded.is_active,
                target_value = excluded.target_value
        """, (
            actuator.id,
            1 if actuator.is_active() else 0,
            actuator.target_value
        ))
        self.conn.commit()
        cur.close()


    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        cur = self.conn.cursor()

        # Finn room-id via rooms-tabellen, siden Room-objektet ikke lagrer id direkte
        cur.execute("""
            SELECT id
            FROM rooms
            WHERE floor = ? AND area = ? AND name = ?
            LIMIT 1
        """, (room.floor.level, room.room_size, room.room_name))
        row = cur.fetchone()

        if row is None:
            cur.close()
            return {}

        room_id = row[0]

        sql = """
            SELECT date(m.ts) AS day, ROUND(AVG(m.value), 4) AS avg_temp
            FROM measurements m
            JOIN devices d ON d.id = m.device
            WHERE d.room = ?
            AND m.unit = '°C'
        """
        params = [room_id]

        if from_date is not None:
            sql += " AND date(m.ts) >= date(?)"
            params.append(from_date)

        if until_date is not None:
            sql += " AND date(m.ts) <= date(?)"
            params.append(until_date)

        sql += """
            GROUP BY date(m.ts)
            ORDER BY day
        """

        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()

        return {day: avg_temp for day, avg_temp in rows}
    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        cur = self.conn.cursor()

        cur.execute("""
            SELECT id
            FROM rooms
            WHERE floor = ? AND area = ? AND name = ?
            LIMIT 1
        """, (room.floor.level, room.room_size, room.room_name))
        row = cur.fetchone()

        if row is None:
            cur.close()
            return []

        room_id = row[0]

        sql = """
            WITH day_avg AS (
                SELECT AVG(m.value) AS avg_humidity
                FROM measurements m
                JOIN devices d ON d.id = m.device
                WHERE d.room = ?
                AND d.kind = 'Humidity Sensor'
                AND date(m.ts) = date(?)
            )
            SELECT CAST(strftime('%H', m.ts) AS INTEGER) AS hour
            FROM measurements m
            JOIN devices d ON d.id = m.device
            CROSS JOIN day_avg a
            WHERE d.room = ?
            AND d.kind = 'Humidity Sensor'
            AND date(m.ts) = date(?)
            AND m.value > a.avg_humidity
            GROUP BY CAST(strftime('%H', m.ts) AS INTEGER)
            HAVING COUNT(*) > 3
            ORDER BY hour
        """

        cur.execute(sql, (room_id, date, room_id, date))
        rows = cur.fetchall()
        cur.close()

        return [hour for (hour,) in rows]