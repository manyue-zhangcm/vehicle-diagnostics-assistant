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


class VehicleRegistry:  # pylint: disable=too-few-public-methods
    """
    Read-only mock registry of connected vehicles, keyed by VIN.
    """

    VEHICLES: dict[str, dict[str, Any]] = {
        "WVWZZZ1KZ8W000001": {
            "make": "Volkswagen",
            "model": "Golf 1.4 TSI",
            "year": 2019,
            "powertrain": "gasoline",
            "mileage_km": 86400,
            "warranty_until": "2024-05-31",
        },
        "WBA7E2C51KB000002": {
            "make": "BMW",
            "model": "530e",
            "year": 2022,
            "powertrain": "plug-in hybrid",
            "mileage_km": 31800,
            "warranty_until": "2027-03-31",
        },
        "WMEEJ9AA5FK000003": {
            "make": "Mercedes-Benz",
            "model": "EQA 250",
            "year": 2023,
            "powertrain": "battery electric",
            "mileage_km": 12900,
            "warranty_until": "2028-08-31",
        },
    }
