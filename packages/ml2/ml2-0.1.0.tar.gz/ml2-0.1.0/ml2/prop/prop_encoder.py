"""Propositional formula encoder"""

import logging

from ..data.encoder import ExprEncoder, SeqEncoder
from ..data.expr import ExprNotation
from .prop_lexer import lex_prop
from .prop_parser import parse_prefix_prop, parse_infix_prop

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PropSeqEncoder(SeqEncoder):
    @property
    def formula(self):
        return self.sequence

    def lex(self):
        self.tokens = lex_prop(self.formula)
        success = self.tokens is not None
        if not success:
            self.error = "Lex formula"
        return success

    def vocabulary_filename(self):
        return "prop-vocab" + super().vocabulary_filename()


class PropTreeEncoder(ExprEncoder):
    @property
    def formula(self):
        return self.expression

    def lex(self):
        self.tokens = lex_prop(self.formula)
        success = self.tokens is not None
        if not success:
            self.error = "Lex formula"
        return success

    def parse(self):
        if self.notation == ExprNotation.PREFIX:
            self.ast = parse_prefix_prop(self.formula)
        elif self.notation == ExprNotation.INFIX:
            self.ast = parse_infix_prop(self.formula)
        else:
            logger.critical("Unsupported notation %s", self.notation)
        success = self.ast is not None
        if not success:
            self.error = "Parse formula"
        return success

    def vocabulary_filename(self):
        return "prop-vocab" + super().vocabulary_filename()
