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

from coded_tools.industry.vehicle_diagnostics_assistant.service_slots import ServiceSlots


class TestServiceSlots(TestCase):
    """
    Unit tests for the ServiceSlots CodedTool.
    """

    def test_slots_skip_weekend(self) -> None:
        """
        On a Friday, slots start on the following Monday and are deterministic.
        """
        response = ServiceSlots().invoke(args={}, sly_data={"current_date": "2026-10-23"})
        slots = response.get("open_slots")
        self.assertEqual(ServiceSlots.MAX_SLOTS, len(slots))
        self.assertEqual("2026-10-26 10:30", slots[0])
        self.assertTrue(all(not slot.startswith(("2026-10-24", "2026-10-25")) for slot in slots))
