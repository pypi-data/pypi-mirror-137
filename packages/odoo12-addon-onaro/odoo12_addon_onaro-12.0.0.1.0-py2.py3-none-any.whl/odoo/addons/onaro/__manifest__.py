{
    'name': "Odoo customizations for Onaro",
    'version': '12.0.0.1.0',
    'author': "Coopdevs Treball SCCL",
    'depends': [
        'auth_api_key',
        'base',
        'base_automation',
        'base_rest',
        'crm_lead_product',
        'helpdesk_mgmt',
        'remove_dup_acc_num_constraint',
        'telecom',
    ],
    'external_dependencies': {
        'python': [
            'pycastiphone_client',
        ],
    },

    'description': """
    Odoo Onaro customizations.
    """,
    'website': 'https://coopdevs.org',
    'category': "Cooperative management",
    'license': "AGPL-3",
    'data': [
        'data/base_automation.xml',
        'data/ir_default.xml',
        'data/product_attribute_value.xml',
        'data/product_product.xml',
        'data/product_template_attribute_line.xml',
        'data/product_template.xml',
        'views/crm_lead.xml',
        'security/res_users.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
