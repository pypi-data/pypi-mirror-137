# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.rpc import RPC


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    supply_state = fields.Function(fields.Selection(
            'get_supply_state_selection', 'Supply State',
            states={
                'invisible': ~Eval('supply_state'),
                }), 'get_supply_state')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.__rpc__.update({
            'get_supply_state_selection': RPC(),
        })

    def get_supply_state(self, name):
        supply_state = ''
        for line in self.lines:
            if line.supply_state == 'cancelled':
                continue
            elif line.supply_state == 'requested':
                supply_state = line.supply_state
                break
            else:
                supply_state = line.supply_state
        if supply_state and (
                self.state == 'done' or self.shipment_state == 'sent'):
            supply_state = 'supplied'
        return supply_state

    @classmethod
    def get_supply_state_selection(cls):
        SaleLine = Pool().get('sale.line')
        field_name = 'supply_state'
        selection = SaleLine.fields_get(
            [field_name])[field_name]['selection']
        return selection
