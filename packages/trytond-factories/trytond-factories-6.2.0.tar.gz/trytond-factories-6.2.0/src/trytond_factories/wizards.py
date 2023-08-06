
__all__ = [
    'create_chart',
]

from trytond.pool import Pool


def create_chart(company, chart_tpl):
    pool = Pool()
    AccountTemplate = pool.get('account.account.template')
    Account = pool.get('account.account')
    CreateChart = pool.get('account.create_chart', type='wizard')

    session_id, _, _ = CreateChart.create()
    create_chart = CreateChart(session_id)

    create_chart.account.account_template = AccountTemplate(chart_tpl.root)
    create_chart.account.company = company

    create_chart.transition_create_account()

    (receivable,) = Account.search([
        ('company', '=', company.id),
        ('template', '=', chart_tpl.receivable),
    ])
    (payable,) = Account.search([
        ('company', '=', company.id),
        ('template', '=', chart_tpl.payable),
    ])
    (revenue,) = Account.search([
        ('company', '=', company.id),
        ('template', '=', chart_tpl.revenue),
    ])
    (expense,) = Account.search([
        ('company', '=', company.id),
        ('template', '=', chart_tpl.expense),
    ])

    create_chart.properties.company = company
    create_chart.properties.account_receivable = receivable
    create_chart.properties.account_payable = payable
    create_chart.properties.category_account_revenue = revenue
    create_chart.properties.category_account_expense = expense

    create_chart.transition_create_properties()
