// Copyright (c) 2021, mayur and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
onload: function(frm){
	 frm.set_value('invoice_date',frappe.datetime.now_datetime())
	 frm.refresh_fields()
},	
order_number:function(frm){
	frappe.call({
		method:"kalp.kalp.doctype.purchase_invoice.purchase_invoice.get_total_qty",
		args: {
			order_number:frm.doc.order_number
		}, 
		callback:(res)=>{
			debugger
			console.log(res)
			frm.set_value('total_quantity',res.message[0])
			frm.set_value('grand_total',res.message[1])
			frm.refresh_fields()
		}
	})

}
});
