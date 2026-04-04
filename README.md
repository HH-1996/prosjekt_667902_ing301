# ING301 – SmartHouse-prosjekt

Dette repoet har min løsning på SmartHouse-prosjektet i **ING301**.

Prosjektet modellerer et smart hus med etasjer, rom, sensorer, aktuatorer og målinger.  
Løsningen er bygget opp i to deler:

- **Del A:** domenemodell for SmartHouse
- **Del B:** persistens og databehandling med SQLite

I Del B er løsningen utvidet slik at SmartHouse-strukturen kan lastes fra database, sensorverdier kan hentes ut, aktuatorstatus kan lagres, og statistiske spørringer kan kjøres på måledata.

---

## Prosjektbeskrivelse

SmartHouse-prosjektet modellerer et hus med:

- etasjer
- rom
- enheter
- sensorer
- aktuatorer
- målinger

Domenemodellen er implementert i `smarthouse/domain.py`, mens databasepersistens og SQL-basert analyse er implementert i `smarthouse/persistence.py`.

Prosjektet bruker en SQLite-database i `data/db.sql` som datakilde for rom, enheter og måledata.

---

## Funksjonalitet

### Del A – domenemodell

Del A implementerer selve objektmodellen for SmartHouse, inkludert:

- `SmartHouse`
- `Floor`
- `Room`
- `Device`
- `Sensor`
- `Actuator`
- `Measurement`

Det finnes også konkrete underklasser for enkelte enheter, som for eksempel:

- `TemperatureSensor`
- `MotionSensor`
- `LightBulp`
- `SmartLock`
- `HeatPump`

---

### Del B – persistens og analyse

I Del B er følgende funksjonalitet implementert i `SmartHouseRepository`:

#### `load_smarthouse_deep()`

Laster hele SmartHouse-strukturen fra databasen, inkludert:

- etasjer
- rom
- devices

#### `get_latest_reading(sensor)`

Henter den siste registrerte målingen for en gitt sensor.

#### `update_actuator_state(actuator)`

Lagrer tilstanden til en aktuator i databasen, slik at status bevares etter reconnect.

#### `calc_avg_temperatures_in_room(room, from_date, until_date)`

Beregner gjennomsnittlig temperatur per dag i et rom innenfor et valgfritt datointervall.

#### `calc_hours_with_humidity_above(room, date)`

Returnerer hvilke timer i et gitt døgn som har mer enn tre luftfuktighetsmålinger over gjennomsnittet for rommet den dagen.

---

## Prosjektstruktur

```text
prosjekt_667902_ing301/
├── data/
│   └── db.sql
├── smarthouse/
│   ├── __init__.py
│   ├── domain.py
│   └── persistence.py
├── tests/
│   ├── __init__.py
│   ├── demo_house.py
│   ├── test_part_a.py
│   └── test_part_b.py
├── demo_house.py
├── domainmodel.png
└── README.md
```
