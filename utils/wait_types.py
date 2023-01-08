__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import enum

class RegexOperator(enum.Enum):
    EXISTS = 0,
    AND = 1,
    OR = 2,
    IN_ORDER_LINE = 3,
    IN_ORDER_REAL_TIMESTAMP = 4,
    IN_ORDER_LOG_TIMESTAMP = 5

class Label:
    def __init__(self, label):
        self.label = label

