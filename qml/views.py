from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import View, TemplateView
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db import transaction

from datetime import datetime, timedelta

from qml.helpers import is_internal
from qml.forms import *
#from qml.components.proposals.models import Referral, Proposal, HelpPage
#from qml.components.compliances.models import Compliance
#from qml.components.proposals.mixins import ReferralOwnerMixin

#from ledger.checkout.utils import create_basket_session, create_checkout_session, place_order_submission, get_cookie_basket
from django.core.management import call_command
import json
from decimal import Decimal

import logging
logger = logging.getLogger('payment_checkout')


class InternalView(UserPassesTestMixin, TemplateView):
    template_name = 'qml/dash/index.html'

    def test_func(self):
        return is_internal(self.request)

    def get_context_data(self, **kwargs):
        context = super(InternalView, self).get_context_data(**kwargs)
        context['dev'] = settings.DEV_STATIC
        context['dev_url'] = settings.DEV_STATIC_URL
        return context

class ExternalView(LoginRequiredMixin, TemplateView):
    template_name = 'qml/dash/index.html'

    def get_context_data(self, **kwargs):
        context = super(ExternalView, self).get_context_data(**kwargs)
        context['dev'] = settings.DEV_STATIC
        context['dev_url'] = settings.DEV_STATIC_URL
        return context

#class ReferralView(ReferralOwnerMixin, DetailView):
#    model = Referral
#    template_name = 'qml/dash/index.html'

#class ExternalProposalView(DetailView):
#    model = Proposal
#    template_name = 'qml/dash/index.html'

#class ExternalComplianceView(DetailView):
#    model = Compliance
#    template_name = 'qml/dash/index.html'

#class InternalComplianceView(DetailView):
#    model = Compliance
#    template_name = 'qml/dash/index.html'

class QuestionMasterlistRoutingView(TemplateView):
    template_name = 'qml/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if is_internal(self.request):
                return redirect('internal')
            return redirect('external')
        #kwargs['form'] = LoginForm
        #return super(BorangaRoutingView, self).get(*args, **kwargs)
        return redirect('/accounts/login')


class BorangaContactView(TemplateView):
    template_name = 'qml/contact.html'

class BorangaFurtherInformationView(TemplateView):
    template_name = 'qml/further_info.html'

#class InternalProposalView(DetailView):
#    #template_name = 'qml/index.html'
#    model = Proposal
#    template_name = 'qml/dash/index.html'
#
#    def get(self, *args, **kwargs):
#        if self.request.user.is_authenticated:
#            if is_internal(self.request):
#                #return redirect('internal-proposal-detail')
#                return super(InternalProposalView, self).get(*args, **kwargs)
#            return redirect('external-proposal-detail')
#        kwargs['form'] = LoginForm
#        return super(BorangaRoutingDetailView, self).get(*args, **kwargs)


@login_required(login_url='ds_home')
def first_time(request):
    context = {}
    if request.method == 'POST':
        form = FirstTimeForm(request.POST)
        redirect_url = form.data['redirect_url']
        if not redirect_url:
            redirect_url = '/'
        if form.is_valid():
            # set user attributes
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.dob = form.cleaned_data['dob']
            request.user.save()
            return redirect(redirect_url)
        context['form'] = form
        context['redirect_url'] = redirect_url
        return render(request, 'qml/user_profile.html', context)
    # GET default
    if 'next' in request.GET:
        context['redirect_url'] = request.GET['next']
    else:
        context['redirect_url'] = '/'
    context['dev'] = settings.DEV_STATIC
    context['dev_url'] = settings.DEV_STATIC_URL
    #return render(request, 'qml/user_profile.html', context)
    return render(request, 'qml/dash/index.html', context)


class HelpView(LoginRequiredMixin, TemplateView):
    template_name = 'qml/help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            application_type = kwargs.get('application_type', None)
            if kwargs.get('help_type', None)=='assessor':
                if is_internal(self.request):
                    qs = HelpPage.objects.filter(application_type__name__icontains=application_type, help_type=HelpPage.HELP_TEXT_INTERNAL).order_by('-version')
                    context['help'] = qs.first()
#                else:
#                    return TemplateResponse(self.request, 'qml/not-permitted.html', context)
#                    context['permitted'] = False
            else:
                qs = HelpPage.objects.filter(application_type__name__icontains=application_type, help_type=HelpPage.HELP_TEXT_EXTERNAL).order_by('-version')
                context['help'] = qs.first()
        return context


class ManagementCommandsView(LoginRequiredMixin, TemplateView):
    template_name = 'qml/mgt-commands.html'

    def post(self, request):
        data = {}
        command_script = request.POST.get('script', None)
        if command_script:
            print ('running {}'.format(command_script))
            call_command(command_script)
            data.update({command_script: 'true'})

        return render(request, self.template_name, data)


