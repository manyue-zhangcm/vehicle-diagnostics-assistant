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

logger = logging.getLogger(__name__)


class SessionClock:  # pylint: disable=too-few-public-methods
    """
    Provides the current date, which can be overridden with an ISO date in sly_data["current_date"]
    so demos and tests are reproducible.
    """

    @staticmethod
    def today(sly_data: dict[str, Any]) -> datetime.date:
        """
        :param sly_data: the private session data, optionally holding "current_date" as "YYYY-MM-DD".
        :return: the overridden date if present and valid, otherwise today's date.
        """
        override: str | None = sly_data.get("current_date")
        if override:
            try:
                return datetime.date.fromisoformat(override)
            except ValueError as error:
                logger.warning("Ignoring invalid current_date override: %s", error)
        return datetime.date.today()
