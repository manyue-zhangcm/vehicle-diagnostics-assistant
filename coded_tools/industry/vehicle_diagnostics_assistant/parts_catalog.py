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


class PartsCatalog:  # pylint: disable=too-few-public-methods
    """
    Read-only mock parts inventory for the service center. Prices are in EUR.
    """

    PARTS: dict[str, dict[str, Any]] = {
        "TH-0128": {"name": "Thermostat with gasket", "price_eur": 48.90, "in_stock": 6, "lead_time_days": 0},
        "CTS-0118": {"name": "Coolant temperature sensor", "price_eur": 32.50, "in_stock": 4, "lead_time_days": 0},
        "IMG-0171": {"name": "Intake manifold gasket set", "price_eur": 39.00, "in_stock": 2, "lead_time_days": 0},
        "MAF-0101": {"name": "Mass air flow sensor", "price_eur": 189.00, "in_stock": 0, "lead_time_days": 2},
        "SP-IR-01": {"name": "Iridium spark plug (single)", "price_eur": 14.90, "in_stock": 24, "lead_time_days": 0},
        "SP-IR-04": {"name": "Iridium spark plug set (4 pcs)", "price_eur": 55.00, "in_stock": 5, "lead_time_days": 0},
        "IC-0301": {"name": "Ignition coil", "price_eur": 74.50, "in_stock": 3, "lead_time_days": 0},
        "FI-0201": {"name": "Fuel injector", "price_eur": 129.00, "in_stock": 0, "lead_time_days": 3},
        "O2-DN-02": {"name": "Downstream oxygen sensor", "price_eur": 96.00, "in_stock": 2, "lead_time_days": 0},
        "CAT-B1-01": {"name": "Catalytic converter (bank 1)", "price_eur": 845.00, "in_stock": 0, "lead_time_days": 5},
        "BAT-12V-70": {"name": "12V AGM battery 70Ah", "price_eur": 169.00, "in_stock": 8, "lead_time_days": 0},
        "ALT-150A": {"name": "Alternator 150A", "price_eur": 412.00, "in_stock": 1, "lead_time_days": 0},
        "SS-0750": {"name": "Transmission shift solenoid", "price_eur": 118.00, "in_stock": 0, "lead_time_days": 4},
        "ATF-SVC-01": {
            "name": "Transmission fluid and filter kit",
            "price_eur": 89.00,
            "in_stock": 7,
            "lead_time_days": 0,
        },
        "WSS-LF-01": {
            "name": "Wheel speed sensor, front left",
            "price_eur": 64.00,
            "in_stock": 3,
            "lead_time_days": 0,
        },
        "CAN-HARN-01": {"name": "CAN bus wiring repair kit", "price_eur": 58.00, "in_stock": 2, "lead_time_days": 0},
    }
