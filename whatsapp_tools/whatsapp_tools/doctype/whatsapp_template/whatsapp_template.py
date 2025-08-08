# # import frappe
# # import urllib.parse

# # @frappe.whitelist()
# # def get_whatsapp_link(docname, template_name):
# #     template = frappe.get_doc("WhatsApp Template", template_name)
# #     if not template.is_active:
# #         frappe.throw("Template tidak aktif.")

# #     if template.for_doctype != "Sales Invoice":
# #         frappe.throw("Template ini bukan untuk Sales Invoice.")

# #     invoice = frappe.get_doc("Sales Invoice", docname)
# #     customer = frappe.get_doc("Customer", invoice.customer)
    
# #     # Ambil nomor WA
# #     wa_number = customer.nomor_whatsapp
# #     if not wa_number:
# #         frappe.throw("Customer tidak memiliki nomor WhatsApp.")

# #     # Template bisa pakai placeholder seperti {{ customer_name }} dsb.
# #     rendered_message = template.message_body
# #     rendered_message = rendered_message.replace("{{ customer_name }}", customer.customer_name)
# #     rendered_message = rendered_message.replace("{{ invoice_number }}", invoice.name)
# #     rendered_message = rendered_message.replace("{{ total }", f"{invoice.grand_total:,.2f}")

# #     # Encode pesan agar aman di URL
# #     encoded_message = urllib.parse.quote(rendered_message)

# #     # Buat link WhatsApp
# #     wa_link = f"https://wa.me/{wa_number}?text={encoded_message}"
# #     return wa_link





# from frappe.utils import get_url
# from urllib.parse import quote
# from jinja2 import Template

# @frappe.whitelist()
# def get_whatsapp_link(invoice_number, template_name):
#     doc = frappe.get_doc("Sales Invoice", invoice_number)
#     template = frappe.get_doc("WhatsApp Template", template_name)

#     # Render message_body pakai Jinja2
#     rendered = frappe.render_template(template.message_body, {"doc": doc})

#     # Hapus tag HTML kalau ada (opsional, jika kamu mau jaga kebersihan pesan)
#     from bs4 import BeautifulSoup
#     clean_text = BeautifulSoup(rendered, "html.parser").get_text()

#     phone = frappe.db.get_value("Customer", doc.customer, "nomor_whatsapp")

#     if not phone:
#         frappe.throw("Customer belum punya nomor WhatsApp")

#     # Encode URL
#     url = f"https://wa.me/{phone}?text={quote(clean_text)}"
#     return url

# import frappe
from frappe.model.document import Document

class WhatsAppTemplate(Document):
	pass
