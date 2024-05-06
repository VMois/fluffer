from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Example_GG02(BaseRule):
    """Columns must be in CamelCase."""

    groups = ("all",)
    crawl_behaviour = SegmentSeekerCrawler({"column_reference"})
    is_fix_compatible = False

    def __init__(self, *args, **kwargs):
        """Overwrite __init__ to set config."""
        super().__init__(*args, **kwargs)

    @staticmethod
    def _is_camel_case(column: str) -> bool:
        first_letter_capital = column[0] == column[0].upper()
        all_letters_not_capital = column != column.upper()
        underscore_is_not_first = column[0] != "_"
        return (
            first_letter_capital and all_letters_not_capital and underscore_is_not_first
        )

    def _eval(self, context: RuleContext):
        for seg in context.segment.segments:
            col_name = seg.raw
            if not self._is_camel_case(col_name):
                return LintResult(
                    anchor=seg,
                    description=f"{col_name} is not in CamelCase.",
                )
