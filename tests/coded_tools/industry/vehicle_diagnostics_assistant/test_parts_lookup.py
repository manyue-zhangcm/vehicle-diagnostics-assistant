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

from coded_tools.industry.vehicle_diagnostics_assistant.parts_lookup import PartsLookup


class TestPartsLookup(TestCase):
    """
    Unit tests for the PartsLookup CodedTool.
    """

    def test_lookup_parts(self) -> None:
        """
        Availability, total price and unknown parts are reported.
        """
        response = PartsLookup().invoke(args={"part_numbers": "SP-IR-01 FI-0201, NOPE-1"}, sly_data={})
        parts = response.get("parts")
        self.assertEqual("in stock", parts.get("SP-IR-01").get("availability"))
        self.assertEqual("order needed, 3 days", parts.get("FI-0201").get("availability"))
        self.assertEqual(["NOPE-1"], response.get("unknown_part_numbers"))
        self.assertAlmostEqual(143.90, response.get("total_parts_price_eur"))

    def test_missing_part_numbers(self) -> None:
        """
        An error is returned when no part number is provided.
        """
        self.assertIn("error", PartsLookup().invoke(args={"part_numbers": " "}, sly_data={}))
