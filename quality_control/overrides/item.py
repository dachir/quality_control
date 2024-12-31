import frappe
from erpnext.stock.doctype.item.item import Item

class CustomItem(Item):
    pass

@frappe.whitelist()
def get_item_default_quality_status(item):
    liste = frappe.db.sql(
        """
        SELECT name, 
        CASE WHEN custom_control_quality = 0 THEN 'A' ELSE 'Q' END status
        FROM tabItem
        WHERE name = %s
        """,(item), as_dict=1
    )

    return liste[0].status