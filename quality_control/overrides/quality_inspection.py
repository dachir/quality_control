import frappe
from frappe.utils import flt
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection

class CustomQualityInspection(QualityInspection):

    def before_save(self):
        self.custom_control_quality = 1
        if flt(self.custom_process_qty) > flt(self.custom_balance_qty):
            frappe.throw("You cannot control more quantity than expected.")
    
    def on_submit(self):
        status = self.status[0]
        stock_entry_name = self.change_status(status)
        self.custom_stock_entry = stock_entry_name
        balance_qty = flt(self.custom_balance_qty) - flt(self.custom_process_qty)
        self.custom_balance_qty = balance_qty
        frappe.db.set_value('Quality Inspection', self.name, 'custom_stock_entry', stock_entry_name)
        frappe.db.set_value('Quality Control', self.custom_quality_control, 'balance_qty', balance_qty)

        #Status Management
        qc_doc = frappe.get_doc('Quality Control', self.custom_quality_control)
        if qc_doc.batch_qty == qc_doc.balance_qty:
            frappe.db.set_value('Quality Control', self.custom_quality_control, 'status', "Not Started")
        else:
            if qc_doc.balance_qty > 0:
                frappe.db.set_value('Quality Control', self.custom_quality_control, 'status', "Partial")
            elif qc_doc.balance_qty <= 0:
                frappe.db.set_value('Quality Control', self.custom_quality_control, 'status', "Completed")


    def on_cancel(self):
        stock_entry_name = self.change_status("Q")
        balance_qty = flt(self.custom_balance_qty) + flt(self.custom_process_qty)
        self.custom_balance_qty = balance_qty
        frappe.db.set_value('Quality Inspection', self.name, 'custom_stock_entry', stock_entry_name)
        frappe.db.set_value('Quality Control', self.custom_quality_control, 'balance_qty', balance_qty)

    def change_status(self, new_status):
        pr_details = frappe.db.sql(
            """
            SELECT DISTINCT warehouse, cost_center, branch
            FROM `tabPurchase Receipt Item` 
            WHERE parent = %(reference_name)s
            UNION
            SELECT DISTINCT t_warehouse AS warehouse, cost_center, branch
            FROM `tabStock Entry Detail` 
            WHERE parent = %(reference_name)s
            """, {"reference_name": self.reference_name}, as_dict=1
        )
        warehouse = pr_details[0].warehouse
        cost_center = pr_details[0].cost_center
        branch = pr_details[0].branch
        try:
            # Create a new Stock Entry of type "Material Transfer"
            stock_entry = frappe.get_doc({
                "doctype": "Stock Entry",
                "stock_entry_type": "Material Transfer",
                "posting_date": self.report_date,
                "company": self.custom_company,
                "remarks": f"Status change based on Quality Inspection: {self.name}",
                "branch": branch,
                "from_warehouse": warehouse,
                "to_warehouse": warehouse,
                "custom_status_change": 1,
                "items": [{
                    "item_code": self.item_code,
                    "qty": flt(self.custom_process_qty),
                    "uom": self.custom_uom,
                    "stock_uom": self.custom_uom,
                    "conversion_factor": 1,
                    "s_warehouse": warehouse,
                    "t_warehouse": warehouse,
                    "cost_center": cost_center,
                    "branch": branch,
                    "quality_status": "Q",
                    "to_quality_status": new_status,
                }]
            })

            # Insert and submit the Stock Entry
            stock_entry.insert()
            stock_entry.submit()

            return stock_entry.name

            #frappe.msgprint(f"Stock Entry {stock_entry.name} created successfully for Quality Inspection {self.name}")

        except Exception as e:
            frappe.log_error(message=str(e), title="Stock Entry Creation Error")
            frappe.throw(f"An error occurred while creating the Stock Entry: {str(e)}")


    