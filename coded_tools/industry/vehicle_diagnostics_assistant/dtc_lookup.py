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

import logging
import re
from typing import Any

from neuro_san.interfaces.coded_tool import CodedTool

from coded_tools.industry.vehicle_diagnostics_assistant.dtc_catalog import DtcCatalog

logger = logging.getLogger(__name__)


class DtcLookup(CodedTool):
    """
    Looks up diagnostic trouble codes (DTCs) in the mock DTC catalog, either by code or by symptom description.
    """

    MAX_SYMPTOM_MATCHES: int = 3
    MIN_KEYWORD_LENGTH: int = 4

    def invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        :param args: a dictionary with the following optional keys (at least one is required):
            - dtc_codes: comma or space separated codes, e.g. "P0301, P0420"
            - symptoms: free-text description of what the driver notices
        :param sly_data: not used.
        :return: a dictionary with the matching DTC records, unknown codes, or an error message.
        """
        codes_text: str = args.get("dtc_codes") or ""
        symptoms: str = args.get("symptoms") or ""
        if not codes_text.strip() and not symptoms.strip():
            return {"error": "Provide at least one DTC code or a description of the symptoms."}

        if codes_text.strip():
            return self.lookup_codes(codes_text)
        return self.search_symptoms(symptoms)

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        Delegates to the synchronous invoke method because it's an in-memory lookup.
        """
        return self.invoke(args, sly_data)

    def lookup_codes(self, codes_text: str) -> dict[str, Any]:
        """
        :param codes_text: comma or space separated DTC codes.
        :return: the catalog records found and the codes that are not in the catalog.
        """
        requested: list[str] = [code.upper() for code in re.split(r"[\s,;]+", codes_text.strip()) if code]
        found: dict[str, Any] = {}
        unknown: list[str] = []
        for code in requested:
            record: dict[str, Any] | None = DtcCatalog.CODES.get(code)
            if record:
                found[code] = record
            else:
                unknown.append(code)
        logger.info("DTC lookup: %d found, %d unknown", len(found), len(unknown))
        return {"codes": found, "unknown_codes": unknown}

    def search_symptoms(self, symptoms: str) -> dict[str, Any]:
        """
        Ranks catalog codes by how many symptom keywords they share with the description.

        :param symptoms: free-text description of the symptoms.
        :return: up to MAX_SYMPTOM_MATCHES candidate codes, best match first.
        """
        keywords: set[str] = {
            word for word in re.findall(r"[a-z]+", symptoms.lower()) if len(word) >= self.MIN_KEYWORD_LENGTH
        }
        scored: list[tuple[int, str]] = []
        for code, record in DtcCatalog.CODES.items():
            symptom_words: set[str] = set(re.findall(r"[a-z]+", " ".join(record.get("symptoms", [])).lower()))
            score: int = len(keywords & symptom_words)
            if score > 0:
                scored.append((score, code))
        scored.sort(key=lambda item: (-item[0], item[1]))
        candidates: dict[str, Any] = {
            code: DtcCatalog.CODES.get(code) for _, code in scored[: self.MAX_SYMPTOM_MATCHES]
        }
        logger.info("Symptom search returned %d candidate codes", len(candidates))
        return {
            "candidate_codes": candidates,
            "note": "Candidates are inferred from symptoms only. Reading the actual codes with an OBD-II scanner "
            "confirms the diagnosis.",
        }
