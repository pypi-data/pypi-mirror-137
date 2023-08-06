# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.timesheet_datetime.tests.test_timesheet_datetime import (
        suite)
except ImportError:
    from .test_timesheet_datetime import suite

__all__ = ['suite']
