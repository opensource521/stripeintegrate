from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.views.generic.detail import DetailView
from billing.models import Transaction, UserCheckOut, ImageSubscription, UserCredit, CreditToCash, FeaturedUser_0, FeaturedUser_1, AnalyticsSubscription, StudentBISubscription
from billing.forms import CreditForm, ImgSubForm, FeatureSubForm, AnaSubForm, StudentBISubForm
from billing.control import feat_days_choices_dict, img_days_choices_dict, ana_days_choices_dict, studentbi_days_dict
from mixins.mixins import GetCheckoutMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
import braintree
import datetime








class AddCredits(LoginRequiredMixin, GetCheckoutMixin, FormView):
	template_name = 'addcredit.html'
	form_class = CreditForm

	def get_context_data(self, *args, **kwargs):
		context = super(AddCredits, self).get_context_data(*args, **kwargs)
		# context["usercred"] = self.get_user_cred()
		return context

	def form_valid(self, form):
		credit = form.cleaned_data.get("credit")
		credit_pack = get_object_or_404(CreditToCash, label=credit)
		#save session for the credit package selected
		self.request.session["credit_id"] = credit_pack.id
		return super(AddCredits, self).form_valid(form)

	def get_success_url(self):
		return reverse('CheckOut')


class CheckOut(LoginRequiredMixin, GetCheckoutMixin, TemplateView):
	template_name = 'checkout.html'

	def dispatch(self, *args, **kwargs):
		dispatch = super(CheckOut, self).dispatch(*args, **kwargs)

		#if credit package id is not selected to exit
		try:
			credit_id = self.request.session.get("credit_id")
		except:
			return reverse('Home')
		return dispatch

	def get_context_data(self, *args, **kwargs):

		context = super(CheckOut, self).get_context_data(*args, **kwargs)
		credit_id = self.request.session.get("credit_id")
		credit_pack = get_object_or_404(CreditToCash, id=credit_id)
		context["creditcost"] = credit_pack.cashprice
		context["credit"] = credit_pack.credits
		if self.request.user.is_authenticated():
			#creating user token for using checking out
			testuser = self.request.user
			user_checkout = UserCheckOut.objects.get_or_create(user=testuser)[0]
			user_checkout.user = self.request.user
			user_checkout.save()
			context["client_token"] = user_checkout.get_client_token()

		elif not self.request.user.is_authenticated():
			return Http404
		return context

	def get_success_url(self):
		return reverse('CheckOutFinal')


class CheckOutFinal(LoginRequiredMixin, GetCheckoutMixin, TemplateView):

	def dispatch(self, *args, **kwargs):
		dispatch = super(CheckOutFinal, self).dispatch(*args, **kwargs)
		#if credit package id is not selected to exit
		try:
			credit_id = self.request.session.get("credit_id")
		except:
			return reverse('Home')
		return dispatch

	def post(self, request, *args, **kwargs):
		# print request.POST
		nonce = request.POST.get("payment_method_nonce")

		if nonce:
			result = braintree.Transaction.sale({
					"amount":self.get_credit_cost(),
					"payment_method_nonce": nonce,
					# "billing":{
					#     "postal_code":"%s" %(order.billing_address.zipcode)
					# },
					"options":{
					"submit_for_settlement":True
					}
				})

			if result.is_success:
				self.request.session["transaction_id"] = result.transaction.id
				transaction = Transaction.objects.get_or_create(
					user=self.request.user,
					transaction_id=result.transaction.id,
					success=True
					)[0]

				#saving the transaction as a record
				transaction.price=self.get_credit_cost()
				transaction.credit=self.get_credit()
				transaction.beforecredit=self.get_user_cred()
				transaction.aftercredit=int(self.get_user_cred()) + int(self.get_credit())
				transaction.save()
				#adding the credits to the account that the user has purchased
				credit = UserCredit.objects.get_or_create(
					user=self.request.user,
					)[0]

				credit.credit = int(self.get_user_cred()) + int(self.get_credit())
				credit.save()

				messages.success(request, "Thank you for your order. Please print this page.")
				return redirect("Invoice")	 

			else:
				messages.warning(request, "There is a problem with your order")
				messages.warning(request, "%s" %(result.message))
				return redirect("CheckOut")


		return redirect("CheckOut")

		def get(self, request, *args, **kwargs):
			return redirect("Invoice")



class Invoice(LoginRequiredMixin, GetCheckoutMixin, TemplateView):
	template_name = 'invoice.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Invoice, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated():
			#retrieving contents of the transaction that the user has purchased
			context["user"] = self.get_transaction().user
			context["transaction_id"] = self.get_transaction().transaction_id
			context["price"] = self.get_transaction().price
			context["creditpurchased"] = self.get_transaction().credit
			context["currentcredit"] = self.get_transaction().aftercredit
			context["timestamp"] = self.get_transaction().timestamp
			messages.success(self.request, "You have succcessfully purchased " + str(self.get_transaction().credit) + " credits")
			del self.request.session["credit_id"]
			del self.request.session["transaction_id"]

		elif not self.request.user.is_authenticated():
			return Http404

		return context




