# Copyright (c) 2024, Kossivi Dodzi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class QualityControl(Document):
	pass


@frappe.whitelist()
def get_filtered_batches(doctype, txt, searchfield, start, page_len, filters):
	warehouse = filters.get('warehouse')+ "%" if filters.get('warehouse') else "%"
	item = filters.get('item')+ "%" if filters.get('item') else "%"
	reference_name = filters.get('reference_name')+ "%" if filters.get('reference_name') else "%"
	name = txt + "%" if txt else "%"

	# SQL query to fetch filtered batches
	query = """
		SELECT b.name, sbe.batch_no,
			b.reference_name, 
			sle.serial_and_batch_bundle, 
			b.batch_qty,
			b.item
		FROM `tabStock Ledger Entry` sle
		INNER JOIN `tabSerial and Batch Bundle` sbb ON sbb.name = sle.serial_and_batch_bundle
		INNER JOIN `tabSerial and Batch Entry` sbe ON sbe.parent = sbb.name
		INNER JOIN tabBatch b ON b.name = sbe.batch_no
		LEFT JOIN (SELECT * FROM `tabQuality Control` WHERE docstatus <> 2) qc ON qc.batch_no = b.name
		WHERE sle.quality_status = 'Q' AND qc.name IS NULL	AND sle.warehouse LIKE %(warehouse)s AND b.reference_name LIKE %(reference_name)s
		AND b.name LIKE %(name)s AND b.item LIKE %(item)s
		GROUP BY sbe.batch_no
		ORDER BY sle.creation DESC
	"""

	results = frappe.db.sql(query, { "warehouse": warehouse, "reference_name": reference_name, "name": name, "item": item }, as_dict=True)
	return results

@frappe.whitelist()
def get_batch_details(name):
	query = """
		SELECT *
		FROM tabBatch
		WHERE name LIKE %(name)s 
	"""

	results = frappe.db.sql(query, { "name": name }, as_dict=True)
	return results