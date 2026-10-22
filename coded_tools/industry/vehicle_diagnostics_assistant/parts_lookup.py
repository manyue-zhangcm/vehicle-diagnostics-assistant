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

from coded_tools.industry.vehicle_diagnostics_assistant.parts_catalog import PartsCatalog

logger = logging.getLogger(__name__)


class PartsLookup(CodedTool):
    """
    Checks price, stock and lead time of parts in the service center's mock inventory.
    """

    def invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        :param args: a dictionary with the following key:
            - part_numbers: comma or space separated part numbers, e.g. "SP-IR-01, IC-0301"
        :param sly_data: not used.
        :return: a dictionary with availability per part, unknown part numbers and the total parts price.
        """
        part_numbers_text: str = args.get("part_numbers") or ""
        requested: list[str] = [part.upper() for part in re.split(r"[\s,;]+", part_numbers_text.strip()) if part]
        if not requested:
            return {"error": "Provide at least one part number."}

        parts: dict[str, Any] = {}
        unknown: list[str] = []
        total_price: float = 0.0
        for part_number in requested:
            record: dict[str, Any] | None = PartsCatalog.PARTS.get(part_number)
            if record is None:
                unknown.append(part_number)
                continue
            in_stock: int = record.get("in_stock", 0)
            parts[part_number] = {
                "name": record.get("name"),
                "price_eur": record.get("price_eur"),
                "availability": "in stock" if in_stock > 0 else f"order needed, {record.get('lead_time_days')} days",
            }
            total_price += record.get("price_eur", 0.0)
        logger.info("Parts lookup: %d found, %d unknown", len(parts), len(unknown))
        return {"parts": parts, "unknown_part_numbers": unknown, "total_parts_price_eur": round(total_price, 2)}

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        Delegates to the synchronous invoke method because it's an in-memory lookup.
        """
        return self.invoke(args, sly_data)
