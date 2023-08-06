#  Copyright (c) 2021 Push Technology Ltd., All Rights Reserved.
#
#  Use is subject to license terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of Push Technology. The intellectual and technical
#  concepts contained herein are proprietary to Push Technology and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import typing

import pydantic

from diffusion.features.control.metrics import MetricCollector
from diffusion.internal.utils import BuilderBase, validate_member_arguments


class TopicMetricCollector(MetricCollector):
    """
    The definition of a topic metric collector.

    These can be configured to record metric data for a subset of all topics,
    specified with a topic selector.
    """

    topic_selector: typing.Optional[pydantic.StrictStr] = None

    groups_by_topic_type: bool = False
    """
    Indicates whether the collector groups by topic type.

    Returns:
        True if grouping by topic type
    """


class TopicMetricCollectorBuilder(BuilderBase[TopicMetricCollector]):
    """
    A topic metric collector builder.

    This creates instances of `TopicMetricCollector` that can be supplied to
    Metrics.put_topic_metric_collector.
    """
    Self = typing.TypeVar('Self', bound=BuilderBase[TopicMetricCollector])

    @validate_member_arguments
    def export_to_prometheus(
            self: Self, export: bool
    ) -> Self:
        """
        Specifies whether the metric collector should export metrics to
        Prometheus or not.

        The default is that metrics are not exported to Prometheus.

        Args:
             export:
                True to export metrics to Prometheus

        Returns:
             this builder
        """
        self._target.exports_to_prometheus = export
        return self

    @validate_member_arguments
    def group_by_topic_type(
            self: Self, group_by_topic_type: bool
    ) -> Self:
        """
        Specifies whether the metric collector should group by topic
        type.

        By default a topic metric collector does not group by topic type.

        Args:
            group_by_topic_type:
                True to indicate that the collector
                should group by topic type

        Returns: this builder
        """
        self._target.groups_by_topic_type = group_by_topic_type
        return self

    def reset(self) -> 'TopicMetricCollectorBuilder':
        """
        Reset the builder.

        Returns:
            this Builder
        """
        return super().reset()

    @validate_member_arguments
    def _create_delegate(
        self, name: pydantic.StrictStr, topic_selector: pydantic.StrictStr
    ) -> TopicMetricCollector:
        return super()._create(name=name, topic_selector=topic_selector)

    def create(
            self, name: str, topic_selector: str
    ) -> TopicMetricCollector:
        """
        Create a new `TopicMetricCollector` using the values
        currently known to this builder.

        Args:
            name:
                the name of the TopicMetricCollector

            topic_selector:
                the selector pattern that specifies the
                topics for which metrics are to be collected

        Returns:
             a new TopicMetricCollector with all of the
             current settings of this builder
        """
        return self._create_delegate(name, topic_selector)
