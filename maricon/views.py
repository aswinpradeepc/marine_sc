import logging

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse
# import send email function

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from base.utils import sendmail
from authentication.forms import SignUpForm
from authentication.models import User
from base.utils import sendmail
from payment.utils import payment_completed
from .forms import PaperAbstractForm
from .models import Faq, Sponsor, Schedule, Gallery, CommitteeMember, Committee, OTP, PaperAbstract, Speaker, \
    THEMES, Contact

logger = logging.getLogger("db")


class AbstractView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(AbstractView, self).get_context_data(**kwargs)
        context['speakers'] = Speaker.objects.all()
        context['faqs'] = Faq.objects.all()
        context['sponsors'] = Sponsor.objects.all()
        context['schedule'] = [
            {
                'day': 'Day 1',
                'schedule': Schedule.objects.filter(day='Day 1')
            },
            {
                'day': 'Day 2',
                'schedule': Schedule.objects.filter(day='Day 2')
            },
            {
                'day': 'Day 3',
                'schedule': Schedule.objects.filter(day='Day 3')
            },
        ]
        context['themes'] = THEMES
        context['gallery'] = Gallery.objects.all()
        committees = Committee.objects.only('name').order_by('-size_on_website')
        context['committees'] = committees

        return context

class GalleryView(AbstractView):
    template_name = "home/gallery.html"

class TravelGrantView(AbstractView):
    template_name = "home/travel_grant.html"

class IndexView(AbstractView):
    template_name = 'home/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['speakers'] = Speaker.objects.all()
        return context

class CommitteeView(AbstractView):
    template_name = 'maricon/committee.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeView, self).get_context_data(**kwargs)
        committees = Committee.objects.all().order_by('-size_on_website')
        context['committee_names'] = committees
        context['committees'] = [
            {
                'committee': committee,
                'members': CommitteeMember.objects.filter(committee=committee)
            }
            for committee in committees
        ]
        return context


class RegisterView(AbstractView):
    template_name = 'new_maricon/signup.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['form'] = SignUpForm()
        return context

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/payment')
        return super().get(request)

    def post(self, request):

        if request.method == 'POST':
            # Assuming you have a custom User model, adjust the form accordingly
            form = SignUpForm(request.POST)
            logger.debug("user trying to register")
            logger.debug(f"request.post = {request.POST}")

            if form.is_valid():
                # Create a new user with the extended information
                logger.debug("form valid")
                user = form.save(commit=False)
                user.full_name = form.cleaned_data['full_name']
                user.gender = form.cleaned_data['gender']
                user.mobile_number = form.cleaned_data['mobile_number']
                user.save()
                messages.success(request, 'Account created successfully.')
                context = self.get_context_data()
                OTP.objects.create(user=user).send_email()
                context['otp'] = True
                context['email'] = user.email
                logger.debug("email sent")
                return render(request, 'new_maricon/signup.html', context)
            else:
                logger.debug("form invalid errors")
                logger.debug(form.errors.as_data())
                context = self.get_context_data()
                context['form'] = form
                messages.error(request, 'Error creating the account. Please check the form.', context)

                return render(request, 'new_maricon/signup.html', context)
        return render(request, 'new_maricon/signup.html', self.get_context_data())


class OtpView(AbstractView):
    template_name = 'new_maricon/login.html'

    def post(self, request):
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        logger.debug(f"otp received {email=} {otp=}")
        if not email or not otp:
            logger.error(f"no otp or email provided {email=} {otp=}")
            return redirect('maricon:login')
        email = email.lower().strip()
        otp = otp.strip()
        logger.debug("get email and otp")
        otp_obj = OTP.objects.filter(user__email=email, otp=otp)
        if otp_obj.exists() and otp_obj.first().is_valid():
            logger.debug(f"otp is valid login user {otp_obj.first().user}")
            login(request, otp_obj.first().user)
            return redirect('submission')
        else:
            logger.debug("invalid otp err sent")
            context = self.get_context_data()
            context['err'] = True
            context['msg'] = "Invalid OTP"
            context['email'] = email
            context['otp'] = True
            return render(request, self.template_name, context)


@payment_completed
def submission_view(request):
    context = {'speakers': Speaker.objects.all(), 'faqs': Faq.objects.all(), 'sponsors': Sponsor.objects.all(),
               'schedule': [
                   {
                       'day': 'Day 1',
                       'schedule': Schedule.objects.filter(day='Day 1')
                   },
                   {
                       'day': 'Day 2',
                       'schedule': Schedule.objects.filter(day='Day 2')
                   },
                   {
                       'day': 'Day 3',
                       'schedule': Schedule.objects.filter(day='Day 3')
                   },
               ], 'gallery': Gallery.objects.all(),
               "themes": THEMES,
               "abstract": PaperAbstract.objects.filter(user=request.user).first(),

               }
    if request.GET.get('payment') == "success":
        context['payment'] = "Payment completed successful please submit your abstract"
    committees = Committee.objects.only('name').order_by('-size_on_website')
    context['committees'] = committees
    if request.user.is_authenticated:
        if request.method == 'POST':
            logger.debug("user trying to submit the abstract")
            form = PaperAbstractForm(request.POST, request.FILES)
            logger.debug(request.FILES)
            if form.is_valid():
                # Save the abstract to the database
                logger.debug("valid abstract details")
                abstract = form.save(commit=False)
                abstract.user = request.user
                abstract.save()
                logger.debug("abstract submitted successfully")
                abstract.send_email()
                logger.debug("email sent to admin")
                context['abstract'] = abstract
                sendmail(
                    f"Dear sir, You have been successfully submitted the abstract for the presentation in ICMBGSD-2025” ",
                    request.user.email, "ICMBGSD-2025 abstract submission"
                )
                messages.success(request, 'Abstract submitted successfully!')
                return render(request, 'new_maricon/abstract.html', context)
            else:
                messages.error(request, 'Error submitting the abstract. Please check the form.')
                logger.debug(form.errors.as_data())
                sendmail(
                    f"Dear sir, "
                    f"Your abstract has failed, please try again or contact the team is issue persists"
                    "With Regards \n ICMBGSD-2025", request.user.email, "ICMBGSD-2025 abstract submission"
                )

        else:
            form = PaperAbstractForm()
            context['form'] = form

        return render(request, 'new_maricon/abstract.html', context)

    return redirect('login')


class LoginView(AbstractView):
    template_name = 'new_maricon/login.html'

    # handle post request
    def post(self, request):
        email = request.POST.get('email')
        context = self.get_context_data()

        if User.objects.filter(email=email).exists():
            otp = OTP.objects.create(user=User.objects.get(email=email))
            context['otp'] = True
            context['email'] = email
            otp.send_email()
            response = render(request, self.template_name, context)

            return response
        context['err'] = True
        context['msg'] = "Invalid Email Please Register to continue"
        print(context)
        return render(request, self.template_name, context)


class TeamView(AbstractView):
    template_name = 'new_maricon/team.html'

    def get_context_data(self, **kwargs):
        context = super(TeamView, self).get_context_data(**kwargs)
        committees = Committee.objects.all().order_by('-size_on_website')
        context['committee_names'] = committees
        context['committees'] = [
            {
                'committee': committee,
                'members': CommitteeMember.objects.filter(committee=committee)
            }
            for committee in committees
        ]
        # context["advisory"] = [
        #     "Prof. (Dr.) P. G. Sankaran, Vice Chancellor, CUSAT",
        #     "Dr. M. Ravichandran, Secretary, MoES, New Delhi",
        #     "Dr. Shailesh Nayk, Director, NIAS, Bangalore",
        #     "Dr. Rasik Ravindra, Chairman, INSA-SCAR, New Delhi",
        #     "Dr. Thamban Meloth, Director, NCPOR, Goa",
        #     "Prof. (Dr.) N.V. Chalapathi Rao, Director, NCESS, Trivandrum",
        #     "Prof. (Dr.) N. C. Pant, Delhi University, New Delhi",
        #     "Prof. (Dr.) M. Radhakrishna, IIT-Bombay, Mumbai",
        #     "Prof. (Dr.) C.T. Aravindakumar, Vice Chancellor, MG University",
        #     "Prof. (Dr.) Bijoy S. Nandan, Vice Chancellor, Kannur University",
        #     "Prof. (Dr.) T. Pradeep Kumar, Vice-Chancellor, KUFOS, Kochi",
        #     "Prof. (Dr.) Harilal B. Menon, Vice-Chancellor, Goa University",
        #     "Prof. (Dr.) Hironori Ando, Niigata University, Japan",
        #     "Prof. (Dr.) Satish Kumar, Niigata University",
        #     "Prof. (Dr.) Syed Hashsham, Michigan State University, USA",
        #     "Prof. (Dr.) PKSM Rahman, Liverpool John Moores University, UK",
        #     "Prof. (Dr.) A. P. Pradeepkumar, Director, SESS, University of Kerala",
        #     "Prof. (Dr.) S. Suresh Kumar, Dean, KUFOS, Kochi",
        #     "Dr.David Jones,CEO, Justoneocean, UK",
        #     'Dr. Ajaya Ravindran, NYU, Abu Dhabi',
        #     "Dr. GVM Gupta, Director, CMLRE, Kochi",
        #     "Dr. M. Habibulla, Director, CIFNET, Koch",
        #     'Dr. George Ninan, Director, CIFT, Kochi',
        #     'Dr. A. Gopalakrishnan,Director, CMFRI, Kochi',
        #     'Dr. Manoj Samuel, Executive Director, CWRDM, Calicut',
        #     'Dr. Jyothibabu R., Division Head, NIO-RC, Kochi',
        #     'Dr. N.P. Kurian, Vice President, Ocean Society of India'
        # ]
        # context["local"] = [
        #     "Prof.(Dr.) A.A.Mohamed Hatha(Organizing Chairman)",
        #     "Prof.(Dr.)Sunil P.S.(Organizing Convenor)",
        #     "Dr.Rahul Mohan(Co - convenor)", ]
        context["members"] = [
            "Prof. (Dr.) R. Sajeev",
            "Prof. (Dr.) K. Satheeshan",
            "Prof. (Dr.) Sajeevan T. P.",
            "Shri. Baby Chakrapani",
            "Dr. Joji V. S.",
            "Dr. Abhilash S.",
            "Dr. P. Preetham Elumalai",
            "Dr. Venu S.",
            "Dr. V. Madhu",
            "Dr. Saji P. K.",
            "Dr. Ajayakumar P.",
            "Dr. N. R. Nisha",
            "Dr. Swapna P. Antony",
            "Dr. Priyaja P.",
            "Dr. K. B. Padmakumar",
            "Dr. Habeeb Rahman",
            "Dr. V. Vijith",
            "Dr. Ratheesh Kumar R. T.",
            "Dr. Shaju S. S.",
            "Dr. Jorphin Joseph",
            "Dr. Midhun M",
            "Dr. Lekshmi P. R.",
            "Dr. Amaldev T.",
            "Dr. Honey H. Das",
            "Dr. Naveen P. U.",
            "Dr. Selvia Kuriakose",
            "Dr. Sreekala P. P.",
            "Dr. Chaithanya E. R.",
            "Dr. Lathika Cicily Thomas",
            "Dr. Mohammed Noohu Nazeer"
        ]

        return context


@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save data to the model
        con = Contact.objects.create(name=name, email=email, subject=subject, message=message)
        con.save()

        # Redirect or show success message
        return redirect('/')


class PrivacyPolicyView(AbstractView):
    template_name = 'home/privacy_policy.html'


class TermsView(AbstractView):
    template_name = 'home/terms_and_conditions.html'


class RefundView(AbstractView):
    template_name = 'new_maricon/refund.html'


class PosterGuidelinesView(AbstractView):
    template_name = 'home/poster_guidelines.html'

class AbstractGuidelinesView(AbstractView):
    template_name = 'home/abstract_guidelines.html'  

class DisclaimerView(AbstractView):
    template_name = 'new_maricon/disclaimer.html'

