#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Season/Episode numbering support
"""
import re
from rebulk import Rebulk, AppendMatchRule

from .common.formatters import cleanup

BONUS = Rebulk().regex_defaults(flags=re.IGNORECASE)

BONUS.regex(r'x(\d+)', name='bonusNumber', private_parent=True, children=True, formatter=int,
            conflict_solver=lambda match: match.name in ['videoCodec', 'episodeNumber'])


class BonusTitleRule(AppendMatchRule):
    """
    Abstract rule to validate audio profiles
    """
    priority = 250

    def when(self, matches, context):
        bonus_number = matches.named('bonusNumber', lambda match: not match.private, index=0)
        if bonus_number:
            hole = matches.holes(bonus_number.end, formatter=cleanup, index=0)
            if hole and hole.value:
                hole.name = 'bonusTitle'
                return hole

BONUS.rules(BonusTitleRule)
