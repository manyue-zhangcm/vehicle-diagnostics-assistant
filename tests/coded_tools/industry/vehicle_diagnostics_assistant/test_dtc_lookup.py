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

from coded_tools.industry.vehicle_diagnostics_assistant.dtc_lookup import DtcLookup


class TestDtcLookup(TestCase):
    """
    Unit tests for the DtcLookup CodedTool.
    """

    def test_lookup_known_and_unknown_codes(self) -> None:
        """
        Known codes are returned with their record, unknown codes are listed separately, case-insensitively.
        """
        response = DtcLookup().invoke(args={"dtc_codes": "p0301, P9999"}, sly_data={})
        self.assertEqual(["P0301"], list(response.get("codes").keys()))
        self.assertEqual("high", response.get("codes").get("P0301").get("severity"))
        self.assertEqual(["P9999"], response.get("unknown_codes"))

    def test_search_by_symptoms(self) -> None:
        """
        Symptom search returns candidate codes ranked by shared keywords.
        """
        response = DtcLookup().invoke(
            args={"symptoms": "high voltage warning, will not go into ready mode"}, sly_data={}
        )
        candidates = list(response.get("candidate_codes").keys())
        self.assertEqual("P0AA6", candidates[0])
        self.assertLessEqual(len(candidates), DtcLookup.MAX_SYMPTOM_MATCHES)

    def test_missing_input(self) -> None:
        """
        An error is returned when neither codes nor symptoms are provided.
        """
        response = DtcLookup().invoke(args={}, sly_data={})
        self.assertIn("error", response)
