"""
Athena Mission Brief Builder

This class is responsible for orchestrating Athena.
As Athena grows, new engines are added here instead of making report.py larger.
"""


class MissionBriefBuilder:
    def __init__(self, core):
        self.core = core

    def build(self, market):
        """
        Temporary placeholder.

        During the refactor we'll move all of report.py into this
        class one section at a time while keeping Athena runnable.
        """
        raise NotImplementedError(
            "MissionBriefBuilder.build() has not been implemented yet."
        )