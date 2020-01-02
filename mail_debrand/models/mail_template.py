# Copyright 2019 O4SB - Graeme Gellatly
# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from lxml import html as htmltree
from odoo import _, api, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    @api.model
    def _debrand_body(self, html):
        root = htmltree.fromstring(html)
        powered_by_elements = root.xpath(
            "//table//a[contains(@href, 'www.odoo.com')]"
        )
        for elem in powered_by_elements:
            parent = elem.getparent().getparent()
            if parent is not None:
                parent.drop_tree()

        link_elements = root.xpath(
            "//a[contains(@href, 'www.odoo.com')]"
        )
        for elem in link_elements:
            parent = elem.getparent()
            if parent is not None:
                parent.drop_tree()

        return htmltree.tostring(root).decode("utf-8")

    @api.model
    def render_post_process(self, html):
        html = super().render_post_process(html)
        return self._debrand_body(html)
