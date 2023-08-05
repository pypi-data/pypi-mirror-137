# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from trytond import backend
from trytond.model import ModelSQL, fields
from trytond.modules.company.model import CompanyValueMixin
from trytond.modules.product.ir import price_decimal
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.tools.multivalue import migrate_property
from trytond.transaction import Transaction

STATES = {
    'readonly': ~Eval('active', True),
}
DEPENDS = ['active']

price_digits = (16, price_decimal)


class Template(metaclass=PoolMeta):
    __name__ = "product.template"

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.list_price = fields.Function(fields.Numeric("List Price"),
            'get_list_price', setter='set_list_price')
        cls.list_price.states['invisible'] = True
        cls.cost_price.states['invisible'] = True

    def get_list_price(self, name):
        if len(self.products) == 1:
            product, = self.products
            return product.list_price

    @classmethod
    def set_list_price(cls, products, name, value):
        # Prevent NotImplementedError for list_price
        pass

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'list_price':
            return pool.get('product.variant.list_price')
        return super().multivalue_model(field)


class Product(metaclass=PoolMeta):
    __name__ = "product.product"

    # s. setup: name and list_price must be defined at the end of setup
    list_prices = fields.One2Many(
        'product.variant.list_price', 'product', "List Prices")
    variant_name = fields.Char('Variant Name', translate=True,
        select=True, states={
                        'readonly': ~Eval('active', True),
                        }, depends=['active'])

    def __getattr__(self, name):
        result = super().__getattr__(name)
        if not result and name == 'name':
            return getattr(self, 'variant_name')
        return result

    @classmethod
    def __setup__(cls):
        if not hasattr(cls, '_no_template_field'):
            cls._no_template_field = set()
        cls._no_template_field.update(['list_price', 'name'])
        super().__setup__()
        # Due to a bug in setup the above mechanism doesn't work:
        # setup is run first for module product without respecting the MRO, the
        # correct MRO is used in a second run. Thus _no_template_field is
        # updated too late and 'list_price' and 'name' are already instanciated
        # as TemplateFunction. So we need to override them at the very end of
        # setup explicitely.
        cls.list_price = fields.MultiValue(fields.Numeric(
            "List Price", digits=price_digits,
            states={
                'readonly': ~Eval('context', {}).get('company'),
                },
            help="The standard price the variant is sold at."))
        cls.name = fields.Function(fields.Char('Name'),
            getter='on_change_with_name', setter='set_variant_name',
            searcher='search_rec_name')

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'list_price':
            return pool.get('product.variant.list_price')
        return super().multivalue_model(field)

    @classmethod
    def default_list_price(cls, **pattern):
        context = Transaction().context
        if pattern.get('company', context.get('company')):
            return Decimal(0)

    @property
    def list_price_used(self):
        transaction = Transaction()
        with transaction.reset_context(), \
                transaction.set_context(self._context):
            return self.get_multivalue('list_price')

    @fields.depends('variant_name')
    def on_change_with_name(self, name=None):
        '''
        Return the variant_name instead of template name
        '''
        return self.variant_name

    @classmethod
    def set_variant_name(cls, products, name, value):
        if not value:
            return
        cls.write(products, {
                'variant_name': value,
                })

    def get_rec_name(self, name=None):
        '''
        Return the variant_name` if it is set, else return
        the template name.
        '''
        rec_name = self.variant_name or self.template.name
        if self.code:
            rec_name = '[%s] %s' % (self.code, rec_name)
        return rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        domain = super().search_rec_name(name, clause)
        domain.append(('variant_name', ) + tuple(clause[1:]))
        return domain

    @classmethod
    def set_template(cls, products, name, value):
        '''
        Provide a generic setter for function fields when using
        template fields on products. (In analogy to get_template,
        search_template for the use in downstream modules)
        '''
        Template = Pool().get('product.template')
        Template.write([p.template for p in products], {
                name: value,
                })


class VariantListPrice(ModelSQL, CompanyValueMixin):
    "Variant List Price"
    __name__ = 'product.variant.list_price'
    product = fields.Many2One(
        'product.product', "Product", ondelete='CASCADE', select=True,
        context={
            'company': Eval('company', -1),
            },
        depends=['company'])
    list_price = fields.Numeric("List Price", digits=price_digits)

    # 6.2
    #@classmethod
    #def __setup__(cls):
    #    super().__setup__()
    #    cls.company.required = True

    @classmethod
    def __register__(cls, module_name):
        exist = backend.TableHandler.table_exist(cls._table)

        super().__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.append('list_price')
        value_names.append('list_price')
        fields.append('company')
        migrate_property(
            'product.product', field_names, cls, value_names,
            parent='product', fields=fields)


class ProductCostPrice(metaclass=PoolMeta):
    __name__ = 'product.cost_price'

    @classmethod
    def __register__(cls, module_name):
        exist = backend.TableHandler.table_exist(cls._table)

        # Migrate cost price properties of this module before those
        # of module product (#4221).
        if not exist:
            cls._migrate_property([], [], [])
        super().__register__(module_name)

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.append('cost_price')
        value_names.append('cost_price')
        fields.append('company')
        migrate_property(
            'product.product', field_names, cls, value_names,
            parent='product', fields=fields)
