# Copyright © 2025-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

from typing import Any


class DtcCatalog:  # pylint: disable=too-few-public-methods
    """
    Read-only mock knowledge base of OBD-II diagnostic trouble codes (DTCs).
    Stands in for an OEM diagnostic database in this demo network.
    """

    CODES: dict[str, dict[str, Any]] = {
        "P0128": {
            "description": "Coolant thermostat: coolant temperature below thermostat regulating temperature",
            "system": "Engine cooling",
            "severity": "low",
            "drivable": "Yes. Safe to drive, but fuel economy and cabin heating are reduced.",
            "symptoms": [
                "check engine light",
                "heater blows cold air",
                "temperature gauge stays low",
                "poor fuel economy",
            ],
            "possible_causes": ["Thermostat stuck open", "Faulty coolant temperature sensor", "Low coolant level"],
            "recommended_repairs": [
                {"repair": "Replace thermostat and gasket", "part_numbers": ["TH-0128"], "labor_hours": 1.2},
                {"repair": "Replace coolant temperature sensor", "part_numbers": ["CTS-0118"], "labor_hours": 0.5},
            ],
        },
        "P0171": {
            "description": "System too lean (bank 1)",
            "system": "Fuel and air metering",
            "severity": "medium",
            "drivable": "Yes, for short distances. Have it checked within a week to avoid engine damage.",
            "symptoms": ["check engine light", "rough idle", "hesitation when accelerating", "hissing noise"],
            "possible_causes": ["Vacuum leak", "Dirty or faulty mass air flow (MAF) sensor", "Weak fuel pump"],
            "recommended_repairs": [
                {
                    "repair": "Smoke test and replace intake manifold gasket",
                    "part_numbers": ["IMG-0171"],
                    "labor_hours": 1.5,
                },
                {"repair": "Replace mass air flow sensor", "part_numbers": ["MAF-0101"], "labor_hours": 0.4},
            ],
        },
        "P0300": {
            "description": "Random or multiple cylinder misfire detected",
            "system": "Ignition",
            "severity": "high",
            "drivable": "Limit driving. If the check engine light is flashing, stop driving: the catalytic converter "
            "can be damaged.",
            "symptoms": ["flashing check engine light", "engine shaking", "rough idle", "loss of power"],
            "possible_causes": ["Worn spark plugs", "Faulty ignition coils", "Vacuum leak", "Low fuel pressure"],
            "recommended_repairs": [
                {"repair": "Replace all spark plugs", "part_numbers": ["SP-IR-04"], "labor_hours": 1.0},
                {"repair": "Replace ignition coil pack", "part_numbers": ["IC-0301"], "labor_hours": 0.6},
            ],
        },
        "P0301": {
            "description": "Cylinder 1 misfire detected",
            "system": "Ignition",
            "severity": "high",
            "drivable": "Limit driving. If the check engine light is flashing, stop driving: the catalytic converter "
            "can be damaged.",
            "symptoms": ["check engine light", "engine shaking", "rough idle", "loss of power"],
            "possible_causes": [
                "Worn spark plug on cylinder 1",
                "Faulty ignition coil on cylinder 1",
                "Clogged fuel injector on cylinder 1",
                "Low compression on cylinder 1",
            ],
            "recommended_repairs": [
                {"repair": "Replace cylinder 1 spark plug", "part_numbers": ["SP-IR-01"], "labor_hours": 0.4},
                {"repair": "Replace cylinder 1 ignition coil", "part_numbers": ["IC-0301"], "labor_hours": 0.4},
                {
                    "repair": "Clean or replace cylinder 1 fuel injector",
                    "part_numbers": ["FI-0201"],
                    "labor_hours": 1.1,
                },
            ],
        },
        "P0420": {
            "description": "Catalyst system efficiency below threshold (bank 1)",
            "system": "Emissions",
            "severity": "medium",
            "drivable": "Yes. Safe to drive, but the vehicle may fail an emissions inspection.",
            "symptoms": ["check engine light", "rotten egg smell", "reduced performance"],
            "possible_causes": ["Worn catalytic converter", "Faulty downstream oxygen sensor", "Exhaust leak"],
            "recommended_repairs": [
                {"repair": "Replace downstream oxygen sensor", "part_numbers": ["O2-DN-02"], "labor_hours": 0.5},
                {"repair": "Replace catalytic converter", "part_numbers": ["CAT-B1-01"], "labor_hours": 2.0},
            ],
        },
        "P0562": {
            "description": "System voltage low",
            "system": "Charging system",
            "severity": "medium",
            "drivable": "Yes, but the vehicle may not restart. Have it checked as soon as possible.",
            "symptoms": ["battery warning light", "dim headlights", "slow engine crank", "car will not start"],
            "possible_causes": ["Weak 12V battery", "Failing alternator", "Corroded battery terminals"],
            "recommended_repairs": [
                {"repair": "Replace 12V battery", "part_numbers": ["BAT-12V-70"], "labor_hours": 0.3},
                {"repair": "Replace alternator", "part_numbers": ["ALT-150A"], "labor_hours": 1.8},
            ],
        },
        "P0700": {
            "description": "Transmission control system malfunction",
            "system": "Transmission",
            "severity": "high",
            "drivable": "Limit driving. The transmission may be in limp mode with reduced gears.",
            "symptoms": ["harsh shifting", "stuck in gear", "limp mode", "check engine light"],
            "possible_causes": [
                "Faulty shift solenoid",
                "Low or burnt transmission fluid",
                "Transmission control module fault",
            ],
            "recommended_repairs": [
                {
                    "repair": "Read transmission module codes and replace shift solenoid",
                    "part_numbers": ["SS-0750"],
                    "labor_hours": 2.5,
                },
                {
                    "repair": "Transmission fluid and filter service",
                    "part_numbers": ["ATF-SVC-01"],
                    "labor_hours": 1.0,
                },
            ],
        },
        "P0AA6": {
            "description": "Hybrid/EV high-voltage battery voltage system isolation fault",
            "system": "High-voltage battery",
            "severity": "critical",
            "drivable": "No. Stop the vehicle in a safe place, do not touch orange high-voltage cables and call "
            "roadside assistance.",
            "symptoms": ["high voltage warning", "vehicle will not go into ready mode", "electric smell"],
            "possible_causes": [
                "Damaged high-voltage cable insulation",
                "Coolant leak in battery pack",
                "Faulty inverter",
            ],
            "recommended_repairs": [
                {
                    "repair": "High-voltage isolation test and battery pack inspection by certified technician",
                    "part_numbers": [],
                    "labor_hours": 3.0,
                },
            ],
        },
        "C0035": {
            "description": "Left front wheel speed sensor circuit",
            "system": "Brakes (ABS)",
            "severity": "medium",
            "drivable": "Yes, carefully. Normal brakes work, but ABS and stability control are disabled.",
            "symptoms": ["abs warning light", "traction control light", "brake pedal pulsing"],
            "possible_causes": ["Faulty wheel speed sensor", "Damaged sensor wiring", "Dirty tone ring"],
            "recommended_repairs": [
                {"repair": "Replace left front wheel speed sensor", "part_numbers": ["WSS-LF-01"], "labor_hours": 0.7},
            ],
        },
        "U0100": {
            "description": "Lost communication with engine control module (ECM)",
            "system": "Vehicle network (CAN bus)",
            "severity": "critical",
            "drivable": "No. The engine may stall without warning. Have the vehicle towed.",
            "symptoms": ["engine stalls", "multiple warning lights", "car will not start", "gauges not working"],
            "possible_causes": ["Damaged CAN bus wiring", "Failed engine control module", "Poor ground connection"],
            "recommended_repairs": [
                {"repair": "CAN bus wiring diagnosis and repair", "part_numbers": ["CAN-HARN-01"], "labor_hours": 2.0},
            ],
        },
    }
