#  Copyright (c) 2021 Push Technology Ltd., All Rights Reserved.
#
#  Use is subject to license terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of Push Technology. The intellectual and technical
#  concepts contained herein are proprietary to Push Technology and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import pydantic

from diffusion.internal.utils import Model


class MetricCollector(Model):
    """
    The common base interface for metric collectors.
    """

    name: str = pydantic.Field(default="", min_length=1, serializer="metric-collector-name")

    """
    The name of the metric collector.
    """

    exports_to_prometheus: bool = False
    """
    Indicates whether the metric collector exports to Prometheus.
    """
