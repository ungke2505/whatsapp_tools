frappe.ui.form.on('WhatsApp Template', {
    refresh(frm) {
        if (
            frm.doc.is_active &&
            frm.doc.for_doctype === "Sales Invoice" &&
            frm.doc.invoice_number
        ) {
            frm.add_custom_button('Kirim WhatsApp', () => {
                frappe.call({
                    method: 'whatsapp_tools.api.get_whatsapp_link',
                    args: {
                        docname: frm.doc.invoice_number,
                        template_name: frm.doc.name
                    },
                    callback(r) {
                        if (r.message) {
                            window.open(r.message, '_blank');
                        } else {
                            frappe.msgprint("Link WhatsApp tidak tersedia.");
                        }
                    }
                });
            });
        }
    }
});
