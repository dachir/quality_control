import frappe
from frappe.utils import flt
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry

class CustomStockEntry(StockEntry):
        
    def before_save(self):
        for i in self.items:             
            if self.stock_entry_type == "Material Transfer":
                # Handle custom recontrol case first
                if i.custom_recontrol == 1:
                    i.to_quality_status = "Q"
                    frappe.db.set_value("Stock Entry Detail", i.name, "to_quality_status", "Q")
                elif self.custom_control_quality == 0:
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
                    frappe.db.set_value("Stock Entry Detail", i.name, "to_quality_status", "Q")





    def on_submit(self):
        super().on_submit()
        for i in self.items:
            if i.to_quality_status == "Q":
                qc_doc = frappe.get_doc({
                    "doctype": "Quality Control",
                    "report_date": self.posting_date,
                    "company": self.company,
                    "item_code": i.item_code,
                    "inspection_type": "Incoming",
                    "reference_type": self.doctype,
                    "reference_name": self.name,
                })

                qc_doc.insert()




