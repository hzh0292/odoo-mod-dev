from odoo import models, fields, api


class ProductCertification(models.Model):
    _description = '产品认证'
    _name = 'product.certification'
    _order = 'name'

    name = fields.Char(string='认证名称', required=True, translate=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='颜色',
                           default=lambda self: max(self.env['product.certification'].search([]).mapped('color')) + 1)
    product_ids = fields.Many2many('product.info', column1='certification_id', column2='product_id', string='产品')


class ProductPhoto(models.Model):
    _name = 'product.photo'
    _order = 'sequence'

    sequence = fields.Integer(string="序号", default=10)
    name = fields.Char(string='名称')
    image = fields.Binary(string='图片', attachment=True)
    product_id = fields.Many2one('product.info', string='产品', copy=True)


class WalrusProduct(models.Model):
    _name = 'product.info'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '官网上架产品信息'

    name = fields.Char('型号', track_visibility='onchange')
    desc = fields.Char('名称', track_visibility='onchange')
    color = fields.Char('颜色', track_visibility='onchange')
    size = fields.Char('尺寸', track_visibility='onchange')
    image = fields.Binary('尺寸图')
    photo_ids = fields.One2many('product.photo', 'product_id', string='组图')
    note = fields.Text('产品特点', track_visibility='onchange')
    type = fields.Selection([('a', '普通马桶/连体坐便式'),
                             ('b', '普通马桶/分体坐便式'),
                             ('c', '普通马桶/挂墙坐便式'),
                             ('n', '面盆系列/台上盆'),
                             ('n2', '面盆系列/台下盆'),
                             ('n3', '面盆系列/半嵌盆'),
                             ('n4', '面盆系列/台面盆'),
                             ('n5', '面盆系列/一体柱盆'),
                             ('n6', '面盆系列/挂墙盆'),
                             ('d', '龙头/面盆龙头'),
                             ('o', '龙头/厨盆龙头'),
                             ('p', '龙头/浴缸龙头'),
                             ('e', '智能系列'),
                             ('f', '浴室柜'),
                             ('g', '花洒'),
                             ('h', '淋浴房'),
                             ('i', '浴缸'),
                             ('j', '五金产品/挂件'),
                             ('k', '五金产品/配件'),
                             ('l', '水槽系列'),
                             ('m', '公共系列'),
                             ], string='分类', track_visibility='onchange')
    active = fields.Boolean('有效', default=True)
    certification_id = fields.Many2many('product.certification', column1='product_id', column2='certification_id',
                                        string='认证')
    state = fields.Selection([('draft', '草稿'),
                              ('partial', '部分完善'),
                              ('done', '全部完善'),
                              ('uploaded', '已上传官网'),
                              ('updated', '信息更新'), ], string='状态', default='draft', track_visibility='onchange')
    web_url = fields.Char('官网链接', track_visibility='onchange')
    desc_t = fields.Char('名称', track_visibility='onchange')
    note_t = fields.Text('产品特点', track_visibility='onchange')
    color_t = fields.Char('颜色', track_visibility='onchange')
    url_t = fields.Char('官网链接', compute='_compute_web_url')
    desc_e = fields.Char('名称', track_visibility='onchange')
    note_e = fields.Text('产品特点', track_visibility='onchange')
    color_e = fields.Char('颜色', track_visibility='onchange')
    url_e = fields.Char('官网链接', compute='_compute_web_url')

    lhh_product_count = fields.Integer('联兴行产品', compute='_compute_lhh_product_count')
    edit_url = fields.Char('编辑链接', compute='_compute_edit_url')

    def action_partial(self):
        self.write({'state': 'partial'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_uploaded(self):
        self.write({'state': 'uploaded'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_updated(self):
        self.write({'state': 'updated'})

    @api.depends('name')
    def _compute_lhh_product_count(self):
        self.lhh_product_count = self.env['lhh.product'].search_count([('name', 'like', self.name[:9])])

    def action_view_count_lhh_product(self):
        action = self.env.ref('lhh_product.action_window_lhh_product').read()[0]
        product = self.env['lhh.product'].search([('name', 'like', self.name[:9])])
        if len(product) > 1:
            action['domain'] = [('id', 'in', product.ids)]
        elif product:
            action['views'] = [(self.env.ref('lhh_product.lhh_product_form').id, 'form')]
            action['res_id'] = product.id
        return action

    @api.depends('web_url')
    def _compute_web_url(self):
        if self.web_url:
            if self.web_url[7:13] != 'walrus':
                self.write({'web_url': 'http://walrus.com.cn' + self.web_url[29:]})
            self.url_t = self.web_url[:21] + 'zh/' + self.web_url[21:]
            self.url_e = self.web_url[:21] + 'en/' + self.web_url[21:]
        else:
            self.url_t = self.url_e = ''

    @api.depends('web_url')
    def _compute_edit_url(self):
        if self.web_url:
            cat1 = self.web_url.split('&')[1][4:]
            pid = self.web_url.split('&')[2][4:]
            cat2 = self.web_url.split('&')[3][4:]
            self.edit_url = 'http://walrus.com.cn/hlsadmin/infoproduct_update.php?cid={}&id={}'.format(
                cat2 if cat2 else cat1, pid)
        else:
            self.edit_url = ''
