// Copyright (c) 2024, Kossivi Dodzi Amouzou and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quality Control", {
    refresh: function(frm) {
        // Button to open the multiselect dialog
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button('Select Batch', () => {
                open_batch_multiselect_dialog(frm);
            });
        }
    }
});

function open_batch_multiselect_dialog(frm) {
    // Define query arguments for fetching batch data
    let query_args = {
        query: "quality_control.quality_control.doctype.quality_control.quality_control.get_filtered_batches",
        filters: {
            reference_name: frm.doc.reference_name,
            item: frm.doc.item,
        }
    };

    // Create the MultiSelectDialog and store a reference to it
    new frappe.ui.form.MultiSelectDialog({
        doctype: "Batch",
        target: frm,
        setters: {
            //warehouse: frm.doc.warehouse,
            item: null,
            
        },
        add_filters_group: 0,
        columns: ["name", "item", "reference_name", "batch_qty"],
        get_query() {
            // Reset filters to avoid carrying over previous values
            query_args.filters = {
                reference_name: frm.doc.reference_name
            };

            // Get the values from the setters (filters)
            const item = this.dialog.fields_dict.item.get_value();
            //const warehouse = this.dialog.fields_dict.warehouse.get_value();

            // Apply filters based on user input
            if (item) {
                query_args.filters.item = item;
            }
            /*if (warehouse) {
                query_args.filters.warehouse = warehouse;
            }*/

            return query_args;
        },
        action(selections) {
            // Ensure only one option is selected
            if (selections.length > 1) {
                frappe.msgprint({
                    title: __('Validation Error'),
                    indicator: 'red',
                    message: __('You can only select one batch. Please deselect any additional options.')
                });
                return;
            }

            // If exactly one selection is made
            if (selections.length === 1) {
                const selected_batch_no = selections[0];

                // Fetch the details of the selected batch using 'frappe.call'
                frappe.call({
                    method: "quality_control.quality_control.doctype.quality_control.quality_control.get_batch_details",
                    args: {
                        name: selected_batch_no
                    },
                    callback: function(response) {
                        if (response.message) {
                            const selected_data = response.message[0];

                            // Set form fields with the selected batch data
                            frm.set_value('item_code', selected_data.item);
                            frm.set_value('batch_no', selected_data.name);
                            frm.set_value('batch_qty', selected_data.batch_qty);
                            frm.set_value('balance_qty', selected_data.batch_qty);

                            // Close the dialog
                            cur_dialog.hide();

                            // Notify the user
                            /*frappe.show_alert({
                                message: `Selected Batch: ${selected_data.name}`,
                                indicator: 'green'
                            });*/
                        } else {
                            frappe.msgprint({
                                title: __('Error'),
                                indicator: 'red',
                                message: __('Failed to fetch batch details. Please try again.')
                            });
                        }
                    },
                    error: function(error) {
                        frappe.msgprint({
                            title: __('Server Error'),
                            indicator: 'red',
                            message: `Error fetching batch details: ${error}`
                        });
                        console.error("Error:", error);
                    }
                });
            } else {
                frappe.msgprint({
                    title: __('Validation Error'),
                    indicator: 'red',
                    message: __('No batch selected. Please select a batch.')
                });
            }
        }
    });
}
