# # import frappe
# # from frappe.utils import money_in_words
# # from urllib.parse import quote


# # @frappe.whitelist()
# # def get_whatsapp_link(docname, template_name):
# #     template = frappe.get_doc("WhatsApp Template", template_name)
# #     doctype = template.for_doctype

# #     doc = frappe.get_doc(doctype, docname)

# #     phone = ""
# #     if hasattr(doc, "customer") and doc.customer:
# #         phone = frappe.db.get_value("Customer", doc.customer, "nomor_whatsapp") or ""

# #     if not phone:
# #         phone = getattr(doc, "contact_mobile", "")

# #     if not phone:
# #         frappe.throw("Nomor WhatsApp tidak ditemukan.")

# #     phone = normalize_whatsapp_number(phone)
# #     rendered = render_whatsapp_message(template, doc)

# #     return f"https://wa.me/{phone}?text={rendered}"


# # def normalize_whatsapp_number(number):
# #     number = number.strip().replace(" ", "").replace("-", "")

# #     if number.startswith("0"):
# #         return "62" + number[1:]
# #     elif number.startswith("+"):
# #         return number[1:]
# #     return number


# # def render_whatsapp_message(template, doc):
# #     context = {
# #         "doc": doc,
# #         "customer_name": getattr(doc, "customer_name", ""),
# #         "total": getattr(doc, "grand_total", 0),
# #         "items": getattr(doc, "items", []),
# #         "money_in_words": money_in_words
# #     }

# #     rendered = frappe.render_template(template.message_body, context)
# #     return quote(rendered)

# import frappe
# from frappe.utils import money_in_words
# from urllib.parse import quote
# from frappe.utils import money_in_words, fmt_money

# @frappe.whitelist()
# def get_whatsapp_link(docname, template_name):
#     template = frappe.get_doc("WhatsApp Template", template_name)
#     doctype = template.for_doctype

#     doc = frappe.get_doc(doctype, docname)

#     phone = ""

#     # Coba ambil nomor dari Customer jika ada
#     if hasattr(doc, "customer") and doc.customer:
#         phone = frappe.db.get_value("Customer", doc.customer, "nomor_whatsapp") or ""

#     # Kalau tidak ada, coba dari field contact_mobile (misalnya di Lead atau Contact)
#     if not phone:
#         phone = getattr(doc, "contact_mobile", "")

#     if not phone:
#         frappe.throw("Nomor WhatsApp tidak ditemukan.")

#     phone = normalize_whatsapp_number(phone)
#     rendered = render_whatsapp_message(template, doc)

#     return f"https://wa.me/{phone}?text={rendered}"


# def normalize_whatsapp_number(number):
#     """Ubah nomor ke format internasional tanpa tanda plus"""
#     number = number.strip().replace(" ", "").replace("-", "")

#     if number.startswith("0"):
#         return "62" + number[1:]
#     elif number.startswith("+"):
#         return number[1:]
#     return number



# def render_whatsapp_message(template, doc):
#     context = {
#         "doc": doc,
#         "customer_name": getattr(doc, "customer_name", ""),
#         "total": float(getattr(doc, "grand_total", 0)),  # <- pastikan float
#         "items": getattr(doc, "items", []),
#         "money_in_words": money_in_words,
#         "fmt_money": fmt_money
#     }

#     rendered = frappe.render_template(template.message_body, context)
#     return quote(rendered)




import re
from urllib.parse import quote

import frappe
from frappe.utils import money_in_words, fmt_money


@frappe.whitelist()
def get_whatsapp_link(docname, template_name):
    template = frappe.get_doc("WhatsApp Template", template_name)
    doctype = template.for_doctype

    doc = frappe.get_doc(doctype, docname)

    phone = ""

    # Ambil nomor dari Customer jika ada
    if hasattr(doc, "customer") and doc.customer:
        phone = frappe.db.get_value("Customer", doc.customer, "nomor_whatsapp") or ""

    # Kalau tidak ada, coba dari field contact_mobile
    if not phone:
        phone = getattr(doc, "contact_mobile", "")

    if not phone:
        frappe.throw("Nomor WhatsApp tidak ditemukan.")

    phone = normalize_whatsapp_number(phone)
    rendered = render_whatsapp_message(template, doc)

    return f"https://wa.me/{phone}?text={rendered}"


def normalize_whatsapp_number(number):
    """Ubah nomor ke format internasional tanpa tanda plus"""
    number = number.strip().replace(" ", "").replace("-", "")
    if number.startswith("0"):
        return "62" + number[1:]
    elif number.startswith("+"):
        return number[1:]
    return number


def html_to_whatsapp(text):
    """Convert HTML tags to WhatsApp-friendly plain text"""
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'<.*?>', '', text)  # remove all other tags
    return text


def render_whatsapp_message(template, doc):
    context = {
        "doc": doc,
        "customer_name": getattr(doc, "customer_name", ""),
        "total": float(getattr(doc, "grand_total", 0)),
        "items": getattr(doc, "items", []),
        "money_in_words": money_in_words,
        "fmt_money": fmt_money,
    }

    rendered = frappe.render_template(template.message_body, context)
    rendered = html_to_whatsapp(rendered)
    return quote(rendered)
