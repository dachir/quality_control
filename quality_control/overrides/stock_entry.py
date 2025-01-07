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

                if self.custom_control_quality == 0:
                    query = """
                        SELECT DISTINCT sle.quality_status
                        FROM `tabStock Ledger Entry` sle
                        INNER JOIN `tabSerial and Batch Bundle` sbb ON sbb.name = sle.serial_and_batch_bundle
                        INNER JOIN `tabSerial and Batch Entry` sbe ON sbe.parent = sbb.name
                        WHERE sle.warehouse = %(warehouse)s 
                        AND sbe.batch_no = %(batch_no)s 
                        AND sle.quality_status = %(quality_status)s
                    """
                    params = {
                        "warehouse": i.s_warehouse,
                        "batch_no": i.batch_no,
                        "quality_status": i.quality_status
                    }
                    results = frappe.db.sql(query, params, as_dict=True)

                    if results:
                        i.to_quality_status = results[0].quality_status
                    else:
                        frappe.throw(
                            f"There is no stock status '{i.quality_status}' for item '{i.item_code}'"
                        )

            elif self.stock_entry_type == "Manufacture":
                # Fetch quality control status for the item
                quality_control = frappe.db.get_value("Item", i.item_code, "quality_control")
                if i.t_warehouse and quality_control == 1:
                    i.to_quality_status = "Q"





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
                    "reference_type": "Purchase Receipt",
                    "reference_name": self.name,
                })

                qc_doc.insert()




