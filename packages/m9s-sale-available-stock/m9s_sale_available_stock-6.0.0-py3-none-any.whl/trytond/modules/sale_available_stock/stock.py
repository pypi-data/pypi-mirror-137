# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction


class Move(metaclass=PoolMeta):
    __name__ = "stock.move"

    available_qty = fields.Function(
        fields.Float(
            'Available Quantity', digits=(16, Eval('unit_digits', 2)),
            depends=['unit_digits']
        ), 'on_change_with_available_qty'
    )

    @fields.depends('product', 'planned_date', 'from_location')
    def on_change_with_available_qty(self, name=None):
        """
        Returns the available quantity
        """
        pool = Pool()
        Date = pool.get('ir.date')
        Product = pool.get('product.product')

        if not (self.product and self.from_location):
            return

        location = self.from_location
        if location.type != 'storage':
            return

        date = self.planned_date or Date.today()
        date = max(date, Date.today())
        with Transaction().set_context(
                locations=[location.id],
                stock_date_end=date,
                stock_assign=True):
            product = Product(self.product.id)
            return product.quantity
