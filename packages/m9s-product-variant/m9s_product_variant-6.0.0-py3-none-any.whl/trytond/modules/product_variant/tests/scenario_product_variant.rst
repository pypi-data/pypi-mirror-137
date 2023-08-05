========================
Product Variant Scenario
========================

Imports::

    >>> from decimal import Decimal
    >>> from proteus import Model
    >>> from trytond.tests.tools import activate_modules

Activate modules::

    >>> config = activate_modules('product_variant')

Create a template::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> template = ProductTemplate()
    >>> template.name = "Product"
    >>> template.default_uom = unit
    >>> template.list_price = Decimal('42.0000')
    >>> template.code = "PROD"
    >>> template.save()
    >>> len(template.products)
    1
    >>> product, = template.products
    >>> product.code
    'PROD'
    >>> product.suffix_code = "001"
    >>> product.save()
    >>> product.code
    'PROD001'

Create some variants::

    >>> Product = Model.get('product.product')
    >>> product = Product()
    >>> product.template = template
    >>> product.name
    >>> product.name = 'Variant 2'
    >>> product.list_price = Decimal('66.0000')
    >>> product.suffix_code = "002"
    >>> product.save()
    >>> product.name
    'Variant 2'
    >>> product.rec_name
    '[PROD002] Variant 2'
    >>> product.list_price
    Decimal('66.0000')
    >>> product.code
    'PROD002'
    >>> product = Product()
    >>> product.template = template
    >>> product.name = 'Variant 3'
    >>> product.list_price = Decimal('88.0000')
    >>> product.suffix_code = "003"
    >>> product.save()
    >>> product.name
    'Variant 3'
    >>> product.rec_name
    '[PROD003] Variant 3'
    >>> product.list_price
    Decimal('88.0000')
    >>> product.code
    'PROD003'

Change template code::

    >>> template.code = "PRD"
    >>> template.save()
    >>> sorted([p.code for p in template.products])
    ['PRD001', 'PRD002', 'PRD003']
