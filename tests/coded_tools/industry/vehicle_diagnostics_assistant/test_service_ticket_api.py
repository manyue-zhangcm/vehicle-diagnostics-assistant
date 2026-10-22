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

from unittest import TestCase

from coded_tools.industry.vehicle_diagnostics_assistant.service_ticket_api import ServiceTicketApi


class TestServiceTicketApi(TestCase):
    """
    Unit tests for the ServiceTicketApi CodedTool.
    """

    VIN = "WVWZZZ1KZ8W000001"
    ARGS = {
        "appointment_slot": "2026-10-26 10:30",
        "customer_complaint": "Engine shakes at idle",
        "diagnosis_summary": "Cylinder 1 misfire",
        "severity": "High",
        "dtc_codes": "P0301",
    }

    def test_open_ticket(self) -> None:
        """
        A ticket is opened, stored in full in sly_data and returned with a masked VIN.
        """
        sly_data = {"vin": self.VIN, "customer_name": "Manyue"}
        response = ServiceTicketApi().invoke(args=self.ARGS, sly_data=sly_data)
        self.assertTrue(response.get("ticket_id").startswith("WO-"))
        self.assertEqual("high", response.get("severity"))
        self.assertEqual("2019 Volkswagen Golf 1.4 TSI", response.get("vehicle"))
        self.assertNotIn(self.VIN, str(response))
        self.assertTrue(response.get("vin").endswith("0001"))
        stored = sly_data.get("service_tickets")[0]
        self.assertEqual(self.VIN, stored.get("vin"))
        self.assertEqual(response.get("ticket_id"), stored.get("ticket_id"))

    def test_ticket_ids_are_unique(self) -> None:
        """
        Each ticket gets a new ID, even across instances.
        """
        sly_data = {"vin": self.VIN, "customer_name": "Manyue"}
        first = ServiceTicketApi().invoke(args=self.ARGS, sly_data=sly_data)
        second = ServiceTicketApi().invoke(args=self.ARGS, sly_data=sly_data)
        self.assertNotEqual(first.get("ticket_id"), second.get("ticket_id"))

    def test_validation_errors(self) -> None:
        """
        Missing VIN, customer name, invalid severity or slot are reported as errors.
        """
        api = ServiceTicketApi()
        self.assertIn("error", api.invoke(args=self.ARGS, sly_data={"customer_name": "Manyue"}))
        self.assertIn("name", api.invoke(args=self.ARGS, sly_data={"vin": self.VIN}).get("error"))
        args_with_name = dict(self.ARGS, customer_name="Manyue")
        self.assertNotIn("error", api.invoke(args=args_with_name, sly_data={"vin": self.VIN}))
        bad_severity = dict(self.ARGS, severity="urgent")
        self.assertIn(
            "Severity", api.invoke(args=bad_severity, sly_data={"vin": self.VIN, "customer_name": "M"}).get("error")
        )
        bad_slot = dict(self.ARGS, appointment_slot="tomorrow")
        self.assertIn("slot", api.invoke(args=bad_slot, sly_data={"vin": self.VIN, "customer_name": "M"}).get("error"))
