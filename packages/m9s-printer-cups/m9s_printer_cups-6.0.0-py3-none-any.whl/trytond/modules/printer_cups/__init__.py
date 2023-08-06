# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import printer

__all__ = ['register']


def register():
    Pool.register(
        printer.Cron,
        printer.Printer,
        printer.PrinterRule,
        printer.PrinterState,
        printer.RuleState,
        module='printer_cups', type_='model')
