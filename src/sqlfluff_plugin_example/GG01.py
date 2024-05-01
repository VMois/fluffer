"""An example of a custom rule implemented through the plugin system.

This uses the rules API supported from 0.4.0 onwards.
"""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Example_GG01(BaseRule):
    """'*' is forbidden in SELECT statements

    **Anti-pattern**

    If new column(s) are added to the table, there is no way to detect it

    .. code-block:: sql

        SELECT * FROM foo

    **Best practice**

    All columns are known and it is clear what is used

    .. code-block:: sql

        SELECT a, b, c FROM foo
    """

    groups = ("all",)
    config_keywords = ["forbidden_columns"]
    crawl_behaviour = SegmentSeekerCrawler({"select_clause"})
    is_fix_compatible = False

    def __init__(self, *args, **kwargs):
        """Overwrite __init__ to set config."""
        super().__init__(*args, **kwargs)
        self.forbidden_columns = [
            col.strip() for col in self.forbidden_columns.split(",")
        ]

    def _eval(self, context: RuleContext):
        """We should not ORDER BY forbidden_columns."""
        for seg in context.segment.segments:
            col_name = seg.raw.lower()
            if col_name == "*":
                return LintResult(
                    anchor=seg,
                    description="'*' is not allowed in SELECT.",
                )
