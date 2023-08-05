# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Equal, Eval
from trytond.transaction import Transaction


class Party(metaclass=PoolMeta):
    __name__ = "party.party"

    _states = {
        "readonly": (~Eval('active', False)
            | ~Equal(Eval('party_type'), 'person')),
        "invisible": ~Equal(Eval('party_type'), 'person'),
        }
    _depends = ['active', 'party_type']

    party_type = fields.Selection([
            ("organization", "Organization"),
            ("person", "Person"),
            ], "Type",
        states={
            'readonly': ~Eval('active'),
            }, depends=['active'])
    first_name = fields.Char(
        "First Name", states=_states, depends=_depends)

    del _states
    del _depends

    @staticmethod
    def default_party_type():
        return Transaction().context.get('party_type', 'person')

    def get_rec_name(self, name):
        rec_name = super().get_rec_name(name)
        if self.party_type == 'person':
            rec_name = " ".join(filter(None, [
                        self.first_name,
                        rec_name,
                        ]))
        return rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        parties = cls.search(['OR',
                ('name',) + tuple(clause[1:]),
                ('first_name',) + tuple(clause[1:]),
                ])
        if parties:
            return [('id', 'in', [x.id for x in parties])]
        return super().search_rec_name(name, clause)

    def get_full_name(self, name):
        full_name = super().get_full_name(name)
        return " ".join(filter(None, [
                        self.first_name,
                        full_name,
                        ]))

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        for parties, values in zip(actions, actions):
            if ('party_type' in values
                    and values['party_type'] == 'organization'):
                values['first_name'] = None
            args.extend((parties, values))
        super().write(*args)


class PartyErase(metaclass=PoolMeta):
    __name__ = 'party.erase'

    def to_erase(self, party_id):
        pool = Pool()
        Party = pool.get('party.party')

        to_erase = super().to_erase(party_id)
        to_erase += [
            (Party, [('id', '=', party_id)], True,
                ['first_name', 'party_type'],
                [None, None]),
            ]
        return to_erase
