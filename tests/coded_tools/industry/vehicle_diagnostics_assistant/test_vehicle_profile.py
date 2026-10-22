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

from coded_tools.industry.vehicle_diagnostics_assistant.vehicle_profile import VehicleProfile


class TestVehicleProfile(TestCase):
    """
    Unit tests for the VehicleProfile CodedTool.
    """

    def test_profile_from_sly_data(self) -> None:
        """
        The vehicle is resolved from the VIN in sly_data and the VIN is not returned.
        """
        sly_data = {"vin": "WBA7E2C51KB000002", "current_date": "2026-10-22"}
        response = VehicleProfile().invoke(args={}, sly_data=sly_data)
        self.assertEqual("530e", response.get("model"))
        self.assertTrue(response.get("warranty").startswith("active"))
        self.assertNotIn("WBA7E2C51KB000002", str(response))

    def test_expired_warranty(self) -> None:
        """
        The warranty is reported as expired after its end date.
        """
        sly_data = {"vin": "WVWZZZ1KZ8W000001", "current_date": "2026-10-22"}
        response = VehicleProfile().invoke(args={}, sly_data=sly_data)
        self.assertTrue(response.get("warranty").startswith("expired"))

    def test_missing_or_unknown_vin(self) -> None:
        """
        An error is returned when no VIN is linked or the VIN is unknown.
        """
        self.assertIn("error", VehicleProfile().invoke(args={}, sly_data={}))
        self.assertIn("error", VehicleProfile().invoke(args={}, sly_data={"vin": "UNKNOWN"}))
