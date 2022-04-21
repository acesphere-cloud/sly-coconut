# -*- coding: utf-8 -*-
import os

from odoo import http
from odoo.http import request


class WhatsAppCheckout(http.Controller):
    @http.route('/shop/whatsapp_checkout', type='http', auth="public", website=True)
    def whatsapp_checkout(self, **kw):
        order = request.website.sale_get_order()
        ui_message = "Quantity \t\t Item\n"
        for line in order.order_line:
            quantity = line.product_uom_qty
            item = line.product_id.display_name
            ui_message += str(quantity) + "\t\t\t" + item + "\n"

        values = {
            'website_sale_order': order,
            'partner': order.partner_id.id,
            'order': order,
            'ui_message': ui_message
        }

        return http.request.render("website_sale_whatsapp_checkout.whatsapp_checkout", values)

    def format_currency_amount(self, amount, currency_id):
        pre = currency_id.position == 'before'
        symbol = u'{symbol}'.format(symbol=currency_id.symbol or '')
        return u'{pre}{0}{post}'.format(amount, pre=symbol if pre else '', post=symbol if not pre else '')

    @http.route('/shop/checkout_whatsapp', type='http', auth="public", website=True)
    def jump_to_whatsapp(self, **kw):
        order = request.website.sale_get_order()
        address_checked = kw.get('address_checked', False)

        method_type = kw.get('method_type', False)
        whats_app_message = ""
        if address_checked:
            whats_app_message += '%0aMode: *Pay on Delivery (Deliver at your address)*'
        else:
            whats_app_message += '%0aMode: *Pick and Pay at Store (Pick order yourself)*'

        whats_app_message += "%0a*Quantity*    *Item*%0a"

        for line in order.order_line:
            quantity = line.product_uom_qty
            item = line.product_id.display_name
            whats_app_message += str(quantity) + "               " + item + "%0a"
        amount_total = self.format_currency_amount(order.amount_total, order.currency_id)
        whats_app_message += "%0a*Total Amount*: " + amount_total
        additional_msg = ""
        if not address_checked:
            additional_msg = kw.get('additional_msg', "")
            order.note = additional_msg
        elif address_checked == 'delivery_address_check':
            additional_msg = order.note

        if additional_msg:
            whats_app_message += "%0a%0a" + additional_msg

        if method_type == 'self_pick':
            for line in order.order_line:
                line.unlink()
            order_ref = request.env['ir.sequence'].sudo().next_by_code('whatsapp.checkout.number')
            whats_app_message = "*_Order Reference:  " + order_ref + '_*%0a' + whats_app_message
            whatsapp_number = request.website.company_id.whatsapp_number
            return request.redirect(
                "https://api.whatsapp.com/send?phone=" + whatsapp_number + "&text=" + whats_app_message)
        elif method_type == 'home_delivery':
            return request.redirect("/shop/checkout?express=1")

        if address_checked == 'delivery_address_check':
            same_shipping = order.partner_shipping_id == order.partner_id or order.only_services
            address = "%0a%0a*Billing Address*:%0a" + os.linesep.join(
                [s + ", " for s in order.partner_id.contact_address.splitlines() if s])
            address = address.strip()[:-1] + "%0a"

            if same_shipping and not order.only_services:
                address = "%0a%0a*Billing and Shipping Address*:%0a" + os.linesep.join(
                    [s + ", " for s in order.partner_id.contact_address.splitlines() if s])
                address = address.strip()[:-1]

            if not same_shipping and not order.only_services:
                address += "%0a%0a*Shipping Address*:%0a" + os.linesep.join(
                    [s + ", " for s in order.partner_shipping_id.contact_address.splitlines() if s])
                address = address.strip()[:-1]

            whats_app_message += address
            for line in order.order_line:
                line.unlink()
            order_ref = request.env['ir.sequence'].sudo().next_by_code('whatsapp.checkout.number')
            whats_app_message = "*_Order Reference:  " + order_ref + '_*%0a' + whats_app_message
            whatsapp_number = request.website.company_id.whatsapp_number
            return request.redirect(
                "https://api.whatsapp.com/send?phone=" + whatsapp_number + "&text=" + whats_app_message)

    @http.route('/all_partners', type='json', auth="user", website=True)
    def test_json_rpc(self):
        partners = request.env['res.partner'].sudo().search([])
        vals = []
        for partner in partners:
            p = {'name': partner.name, 'email': partner.email}
            vals.append(p)

        return {'status': 200, 'response': vals, 'message': 'success'}
