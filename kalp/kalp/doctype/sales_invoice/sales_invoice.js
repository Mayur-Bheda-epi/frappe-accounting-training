// Copyright (c) 2021, mayur and contributors
// For license information, please see license.txt
// Client Side logic for Purchase Invoice to fetch the values 
frappe.ui.form.on('Sales Invoice', {	
	onload: function(frm){
	 frm.set_value('invoice_date',frappe.datetime.now_datetime())
	 frm.refresh_fields()
},
order_number:function(frm){
	//To fetch the get_total_qty on change of Order Number
	frappe.call({
		method:"kalp.kalp.doctype.sales_invoice.sales_invoice.get_total_qty",
		args: {
			order_number:frm.doc.order_number
		}, 
		callback:(res)=>{
			// Settting the values of the Fields at callback
			frm.set_value('total_quantity',res.message[0])
			frm.set_value('grand_total',res.message[1])
			frm.refresh_fields()
		}
	})

}

});
