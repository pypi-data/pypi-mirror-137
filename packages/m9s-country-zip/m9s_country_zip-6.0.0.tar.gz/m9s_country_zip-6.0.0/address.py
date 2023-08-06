# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    @classmethod
    def default_country(cls, **pattern):
        Configuration = Pool().get('party.configuration')
        config = Configuration(1)

        context = Transaction().context
        if pattern.get('company', context.get('company')):
            if config.default_country:
                return config.default_country.id

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'country':
            return pool.get('country.country')
        return super().multivalue_model(field)

    def get_subdivision_country(self):
        PostalCode = Pool().get('country.postal_code')

        if self.postal_code and self.country:
            postal_codes = PostalCode.search([
                        ('postal_code', '=', self.postal_code),
                        ('subdivision.country', '=', self.country.id),
                        ])
            if postal_codes and len(postal_codes) == 1:
                postal_code_, = postal_codes
                self.city = postal_code_.city
                if postal_code_.subdivision:
                    self.subdivision = postal_code_.subdivision
            else:
                self.city = None
                self.subdivision = None

    @fields.depends('postal_code', 'country', 'city', 'subdivision')
    def on_change_postal_code(self):
        return self.get_subdivision_country()

    @fields.depends('postal_code', 'country', 'city', 'subdivision')
    def on_change_country(self):
        return self.get_subdivision_country()

    @fields.depends('postal_code', 'country', 'city')
    def on_change_city(self):
        PostalCode = Pool().get('country.postal_code')

        if self.postal_code and self.country and self.city:
            postal_codes = PostalCode.search([
                        ('postal_code', '=', self.postal_code),
                        ('country', '=', self.country.id),
                        ('city', '=', self.city),
                        ])
            if postal_codes:
                self.subdivision = postal_codes[0].subdivision
