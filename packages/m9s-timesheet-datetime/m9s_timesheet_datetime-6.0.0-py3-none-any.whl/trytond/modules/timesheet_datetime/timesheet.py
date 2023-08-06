# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


class Line(metaclass=PoolMeta):
    __name__ = 'timesheet.line'

    start_time = fields.DateTime('Start Date', format='%H:%M',
            depends=['date', 'end_time'])
    end_time = fields.DateTime('End Date', format='%H:%M',
            depends=['date', 'end_time'])

    @classmethod
    def __setup__(cls):
        super().__setup__()
        # timesheet:  [('date', 'DESC'), ('id', 'ASC')]
        # we want descending by start_time or id
        #  [('date', 'DESC'), ('start_time', 'DESC'), ('id', 'DESC')]
        #  does is the best for now.
        #  TODO via SQL-clause (didn't work for now):
        #  sort by start_date or create_date
        id_asc = ('id', 'ASC')
        if id_asc in cls._order:
            cls._order.remove(id_asc)
        cls._order.append(('start_time', 'DESC'))
        cls._order.append(('id', 'DESC'))
        cls.duration.on_change_with |= set(('start_time', 'end_time'))
        cls.date.on_change_with.add('start_time')

    @staticmethod
    def default_start_time():
        now = datetime.datetime.now()
        return now.replace(second=0, microsecond=0)

    @staticmethod
    def default_end_time():
        now = datetime.datetime.now()
        return now.replace(second=0, microsecond=0)

    @fields.depends('duration', 'start_time', 'end_time')
    def on_change_with_duration(self, name=None):
        if self.start_time and self.end_time:
            td = self.end_time - self.start_time
            # format as minutes without seconds
            minutes = round(td.total_seconds() / 60)
            return datetime.timedelta(minutes=minutes)
        else:
            return self.duration

    @fields.depends('start_time')
    def on_change_with_date(self, name=None):
        Date = Pool().get('ir.date')
        if self.start_time:
            return self.start_time.date()
        return Transaction().context.get('date') or Date.today()

    @fields.depends('start_time', 'duration')
    def on_change_duration(self):
        if self.start_time and self.duration:
            self.end_time = self.start_time + self.duration

    @fields.depends('start_time', 'end_time')
    def on_change_start_time(self):
        if (self.start_time and self.end_time
                and self.end_time < self.start_time):
            self.end_time = self.start_time
