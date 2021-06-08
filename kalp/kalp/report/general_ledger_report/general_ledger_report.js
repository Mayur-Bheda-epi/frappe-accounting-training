// Copyright (c) 2016, mayur and contributors
// For license information, please see license.txt
/* eslint-disable */
//Filters for adding viewing report
frappe.query_reports["General Ledger Report"] = {
	"filters": [
		{
			"fieldname": "transaction_date",
			"fieldtype": "Date",
			"in_list_view": 1,
			"label": "Transaction Date"
		   },
		   {
			"fieldname": "account",
			"fieldtype": "Link",
			"label": "Account Details",
			"options": "Account"
			},
		   {
			"fieldname": "fiscal_year",
			"fieldtype": "Data",
			"label": "Fiscal Year",
			"options": "Fiscal Year"
		   },
		   {
			"fieldname": "voucher_type",
			"default": "All",
			"fieldtype": "Select",
			"label": "Voucher type",
			"options": "Purchase Invoice\nSales Invoice\nPayment Entry For Supplier\nPayment Entry for Customer"
		   },
		   {
			"fieldname": "created_at",
			"fieldtype": "Date",
			"label": "Created At"
		   }
	]
};
