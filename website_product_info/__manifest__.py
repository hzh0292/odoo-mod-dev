{
    'name': "官网上架产品信息收集",

    'summary': """
        官网上架产品信息收集""",

    'description': """
        官网上架产品信息收集
    """,

    'author': "Jeanphy Huang",
    'website': "https://jeanphy.online",


    'category': 'Uncategorized',
    'version': '0.1',


    'depends': ['base', 'mail', 'sale_management', 'lhh_product'],

    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
    ],
}
