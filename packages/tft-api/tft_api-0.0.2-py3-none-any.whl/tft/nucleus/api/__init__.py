# Copyright 2020 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
The package provides the implementation of testing farm API, both public and internal parts.
"""

import pkg_resources
import sentry_sdk
from dynaconf import settings

app_version: str = pkg_resources.get_distribution("tft-api").version
"""
Application version from `pyproject.toml file.
"""

if settings.exists("SENTRY_DSN"):
    sentry_sdk.init(
        settings.SENTRY_DSN, traces_sample_rate=settings.TRACES_SAMPLE_RATE
    )  # noqa pylint: disable=abstract-class-instantiated
