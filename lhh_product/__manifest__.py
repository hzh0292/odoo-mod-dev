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
<<<<<<< HEAD
    'version': '12.0.0.1.0',

    'depends': ['base', 'sale_management'],

    'external_dependencies': {
        'python': ['zhconv'],
=======
    'version': '1.0',


    'depends': ['base', 'sale_management'],

    'external_dependencies' : {
        'python' : ['zhconv'],
>>>>>>> master
    },

    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
