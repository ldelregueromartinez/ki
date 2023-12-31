# Copyright (c) 2018,2023 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPL 2.0: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

from pylint import checkers
from pylint.checkers import utils


class BulkCreateChecker(checkers.BaseChecker):
    name = "bulk-create-checker"

    msgs = {
        "E4451": (
            "Use bulk_create_with_history() instead of bulk_create()",
            "bulk-create-used",
            "bulk_create() will not save model history. "
            "Use bulk_create_with_history() instead!",
        )
    }

    @utils.only_required_for_messages("bulk-create-used")
    def visit_attribute(self, node):
        if node.attrname == "bulk_create":
            self.add_message("bulk-create-used", node=node)
