from odoo import models, fields, api
from zhconv import convert


class WalrusProduct(models.Model):
    _name = 'lhh.product'
    _description = '联兴行产品信息'

    name = fields.Char('型号', help='No_')
    chn_desc1 = fields.Char('中文名1', help='Chinese Description 1')
    chn_desc2 = fields.Char('中文名2', help='Chinese Description 2')
    s_eng_desc1 = fields.Char('短英文名1', help='Short English Description 1')
    eng_desc2 = fields.Char('英文名2', help='English Description 2')
    uom = fields.Char('计量单位', help='Unit of Measure')
    color = fields.Char('颜色', help='Color')
    size = fields.Char('尺寸', help='Size')
    series = fields.Char('系列', help='Series')
    brand = fields.Char('品牌', help='Brand')
    cat_l1 = fields.Char('一级类别', help='Category Level 1')
    cat_l2 = fields.Char('二级类别', help='Category Level 2')
    cat_l3 = fields.Char('三级类别', help='Category Level 3')
    cat_l4 = fields.Char('四级类别', help='Category Level 4')
    a1 = fields.Char()
    a2 = fields.Char()
    a3 = fields.Char()
    a4 = fields.Char()
    a5 = fields.Char()
    remarks = fields.Char('备注', help='Remarks')
    pic_link = fields.Char('图片链接', help='Picture Link')
    active = fields.Boolean(default=True)
    chn_desc0 = fields.Char('简体中文名', compute='_compute_chn_desc', store=True)

    @api.depends('chn_desc2')
    def _compute_chn_desc(self):
        for rec in self:
            if rec.chn_desc2:
                rec.chn_desc0 = convert(rec.chn_desc2, 'zh-cn')
            else:
                rec.chn_desc0 = ''
