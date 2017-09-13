"""teachadvisor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from home.views import HomeView, AboutUsView, PromotionView, ContactView, TermsAndConditionView, DisclaimerView, PrivacyPolicyView, RefundPolicyView, FAQTutorView, FAQStudentView, CSupportView, TutorialsView, CareersView, PressView, PartnershipsView, SiteMapView, Test

from teacher.views import TeacherCreate, TeacherUpdate, TeacherList, TeacherDetail, FavTeacherList
from student.views import StudentCreate, StudentUpdate, StudentList, StudentDetail

from billing.views import AddCredits, CheckOut, CheckOutFinal, Invoice



#test push


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/',include('allauth.urls')),
    url(r'^$', HomeView.as_view(), name='Home'),
    url(r'^contact/$', ContactView.as_view(), name='Contact'),
    url(r'^promotions/$', PromotionView.as_view(), name='Promotions'),

    url(r'^termsandconditions/$', TermsAndConditionView.as_view(), name='TermsAndCondition'),
    url(r'^disclaimer/$', DisclaimerView.as_view(), name='Disclaimer'),
    url(r'^privacypolicy/$', PrivacyPolicyView.as_view(), name='PrivacyPolicy'),
    url(r'^refundpolicy/$', RefundPolicyView.as_view(), name='RefundPolicy'),

    url(r'^FAQTutors/$', FAQTutorView.as_view(), name='FAQTutor'),
    url(r'^FAQStudents/$', FAQStudentView.as_view(), name='FAQStudent'),
    url(r'^customersupport/$', CSupportView.as_view(), name='Customer_Support'),
    url(r'^tutorials/$', TutorialsView.as_view(), name='Tutorials'),

    url(r'^aboutus/$', AboutUsView.as_view(), name='AboutUs'),
    url(r'^careers/$', CareersView.as_view(), name='Careers'),
    url(r'^press/$', PressView.as_view(), name='Press'),
    url(r'^partnership/$', PartnershipsView.as_view(), name='Partnership'),


    url(r'^site-map/$', SiteMapView.as_view()),



    url(r'^test/$', Test, name='Test'),

    #billing and subscription

    url(r'^billing/creditadd/$', AddCredits.as_view(), name='AddCredits'),
    url(r'^billing/checkout/$', CheckOut.as_view(), name='CheckOut'),
    url(r'^billing/checkout/final$', CheckOutFinal.as_view(), name='CheckOutFinal'),
    url(r'^billing/checkout/invoice$', Invoice.as_view(), name='Invoice'),

    #worker details
    url(r'^tutor/add/$', TeacherCreate.as_view(), name='TeacherCreate'),
    url(r'^tutor/$', TeacherList.as_view(), name='TeacherList'),
    url(r'^tutor/(?P<pk>[0-9]+)/edit$', TeacherUpdate.as_view(), name='TeacherUpdate'),
    url(r'^tutor/(?P<pk>[0-9]+)/$', TeacherDetail.as_view(), name='TeacherDetail'),

    #company details
    url(r'^student/add/$', StudentCreate.as_view(), name='StudentCreate'),
    url(r'^student/$', StudentList.as_view(), name='StudentList'), #to block when live
    url(r'^student/(?P<pk>[0-9]+)/edit$', StudentUpdate.as_view(), name='StudentUpdate'),
    url(r'^student/(?P<pk>[0-9]+)/$', StudentDetail.as_view(), name='StudentDetail'),


    



]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
