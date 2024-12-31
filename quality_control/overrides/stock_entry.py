import frappe
from frappe.utils import flt
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry

class CustomStockEntry(StockEntry):

    def before_save(self):
        if self.stock_entry_type == "Material Transfer" and self.custom_control_quality == 0:
            for i in self.items:
                query = """
                            SELECT DISTINCT sle.quality_status
                            FROM `tabStock Ledger Entry` sle
                            INNER JOIN `tabSerial and Batch Bundle` sbb ON sbb.name = sle.serial_and_batch_bundle
                            INNER JOIN `tabSerial and Batch Entry` sbe ON sbe.parent = sbb.name
                            WHERE sle.warehouse = %(warehouse)s AND sbe.batch_no = %(batch_no)s AND sle.quality_status = %(quality_status)s
                        """

                results = frappe.db.sql(query, { "warehouse": i.s_warehouse, "batch_no": i.batch_no, "quality_status": i.quality_status }, as_dict=True)

                if  len(results) > 0:
                    i.to_quality_status = results[0].quality_status
                else:
                    frappe.throw("There is no stock of Status " + i.quality_status + " for item " + i.item_code)




