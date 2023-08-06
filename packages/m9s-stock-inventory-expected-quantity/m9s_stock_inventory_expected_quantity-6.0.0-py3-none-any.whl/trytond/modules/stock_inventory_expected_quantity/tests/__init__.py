# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.stock_inventory_expected_quantity.tests.test_stock_inventory_expected_quantity import suite
except ImportError:
    from .test_stock_inventory_expected_quantity import suite

__all__ = ['suite']
