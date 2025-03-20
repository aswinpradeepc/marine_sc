from django.urls import path

from .views import (IndexView, RegisterView, OtpView, LoginView,
                    submission_view, TeamView, RefundView, TermsView,
                    PrivacyPolicyView, DisclaimerView, PosterGuidelinesView,
                    AbstractGuidelinesView, contact_form, GalleryView,
                    TravelGrantView, ApplyTravelGrantView, AccommodationView, AbstracSubmissionClosedView)

urlpatterns = [
    path('', IndexView.as_view(), name='maricon'),
    # path('committee/', CommitteeView.as_view(), name='committee'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/otp/', OtpView.as_view(), name='otp'),
    path('login/otp/', OtpView.as_view(), name='otp'),
    path('abstract/', submission_view, name='submission'),
    path('login/', LoginView.as_view(), name='login'),
    path('committee/', TeamView.as_view(), name='login'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('travel_grant/', TravelGrantView.as_view(), name='travel_grant'),
    path('apply_travel_grant/', ApplyTravelGrantView.as_view(), name='apply_travel_grant'),
    path('refund/', RefundView.as_view(), name='refund'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),
    path('disclaimer/', DisclaimerView.as_view(), name='disclaimer'),
    path('poster-guidelines/', PosterGuidelinesView.as_view(), name='poster-guidelines'),
    path('abstract-guidelines/', AbstractGuidelinesView.as_view(), name='abstract-guidelines'),
    path('accommodation/', AccommodationView.as_view(), name='accommodation'),
    path('conatct_form/', contact_form, name='contact_form'),
    path('abstract_closed/', AbstracSubmissionClosedView.as_view(), name='abstract_closed'),
]
