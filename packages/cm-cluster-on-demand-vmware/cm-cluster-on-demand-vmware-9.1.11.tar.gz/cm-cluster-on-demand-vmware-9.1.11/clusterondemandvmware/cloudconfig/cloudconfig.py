# Copyright 2004-2022 Bright Computing Holding BV
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

import logging
import shlex

from clusterondemand.cloudconfig import SignalHandler

log = logging.getLogger("cluster-on-demand")

ERROR_HANDLER = """\
set -e
function error_handler {
    read line file <<<$(caller)
    echo \"An error occurred in line $line of $file: exit code '$1' while running: '$2'\"
    exit 1
}
trap 'error_handler $? "$BASH_COMMAND"' ERR
"""


class VMwareSignalHandler(SignalHandler):
    def __init__(self, status_log_prefix: str):
        super().__init__(status_log_prefix)

    def get_init_commands(self):
        return [
            ERROR_HANDLER,
        ]

    def get_files(self):
        return []

    def get_config_complete_commands(self):
        commands = self.get_status_log_commands("cloud-init: Complete.")
        return commands

    def get_status_log_commands(self, status: str):
        escaped_status = shlex.quote(f"{self.log_prefix} {status}")
        return [f"echo {escaped_status}"]
