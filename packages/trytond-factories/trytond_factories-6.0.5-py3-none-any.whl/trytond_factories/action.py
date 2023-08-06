
__all__ = [
    'Action',
    'Keyword',
    'Report',
]

import factory
import factory_trytond


class Action(factory_trytond.TrytonFactory):
    class Meta:
        model = 'ir.action'

    name = factory.Faker('word')
    type = factory.Faker('word', ext_word_list=['tree', 'form'])
    records = 'selected'
    usage = factory.Faker('word')
    keywords = factory.RelatedFactoryList(
        'trytond_factories.action.Keyword',
        factory_related_name='action',
        size=1,
    )
    icon = factory_trytond.LazySearch(
        'ir.ui.icon',
        lambda stub: [('module', '=', 'ir')],
    )


class Keyword(factory_trytond.TrytonFactory):
    class Meta:
        model = 'ir.action.keyword'

    keyword = factory.Faker(
        'word',
        ext_word_list=[
            'tree_open',
            'form_print',
            'form_action',
            'form_relate',
            'graph_open',
        ]
    )
    action = factory.SubFactory('trytond_factories.action.Action')


class Report(factory_trytond.TrytonFactory):
    class Meta:
        model = 'ir.action.report'

    action = factory.SubFactory('trytond_factories.action.Action')
    report_name = factory.Faker('word')
    direct_print = True
    single = True
    translatable = True
    template_extension = factory.Faker(
        'word',
        ext_word_list=[
            'odt', 'odp', 'ods', 'odg', 'txt', 'xml', 'html', 'xhtml'
        ]
    )
    extension = factory.Faker(
        'word',
        ext_word_list=[
            '', 'bib', 'bmp', 'csv', 'dbf', 'dif', 'doc', 'doc6', 'doc95',
            'docbook', 'docx', 'docx7', 'emf', 'eps', 'gif', 'html', 'jpg',
            'met', 'ooxml', 'pbm', 'pct', 'pdb', 'pdf', 'pgm', 'png', 'ppm',
            'ppt', 'psw', 'pwp', 'pxl', 'ras', 'rtf', 'latex', 'sda', 'sdc',
            'sdc4', 'sdc3', 'sdd', 'sdd3', 'sdd4', 'sdw', 'sdw4', 'sdw3',
            'slk', 'svg', 'svm', 'swf', 'sxc', 'sxi', 'sxd', 'sxd3', 'sxd5',
            'sxw', 'text', 'tiff', 'txt', 'wmf', 'xhtml', 'xls', 'xls5',
            'xls95', 'xlsx', 'xpm',
        ],
    )
