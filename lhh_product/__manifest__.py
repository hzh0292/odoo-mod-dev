{
    'name': "联兴行产品信息查询",

    'summary': """
        联兴行产品信息查询""",

    'description': """
        联兴行产品信息查询
    """,

    'author': "Jeanphy Huang",
    'website': "https://jeanphy.online",


    'category': 'Uncategorized',
    'version': '13.0.0.1.0',


    'depends': ['base', 'sale_management'],

    'external_dependencies' : {
        'python' : ['zhconv'],
    },

    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
