from django.conf import settings
#from django.contrib import admin
from qml.admin import admin
from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from django.contrib.auth import logout, login # DEV ONLY

from django.conf.urls.static import static
from rest_framework import routers
from qml import views
#from qml.admin import qml_admin_site
#from qml.components.qml import views as qml_views
#from qml.components.proposals import views as proposal_views
#from qml.components.organisations import views as organisation_views
#
#from qml.components.users import api as users_api
#from qml.components.organisations import api as org_api
#from qml.components.main import api as main_api
#from qml.components.proposals import api as proposal_api
#from qml.components.approvals import api as approval_api
#from qml.components.compliances import api as compliances_api
from qml.components.masterlist import api as masterlist_api
from ledger_api_client.urls import urlpatterns as ledger_patterns

# API patterns
router = routers.DefaultRouter()
#router.register(r'organisations',org_api.OrganisationViewSet)
#router.register(r'proposal',proposal_api.ProposalViewSet)
#router.register(r'proposal_submit',proposal_api.ProposalSubmitViewSet)
#router.register(r'proposal_paginated',proposal_api.ProposalPaginatedViewSet)
#router.register(r'approval_paginated',approval_api.ApprovalPaginatedViewSet)
#router.register(r'compliance_paginated',compliances_api.CompliancePaginatedViewSet)
#router.register(r'referrals',proposal_api.ReferralViewSet)
#router.register(r'approvals',approval_api.ApprovalViewSet)
#router.register(r'compliances',compliances_api.ComplianceViewSet)
#router.register(r'proposal_requirements',proposal_api.ProposalRequirementViewSet)
#router.register(r'proposal_standard_requirements',proposal_api.ProposalStandardRequirementViewSet)
#router.register(r'organisation_requests',org_api.OrganisationRequestsViewSet)
#router.register(r'organisation_contacts',org_api.OrganisationContactViewSet)
#router.register(r'my_organisations',org_api.MyOrganisationsViewSet)
#router.register(r'users',users_api.UserViewSet)
#router.register(r'amendment_request',proposal_api.AmendmentRequestViewSet)
#router.register(r'compliance_amendment_request',compliances_api.ComplianceAmendmentRequestViewSet)
#router.register(r'global_settings', main_api.GlobalSettingsViewSet)
##router.register(r'application_types', main_api.ApplicationTypeViewSet)
#router.register(r'assessments', proposal_api.ProposalAssessmentViewSet)
#router.register(r'required_documents', main_api.RequiredDocumentViewSet)
#router.register(r'questions', main_api.QuestionViewSet)
router.register(r'layers', masterlist_api.LayerViewSet)
router.register(r'layer_features',masterlist_api.FeatureViewSet)

api_patterns = [
#    url(r'^api/profile$', users_api.GetProfile.as_view(), name='get-profile'),
#    url(r'^api/countries$', users_api.GetCountries.as_view(), name='get-countries'),
#    url(r'^api/department_users$', users_api.DepartmentUserList.as_view(), name='department-users-list'),
#    url(r'^api/filtered_users$', users_api.UserListFilterView.as_view(), name='filtered_users'),
#    #url(r'^api/filtered_organisations$', org_api.OrganisationListFilterView.as_view(), name='filtered_organisations'),
#    url(r'^api/filtered_payments$', approval_api.ApprovalPaymentFilterViewSet.as_view(), name='filtered_payments'),
#    url(r'^api/proposal_type$', proposal_api.GetProposalType.as_view(), name='get-proposal-type'),
#    url(r'^api/empty_list$', proposal_api.GetEmptyList.as_view(), name='get-empty-list'),
#    url(r'^api/organisation_access_group_members',org_api.OrganisationAccessGroupMembers.as_view(),name='organisation-access-group-members'),
    url(r'^api/',include(router.urls)),
#    url(r'^api/amendment_request_reason_choices',proposal_api.AmendmentRequestReasonChoicesView.as_view(),name='amendment_request_reason_choices'),
#    url(r'^api/compliance_amendment_reason_choices',compliances_api.ComplianceAmendmentReasonChoicesView.as_view(),name='amendment_request_reason_choices'),
#    url(r'^api/search_keywords',proposal_api.SearchKeywordsView.as_view(),name='search_keywords'),
#    url(r'^api/search_reference',proposal_api.SearchReferenceView.as_view(),name='search_reference'),
]

# URL Patterns
urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'admin/', admin.site.urls),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    url(r'', include(api_patterns)),
    url(r'^$', views.QuestionMasterlistRoutingView.as_view(), name='ds_home'),


#    path(r'admin/', admin.site.urls),
#    #url(r'^admin/', include(qml_admin_site.urls)),
#    #url(r'^admin/', qml_admin_site.urls),
#    #url(r'^login/', LoginView.as_view(),name='login'),
#    #path('login/', login, name='login'),
#    url(r'^logout/$', LogoutView.as_view(), {'next_page': '/'}, name='logout'),
#    url(r'', include(api_patterns)),
#    url(r'^$', views.BorangaRoutingView.as_view(), name='ds_home'),
#    url(r'^contact/', views.BorangaContactView.as_view(), name='ds_contact'),
#    url(r'^further_info/', views.BorangaFurtherInformationView.as_view(), name='ds_further_info'),
#    url(r'^internal/', views.InternalView.as_view(), name='internal'),
#    url(r'^internal/proposal/(?P<proposal_pk>\d+)/referral/(?P<referral_pk>\d+)/$', views.ReferralView.as_view(), name='internal-referral-detail'),
#    url(r'^external/', views.ExternalView.as_view(), name='external'),
#    url(r'^firsttime/$', views.first_time, name='first_time'),
#    url(r'^account/$', views.ExternalView.as_view(), name='manage-account'),
#    url(r'^profiles/', views.ExternalView.as_view(), name='manage-profiles'),
#    url(r'^help/(?P<application_type>[^/]+)/(?P<help_type>[^/]+)/$', views.HelpView.as_view(), name='help'),
#    url(r'^mgt-commands/$', views.ManagementCommandsView.as_view(), name='mgt-commands'),
#    #url(r'test-emails/$', proposal_views.TestEmailView.as_view(), name='test-emails'),
#    url(r'^proposal/$', proposal_views.ProposalView.as_view(), name='proposal'),
] + ledger_patterns

if settings.EMAIL_INSTANCE != 'PROD':
    urlpatterns.append(path('accounts/', include('django.contrib.auth.urls')))

#if settings.DEBUG:  # Serve media locally in development.
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.SHOW_DEBUG_TOOLBAR:
#    import debug_toolbar
#    urlpatterns = [
#        url('__debug__/', include(debug_toolbar.urls)),
#    ] + urlpatterns
