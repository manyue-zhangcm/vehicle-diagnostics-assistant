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

import datetime
import logging
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.industry.vehicle_diagnostics_assistant.session_clock import SessionClock
from coded_tools.industry.vehicle_diagnostics_assistant.vehicle_registry import VehicleRegistry

logger = logging.getLogger(__name__)


class VehicleProfile(CodedTool):
    """
    Returns the profile of the vehicle linked to the session. The VIN is read from sly_data,
    so it never appears in the conversation or reaches the LLM.
    """

    def invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        :param args: an empty dictionary (not used).
        :param sly_data: a dictionary with the following keys:
            - vin: the vehicle identification number of the user's vehicle
            - current_date: optional - "YYYY-MM-DD" date override used for the warranty check
        :return: make, model, year, powertrain, mileage and warranty status, or an error message.
        """
        vin: str | None = sly_data.get("vin")
        if not vin:
            return {"error": "No vehicle is linked to this session. Ask the user for make, model, year and mileage."}

        vehicle: dict[str, Any] | None = VehicleRegistry.VEHICLES.get(vin)
        if vehicle is None:
            logger.warning("The vehicle linked to the session is not in the registry")
            return {"error": "The linked vehicle is not in the registry. Ask the user for make, model and year."}

        warranty_until: datetime.date = datetime.date.fromisoformat(vehicle.get("warranty_until"))
        in_warranty: bool = SessionClock.today(sly_data) <= warranty_until
        return {
            "make": vehicle.get("make"),
            "model": vehicle.get("model"),
            "year": vehicle.get("year"),
            "powertrain": vehicle.get("powertrain"),
            "mileage_km": vehicle.get("mileage_km"),
            "warranty": f"{'active' if in_warranty else 'expired'} (until {warranty_until.isoformat()})",
        }

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        Delegates to the synchronous invoke method because it's an in-memory lookup.
        """
        return self.invoke(args, sly_data)
