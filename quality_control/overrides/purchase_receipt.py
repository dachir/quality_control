import frappe
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt

class CustomPurchaseReceipt(PurchaseReceipt):
    
    def on_submit(self):
        super().on_submit()  # Call the original method

        # Custom processing after the main post-process actions
        self.create_quality_control_entries()

    def create_quality_control_entries(self):
        for i in self.items:
            # Ensure serial_and_batch_bundle is populated
            if i.quality_status == "Q":
                #batch_data = frappe.db.sql(
                #    """
                #    SELECT batch_no
                #    FROM `tabSerial and Batch Entry`
                #    WHERE parent = %s
                #    """, (i.serial_and_batch_bundle), as_dict=1
                #)

                #if batch_data:
                #    b = batch_data[0]
                qc_doc = frappe.get_doc({
                    "doctype": "Quality Control",
                    "report_date": self.posting_date,
                    "company": self.company,
                    "item_code": i.item_code,
                    #"batch_no": b.batch_no,
                    #"batch_qty": i.qty,
                    #"balance_qty": i.qty,
                    "inspection_type": "Incoming",
                    "reference_type": "Purchase Receipt",
                    "reference_name": self.name,
                })

                # Insert and submit the Quality Control document
                qc_doc.insert()