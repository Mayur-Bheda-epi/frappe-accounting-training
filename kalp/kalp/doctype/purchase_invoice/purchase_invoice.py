# -*- coding: utf-8 -*-
# Copyright (c) 2021, mayur and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import random
import uuid
from datetime import datetime, date


class PurchaseInvoice(Document):
	def on_submit(self):
		invdate = datetime.strptime(self.invoice_date,'%Y-%m-%d')
		
		""" Entering value for payment entry for supplier """
		payment_entry_for_supplier = frappe.new_doc('Payment Entry')
		payment_entry_for_supplier.name1 = self.purchaser_name
		payment_entry_for_supplier.paid_from_account = self.assets_account
		payment_entry_for_supplier.paid_to_account = self.purchaser_name
		
		payment_entry_for_supplier.payment_date = self.invoice_date
		payment_entry_for_supplier.amount = self.grand_total
		payment_entry_for_supplier.invoice_number = self.invoice_number
		payment_entry_for_supplier.transaction_Id = str(uuid.uuid1())
		payment_entry_for_supplier.payment_type = "Supplier"
		payment_entry_for_supplier.save()
		payment_entry_for_supplier.submit()

		""" Entering values in the Journal for supplier"""

		journal_entry = frappe.new_doc('journal_entry')
		account_entry = {
			'account': self.assets_account,
			'party': self.purchaser_name,
			'party_type': "Supplier",
			"debit": self.grand_total,
			"credit": 0.00
		}

		journal_entry.append('entries', account_entry)
		journal_entry.total_debit = self.grand_total
		journal_entry.total_credit = 0.00
		journal_entry.entry_id = str(uuid.uuid1())
		journal_entry.save()
		journal_entry.submit()
	
		""" Saving data/ entry for purchase in general ledger"""
		general_ledger = frappe.new_doc('General Ledger')
		general_ledger.transaction_date = self.invoice_date
		general_ledger.account = self.debit_from
		general_ledger.against_account = self.account_details
		general_ledger.voucher_type = "Purchase Invoice"
		general_ledger.debit = self.grand_total
		general_ledger.credit = 0.00
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
			totalqty = int(each_item.get('qty')) + int(totalqty)		
			product_update.opening_stock = str(totalqty)
			product_update.cost = each_item.get('cost_price')
			product_update.mrp = str(each_item.get('mrp'))

			product_update.save()
		
		
# White listing of functions/methods for fetching total qty and sending back to frontend 
@frappe.whitelist()
def get_total_qty(order_number):
	purchase_qty = frappe.get_all('Purchase_Product',filters={'parent':order_number},fields=["product", "qty", "mrp", "cost_price"])
	totalqty=0
	for each_item in purchase_qty:
		totalqty = int(each_item.get('qty')) + totalqty		
	totalcost=0
	for each_item in purchase_qty:
		totalcost = (int(each_item.get('cost_price'))* int(each_item.get('qty'))) + totalcost		
	return totalqty, totalcost
