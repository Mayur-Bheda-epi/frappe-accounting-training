# Copyright (c) 2013, mayur and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns= get_columns()
	data=get_filtered_data(filters)
	return columns, data

def get_filtered_data(filters=None):
	if filters:
		create_filter = []
		if filters.get('account'):
			create_filter += ["account = '{}'".format(filters.get('account'))]
		if filters.get('voucher_type'):
			if filters.get('voucher_type') == 'All':
				pass
			else:
				create_filter += ["voucher_type = '{}'".format(filters.get('voucher_type'))]
		if filters.get('fiscal_year'):
			create_filter += ["fiscal_year = '{}'".format(filters.get('fiscal_year'))]
		if filters.get('transaction_date'):
			create_filter += ["transaction_date = '{}'".format(filters.get('transaction_date'))]
		if filters.get('created_at'):
			print("in if")
			create_filter.append("created_at = '{}'".format(filters.get('created_at')))
		print("create filter", create_filter)
		where_conditions = 'where {}'.format(' and '.join(create_filter))
		print(where_conditions)   
		query = 'select * from `tabGeneral Ledger` {} order by created_at desc;'.format(where_conditions)
		print(query)
		data = frappe.db.sql(query, filters, as_dict=1)
		return data
	query = 'select * from `tabGeneral Ledger` order by created_at desc;'
	data = frappe.db.sql(query, as_dict=1)
	return data

def get_columns():
	return [
		{
		"fieldname": "account",
		"fieldtype": "Data",
		"label": "Account",
		"width": 120
		},
		{
		"fieldname": "credit",
		"fieldtype": "Float",
		"label": "Credit",
		"width": 120
		},
		{
		"fieldname": "debit",
		"fieldtype": "Float",
		"label": "Debit",
		"width": 120
		},
		{
		"fieldname": "balance",
		"fieldtype": "Data",
		"label": "Balance",
		"width": 120
		},
		{
		"fieldname": "voucher_type",
		"fieldtype": "Select",
		"label": "Voucher type",
		"options": "Purchase Invoice\nSales Invoice\nPayment Entry For Supplier\nPayment Entry for Customer",
		"width": 120
		},
		{
		"fieldname": "against_account",
		"fieldtype": "Data",
		"label": "Against Account",
		"width": 120
		},
		{
		"fieldname": "transaction_date",
		"label": "Transaction Date",
		"fieldtype": "Date",
		"width": 120,
		"in_list_view": 1	
		},
		{
		"fieldname": "fiscal_year",
		"fieldtype": "Data",
		"label": "Fiscal Year",
		"options": "Fiscal Year",
		"width": 120
		},
		{
		"fieldname": "created_at",
		"fieldtype": "Date",
		"label": "Created At",
		"width": 120
		}
	]

