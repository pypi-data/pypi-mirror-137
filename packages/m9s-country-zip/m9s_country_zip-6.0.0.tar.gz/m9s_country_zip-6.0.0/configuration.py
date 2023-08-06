# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ValueMixin, fields
from trytond.modules.party.configuration import _ConfigurationValue
from trytond.pool import PoolMeta

default_country = fields.Many2One('country.country', 'Default Country')


class Configuration(metaclass=PoolMeta):
    __name__ = 'party.configuration'
    default_country = fields.MultiValue(default_country)


class ConfigurationCountry(_ConfigurationValue, ModelSQL, ValueMixin):
    'Party Configuration Country'
    __name__ = 'party.configuration.default_country'
    default_country = default_country
    _configuration_value_field = 'default_country'
