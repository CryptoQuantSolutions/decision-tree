# Class that handles order arrays
class OrderArray():
    def __init__(self, id, operation, price_type, order_type, max_delta, min_delta, max_change_above, max_change_below,
                 start_price_offset, price_interval, n_orders, trigger_offset=None, trigger_interval=None):
        self.id = id
        self.operation = operation
        self.price_type = price_type
        self.order_type = order_type
        self.start_price_offset = start_price_offset
        self.price_interval = price_interval
        self.n_orders = n_orders
        self.trigger_offset = trigger_offset
        self.trigger_interval = trigger_interval

        self.deltas = [max_delta, min_delta, max_change_above, max_change_below]

    def adjust_deltas(self):
        logger.info('\'{0}\' comparison, adjusting deltas...'.format(self.id))

        for delta_index in range(len(self.deltas)):
            self.deltas[delta_index] += self.deltas[delta_index]

    def generate_array(self):
        if self.trigger_offset is not None and self.trigger_interval is not None:
            return {'operation': self.operation,
                    'price_type': self.price_type,
                    'order_type': self.order_type,
                    'start_price_offset': self.start_price_offset,
                    'price_interval': self.price_interval,
                    'n_orders': self.n_orders,
                    'trigger_offset':self.tigger_offest,
                    'trigger_interval':self.trigger_interval}
        else:
            return {'operation': self.operation,
                    'price_type': self.price_type,
                    'order_type': self.order_type,
                    'start_price_offset': self.start_price_offset,
                    'price_interval': self.price_interval,
                    'n_orders': self.n_orders}
