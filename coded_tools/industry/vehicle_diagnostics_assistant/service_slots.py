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

logger = logging.getLogger(__name__)


class ServiceSlots(CodedTool):
    """
    Lists open workshop appointment slots for the next business days.
    Occupancy is simulated with a fixed pattern so results are deterministic for a given date.
    """

    SLOT_TIMES: tuple[str, ...] = ("08:00", "10:30", "14:00", "16:30")
    BUSINESS_DAYS_AHEAD: int = 5
    MAX_SLOTS: int = 6
    SATURDAY: int = 5

    def invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        :param args: an empty dictionary (not used).
        :param sly_data: a dictionary with the following optional key:
            - current_date: "YYYY-MM-DD" date override, slots start on the next business day
        :return: a dictionary with the list of open slots formatted as "YYYY-MM-DD HH:MM".
        """
        day: datetime.date = SessionClock.today(sly_data)
        open_slots: list[str] = []
        business_day_index: int = 0
        while business_day_index < self.BUSINESS_DAYS_AHEAD and len(open_slots) < self.MAX_SLOTS:
            day += datetime.timedelta(days=1)
            if day.weekday() >= self.SATURDAY:
                continue
            for slot_index, slot_time in enumerate(self.SLOT_TIMES):
                # Every third slot is simulated as already booked.
                if (business_day_index + slot_index) % 3 != 0:
                    open_slots.append(f"{day.isoformat()} {slot_time}")
            business_day_index += 1
        logger.info("Returning %d open service slots", len(open_slots[: self.MAX_SLOTS]))
        return {"open_slots": open_slots[: self.MAX_SLOTS]}

    async def async_invoke(self, args: dict[str, Any], sly_data: dict[str, Any]) -> dict[str, Any]:
        """
        Delegates to the synchronous invoke method because it's a quick computation.
        """
        return self.invoke(args, sly_data)
