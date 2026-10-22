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
import itertools
import logging
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.industry.vehicle_diagnostics_assistant.vehicle_registry import VehicleRegistry

logger = logging.getLogger(__name__)


class ServiceTicketApi(CodedTool):
    """
    Mock workshop work-order API: books an appointment and opens a service ticket for the technicians.
    The full ticket, including the VIN, is stored in sly_data["service_tickets"] for the client application,
    while the agents only see a summary with a masked VIN.
    """

    # Shared across instances so ticket IDs stay unique for the lifetime of the server.
    _ticket_ids = itertools.count(1001)
    SLOT_FORMAT: str = "%Y-%m-%d %H:%M"
    VISIBLE_VIN_CHARS: int = 4
    SEVERITIES: tuple[str, ...] = ("low", "medium", "high", "critical")

    def invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        :param args: a dictionary with the following keys:
            - appointment_slot: required - one of the open slots, formatted "YYYY-MM-DD HH:MM"
            - customer_complaint: required - what the driver reported, in their own words
            - diagnosis_summary: required - the preliminary diagnosis
            - severity: required - one of low, medium, high, critical
            - dtc_codes: optional - comma separated diagnostic trouble codes
            - recommended_repairs: optional - repairs to perform
            - part_numbers: optional - comma separated parts to prepare
            - customer_name: optional - used only when sly_data has no customer_name
        :param sly_data: a dictionary with the following keys:
            - vin: the vehicle identification number
            - customer_name: optional - the name of the vehicle owner
        :return: a ticket summary for the agents, or an error message describing what is missing.
        """
        error: str | None = self.validate(args, sly_data)
        if error:
            return {"error": error}

        vin: str = sly_data.get("vin")
        vehicle: dict[str, Any] = VehicleRegistry.VEHICLES.get(vin) or {}
        ticket_id: str = f"WO-{next(self._ticket_ids)}"
        ticket: dict[str, Any] = {
            "ticket_id": ticket_id,
            "status": "OPEN",
            "appointment_slot": args.get("appointment_slot"),
            "customer_name": sly_data.get("customer_name") or args.get("customer_name"),
            "vin": vin,
            "vehicle": f"{vehicle.get('year', '')} {vehicle.get('make', '')} {vehicle.get('model', '')}".strip(),
            "severity": args.get("severity").lower(),
            "dtc_codes": args.get("dtc_codes") or "",
            "customer_complaint": args.get("customer_complaint"),
            "diagnosis_summary": args.get("diagnosis_summary"),
            "recommended_repairs": args.get("recommended_repairs") or "",
            "part_numbers": args.get("part_numbers") or "",
        }
        sly_data.setdefault("service_tickets", []).append(ticket)
        logger.info("Opened service ticket %s with severity %s", ticket_id, ticket.get("severity"))

        summary: dict[str, Any] = dict(ticket)
        summary["vin"] = "*" * (len(vin) - self.VISIBLE_VIN_CHARS) + vin[-self.VISIBLE_VIN_CHARS :]
        return summary

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        Delegates to the synchronous invoke method because it's an in-memory operation.
        """
        return self.invoke(args, sly_data)

    def validate(self, args: dict[str, Any], sly_data: dict[str, Any]) -> str | None:
        """
        :param args: the tool arguments, see invoke.
        :param sly_data: the private session data, see invoke.
        :return: a message describing the first problem found, or None if the request is valid.
        """
        if not sly_data.get("vin"):
            return "No vehicle is linked to this session, so a service ticket cannot be opened."
        if not (sly_data.get("customer_name") or args.get("customer_name")):
            return "Ask the customer for their name before opening a service ticket."
        for required in ("customer_complaint", "diagnosis_summary"):
            if not args.get(required):
                return f"Missing required field: {required}."
        severity: str = (args.get("severity") or "").lower()
        if severity not in self.SEVERITIES:
            return f"Severity must be one of: {', '.join(self.SEVERITIES)}."
        try:
            datetime.datetime.strptime(args.get("appointment_slot") or "", self.SLOT_FORMAT)
        except ValueError:
            return "Appointment slot must be one of the open slots, formatted YYYY-MM-DD HH:MM."
        return None
