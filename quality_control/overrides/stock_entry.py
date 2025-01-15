import frappe
from frappe.utils import flt
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry

class CustomStockEntry(StockEntry):
        
    def before_save(self):
        empty_quality_rows = []  # List to store rows with missing quality status
        for idx, i in enumerate(self.items, start=1):  # Add `enumerate` to track row index
            if self.stock_entry_type == "Material Transfer":
                # Handle custom recontrol case first
                if i.custom_recontrol == 1:
                    i.to_quality_status = "Q"
                    frappe.db.set_value("Stock Entry Detail", i.name, "to_quality_status", "Q")
                elif self.custom_control_quality == 0 and self.custom_status_change == 0:
                    if not i.quality_status:
                        i.quality_status = "A"
                        frappe.db.set_value("Stock Entry Detail", i.name, "quality_status", "A")
                    i.to_quality_status = i.quality_status
                    frappe.db.set_value("Stock Entry Detail", i.name, "to_quality_status", i.quality_status)

            elif self.stock_entry_type == "Manufacture":
                # Fetch quality control status for the item
                if i.branch == "Kinshasa":
                    quality_control = frappe.db.get_value("Item", i.item_code, "custom_control_quality")
                    if i.t_warehouse and quality_control == 1:
                        i.to_quality_status = "Q"
                        frappe.db.set_value("Stock Entry Detail", i.name, "to_quality_status", "Q")
                else:
                    i.to_quality_status = "A"
                    frappe.db.set_value("Stock Entry Detail", i.name, "to_quality_status", "A")

            elif self.stock_entry_type == "Material Transfer for Manufacture":
                i.quality_status = "A"
                i.to_quality_status = "A"
                frappe.db.set_value("Stock Entry Detail", i.name, "quality_status", "A")
                frappe.db.set_value("Stock Entry Detail", i.name, "to_quality_status", "A")

            elif self.stock_entry_type in ["Material Receipt", "Material Issue"]:
                i.to_quality_status = i.quality_status
                frappe.db.set_value("Stock Entry Detail", i.name, "to_quality_status", i.quality_status)

             # Collect rows with empty quality_status or to_quality_status
            if not (i.quality_status or i.to_quality_status):
                empty_quality_rows.append(idx)

        # Throw error after the loop if there are any issues
        if empty_quality_rows:
            frappe.throw(f"Rows {', '.join(map(str, empty_quality_rows))}: 'quality_status' or 'to_quality_status' cannot be empty.")



    def on_submit(self):
        super().on_submit()
        for i in self.items:
            if i.to_quality_status == "Q":
                serial_and_batch_bundle

                batch_docs = frappe.db.sql(
                    """
                    SELECT sbe.batch_no, sbe.qty, type_of_transaction
                    FROM `tabSerial and Batch Entry` sbe INNER JOIN `tabSerial and Batch Bundle` sbb ON sbb.name = sbe.parent
                    WHERE voucher_no = %s 
                    """, (self.name)
                )
                #AND type_of_transaction = 'Inward'

                if type_of_transaction == "Inward":
                    for b in batch_docs:
                        qc_doc = frappe.get_doc({
                            "doctype": "Quality Control",
                            "report_date": self.posting_date,
                            "company": self.company,
                            "item_code": i.item_code,
                            "inspection_type": b.type_of_transaction,
                            "reference_type": self.doctype,
                            "reference_name": self.name,
                            "batch_no": b.batch_no,
                            "balance_qty": b.qty,
                        })

                        qc_doc.insert()
                #else:
                #    qc_doc = frappe.get_doc("Quality Control", {"batch_no": b.batch_no})



