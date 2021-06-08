# -*- coding: utf-8 -*-
# Copyright (c) 2021, mayur and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import random
import uuid
from datetime import datetime, date

class SalesInvoice(Document):
	def on_submit(self):
		invdate = datetime.strptime(self.invoice_date,'%Y-%m-%d')
		
		""" Entering value for payment entry for supplier """
		payment_entry_for_customer = frappe.new_doc('Payment Entry')
		payment_entry_for_customer.name1 = self.customer_name
		payment_entry_for_customer.paid_from_account = self.assets_account
		payment_entry_for_customer.paid_to_account = self.credit_to
		
		payment_entry_for_customer.payment_date = self.invoice_date
		payment_entry_for_customer.amount = self.grand_total
		payment_entry_for_customer.invoice_number = self.invoice_number
		payment_entry_for_customer.transaction_Id = str(uuid.uuid1())
		payment_entry_for_customer.payment_type = "Customer"
		payment_entry_for_customer.save()
		payment_entry_for_customer.submit()
	
		""" Entering values in the Journal for supplier"""

		journal_entry = frappe.new_doc('journal_entry')
		account_entry = {
			'account': self.customer_name,
			'party': self.assets_account,
			'party_type': "Customer",
			"credit": self.grand_total,
			"debit": 0.00
		}

		journal_entry.append('entries', account_entry)
		journal_entry.total_credit = self.grand_total
		journal_entry.total_debit = 0.00
		journal_entry.entry_id = str(uuid.uuid1())
		journal_entry.save()
		journal_entry.submit()

		""" Saving data/ entry for purchase in general ledger"""
		general_ledger = frappe.new_doc('General Ledger')
		general_ledger.transaction_date = self.invoice_date
		general_ledger.account = self.account_details
		general_ledger.against_account = self.credit_to
		general_ledger.voucher_type = "Sales Invoice"
		general_ledger.credit = self.grand_total
		general_ledger.debit = 0.00
		general_ledger.fiscal_year = str(invdate.year) +"-"+ str(int(invdate.year)+1)
		general_ledger.created_at = self.invoice_date
		general_ledger.save()

		""" Stock Updation in Purchase Product multiple items can be updated """
		purchase_qty = frappe.get_all('Purchase_Product',filters={'parent':self.order_number},fields=["product", "qty", "mrp", "cost_price"])				
		for each_item in purchase_qty:
			product_update = frappe.get_doc('Product', {
				"prod_name": each_item.get('product')
			})
			totalqty = int(product_update.opening_stock)
			totalqty = int(totalqty) - int(each_item.get('qty')) 		
			product_update.opening_stock = str(totalqty)

			product_update.save()

# White listing of functions/methods for fetching total qty and sending back to frontend 
@frappe.whitelist()
def get_total_qty(order_number):
	sales_qty = frappe.get_all('Purchase_Product',filters={'parent':order_number},fields=["product", "qty", "mrp", "cost_price"])
	totalsalesqty=0
	for each_item in sales_qty:
		totalsalesqty = int(each_item.get('qty')) + totalsalesqty		
	totalmrp=0
	for each_item in sales_qty:
		totalmrp = (int(each_item.get('mrp'))* int(each_item.get('qty'))) + totalmrp		
	return totalsalesqty, totalmrp