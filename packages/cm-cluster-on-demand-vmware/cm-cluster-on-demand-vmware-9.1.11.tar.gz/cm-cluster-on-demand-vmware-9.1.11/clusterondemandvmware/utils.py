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

from clusterondemand.imagetable import make_cod_images_table

log = logging.getLogger("cluster-on-demand")


def print_images_table(images, print_func=log.info):
    table = make_cod_images_table(
        images,
        columns=["name", "type", "size", "distro", "bcm_version", "created_at"],
        sortby=["name"],
        advanced=True,
    )

    print(table)
