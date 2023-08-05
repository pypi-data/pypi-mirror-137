===================================
Account Tax Reverse Charge Scenario
===================================

Imports::

    >>> from decimal import Decimal
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax, create_tax_code

Activate modules::

    >>> config = activate_modules('account_tax_reverse_charge')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> receivable = accounts['receivable']
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> account_tax = accounts['tax']
    >>> account_cash = accounts['cash']

Create a tax tree::

    >>> Tax = Model.get('account.tax')
    >>> TaxGroup = Model.get('account.tax.group')
    >>> TaxCode = Model.get('account.tax.code')

    >>> tax_group = TaxGroup(name="Cash", code="CASH")
    >>> tax_group.save()
    
    >>> tax1 = create_tax(Decimal('.10'))
    >>> tax1.group = tax_group
    >>> tax1.reverse_charge = True
    >>> tax1.save()
    
    >>> tax2 = create_tax(Decimal('.10'))
    >>> tax2.group = tax_group
    >>> tax2.reverse_charge = True
    >>> tax2.parent = tax1
    >>> tax2.save()
    
    >>> tax3 = create_tax(Decimal('.10'))
    >>> tax3.group = tax_group
    >>> tax3.reverse_charge = True
    >>> tax3.parent = tax1
    >>> tax3.save()
    
    >>> tax4 = create_tax(Decimal('.10'))
    >>> tax4.group = tax_group
    >>> tax4.reverse_charge = True
    >>> tax4.parent = tax2
    >>> tax4.save()
    
    >>> tax5 = create_tax(Decimal('.10'))
    >>> tax5.group = tax_group
    >>> tax5.reverse_charge = True
    >>> tax5.parent = tax2
    >>> tax5.save()

Check for the validation of same setting in a tree::

    >>> tax5.reverse_charge = False
    >>> tax5.save() # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    trytond.model.modelstorage.ValidationError: All child taxes must have the same setting for reverse charge.
    
    >>> tax6 = create_tax(Decimal('.10'))
    >>> tax6.group = tax_group
    >>> tax6.reverse_charge = False
    >>> tax6.parent = tax3
    >>> tax6.save() # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    trytond.model.modelstorage.ValidationError: All child taxes must have the same setting for reverse charge.
