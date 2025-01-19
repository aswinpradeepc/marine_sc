from django.urls import path

from .views import (IndexView, RegisterView, OtpView, LoginView,
                    submission_view, TeamView, RefundView, TermsView, PrivacyPolicyView, DisclaimerView, PosterGuidelinesView, AbstractGuidelinesView,contact_form)

urlpatterns = [
    path('', IndexView.as_view(), name='maricon'),
    # path('committee/', CommitteeView.as_view(), name='committee'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/otp/', OtpView.as_view(), name='otp'),
    path('login/otp/', OtpView.as_view(), name='otp'),
    path('abstract/', submission_view, name='submission'),
    path('login/', LoginView.as_view(), name='login'),
    path('committee/', TeamView.as_view(), name='login'),
    path('refund/', RefundView.as_view(), name='refund'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),
    path('disclaimer/', DisclaimerView.as_view(), name='disclaimer'),
    path('poster-guidelines/', PosterGuidelinesView.as_view(), name='poster-guidelines'),
    path('abstract-guidelines/', AbstractGuidelinesView.as_view(), name='abstract-guidelines'),
    path('conatct_form', contact_form, name='contact_form'),
]
