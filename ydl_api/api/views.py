from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from django.contrib.auth.models import User, AnonymousUser  # If used custom user model
# Our imports
from .models import Course, Student, Resource, Announcement, Teacher, User, Post, Message
from .serializers import UserSerializer, CourseSerializer, LongUserSerializer, StudentSerializer, \
    ResourceSerializer, AnnouncementSerializer, PostSerializer, MessageSerializer

from django.db.models import Q 

# Email Stuff A
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from django.core.exceptions import ObjectDoesNotExist
# Email Stuff E

# Payment
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded

# own 404
from django.shortcuts import (
    render_to_response
)
from django.template import RequestContext

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def render_email(request):
    context = {
        'user': 'Croozer',
        'link': 'https://api.ydlearning.com/activate/',
        'expires_in': '1',
        'expires_time': ' hours',  # change plural!
        # 'logo_img_link':"",
        'email_sendto': 'Croozer@',
        'ydl_context': "Context Text",
        'ydl_email': "admin@ydlearning.com",
        'ydl_url': "https://www.ydlearning.com",
        'ydl_url_github': "https://github.com/YoungAndDigitalLearning",
        'ydl_url_impr': "https://www.ydlearning.com/sites/impressum.html",
    }

    context2 = {
        'user': 'Croozer2',
        'link': 'https://api.ydlearning.com/ressource/',
        'expires_in': '1',
        'expires_time': ' hours',  # change plural!
        # 'logo_img_link':"",
        'email_sendto': 'Croozer@ydlaerning.com',
        'ydl_context': "Context Text",
        'ydl_email': "admin@ydlearning.com",
        'ydl_url': "https://www.ydlearning.com",
        'ydl_url_github': "https://github.com/YoungAndDigitalLearning",
        'ydl_url_impr': "https://www.ydlearning.com/sites/impressum.html",
    }

    # return render(request, "api/verification_email.html", context)
    # return render(request, "api/verified.html", context)
    return render(request, "api/ressource_save.html", context2)


def activate(request, uidb64, token):
    """
    Activates an account

    Arguments:
        request {[type]} -- [description]
        uidb64 {[type]} -- [description]
        token {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64).decode())
        user = User.objects.get(pk=uid)
        print("user: ", user)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    verifier = VerifyJSONWebTokenSerializer()
    # print("verifier:", verifier.validate({'token':token}))
    validated = None
    # verifier.validate({'token':token})
    try:
        validated = jwt_decode_handler(token)
    except:
        pass

    if user is not None and validated:
        user.isEmailActivated = True
        user.save()
        # return redirect('home')
        return HttpResponse(''' 
        <html>

<body>
	<!-- Wrapper/Container Table: Use a wrapper table to control the width and the background color consistently of your email. Use this approach instead of setting attributes on the body tag. -->
	<table cellpadding="0" width="100%" cellspacing="0" border="0" id="backgroundTable" class='bgBody'>
		<tr>
			<td>
				<table cellpadding="0" width="620" class="container" align="center" cellspacing="0" border="0">
					<tr>
						<td>
							<!-- Tables are the most common way to format your email consistently. Set your table widths inside cells and in most cases reset cellpadding, cellspacing, and border to zero. Use nested tables as a way to space effectively in your message. -->


							<table cellpadding="0" cellspacing="0" border="0" align="center" width="600" class="container">
								<tr>
									<td class='movableContentContainer bgItem'>

										<div class='movableContent'>
											<table cellpadding="0" cellspacing="0" border="0" align="center" width="600" class="container">
												<tr height="40">
													<td width="200">&nbsp;</td>
													<td width="200">&nbsp;</td>
													<td width="200">&nbsp;</td>
												</tr>

												<tr height="25">
													<td width="200">&nbsp;</td>
													<td width="200">&nbsp;</td>
													<td width="200">&nbsp;</td>
												</tr>

											</table>
										</div>

										<div class='movableContent'>
											<table cellpadding="0" cellspacing="0" border="0" align="center" width="600" class="container">
												<tr>
													<td width="100%" colspan="3" align="center" style="padding-bottom:0px;padding-top:0px;">
														<div class="contentEditableContainer contentTextEditable">
															<div class="contentEditable" align='center'>
																<h1>Email verified</h1>
															</div>
														</div>
													</td>
												</tr>
												<tr>
													<td width="100">&nbsp;</td>
													<td width="400" align="center">
														<div class="contentEditableContainer contentTextEditable">
															<div class="contentEditable" align='left'>
																<br>
																<p>
																	Thank you for verification.
																	<br>
																	<br/> You can now use all features of
																	<i style="color:#0689b3;">
																		<b>Y&D Learning</b>
																	</i>.
																	<br/>
																	<br/> Go to mainpage:
																</p>
															</div>
														</div>
													</td>
													<td width="100">&nbsp;</td>
												</tr>
											</table>
											<table cellpadding="0" cellspacing="0" border="0" align="center" width="600" class="container">
												<tr>
													<td width="200">&nbsp;</td>
													<td width="200" align="center" style="padding-top:20px;">
														<table cellpadding="0" cellspacing="0" border="0" align="center" width="200" height="50">
															<tr>
																<td bgcolor="#0689b3" align="center" style="border-radius:4px;" width="200" height="50">
																	<div class="contentEditableContainer contentTextEditable">
																		<div class="contentEditable" align='center'>
																			<a target='_blank' href="https://ydlearning.com/" class='link2'>Homepage</a>
																		</div>
																	</div>
																</td>
															</tr>
														</table>
													</td>
													<td width="200">&nbsp;</td>
												</tr>
											</table>
										</div>


									</td>
								</tr>
							</table>
						</td>
					</tr>
				</table>

			</td>
		</tr>
	</table>
</body>

</html>
        ''')
    else:
        return HttpResponse('Activation link is invalid!')

def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'payment.html',
                            {'form': form, 'payment': payment})

class UserViewSet(ModelViewSet):

    """ User Resource
    ---
    create_request_serializer: UserSerializer
    create_response_serializer: UserSerializer
    """

    model = User
    permission_classes = [
        permissions.AllowAny  # Or users can't register
    ]

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserSerializer
        else:
            return LongUserSerializer

class StudentViewSet(ModelViewSet):
    model = Student
    serializer_class = StudentSerializer

    queryset = Student.objects.all()

    # Debug
    permission_classes = [
        permissions.AllowAny
    ]


class ListCreateResourceAPIView(ListCreateAPIView):
    model = Resource
    serializer_class = ResourceSerializer

    queryset = Resource.objects.all()

    # automatically assign the owner to the resource
    def perform_create(self, serializer):
        serializer.validated_data["uploader"] = self.request.user
        serializer.save()


class ListCreateAnnouncementAPIView(ListCreateAPIView):
    model = Announcement
    serializer_class = AnnouncementSerializer

    # allow a limit for announcements
    def get_queryset(self):
        if self.request.method == "GET":
            limit = self.request.GET.get("limit", None)
            if limit:
                return Announcement.objects.all()[:int(limit)]
            else:
                return Announcement.objects.all()

    # Everyone should see
    permission_classes = [
        permissions.AllowAny
    ]

class CourseViewSet(ModelViewSet):
    model = Course
    serializer_class = CourseSerializer

    # automatically assign the teacher to the course
    def perform_create(self, serializer):
        serializer.validated_data["teacher"] = Teacher.objects.get(user=self.request.user)
        serializer.save()

    def get_queryset(self):
        if self.request.method == "GET":
            # distinguished between paid and free courses if a type is provided
            course_type = self.request.GET.get("type", None)
            if course_type:
                if course_type == "paid": 
                    return Course.objects.filter(price__gt=0)
                elif course_type == "free":
                    return Course.objects.filter(price=0)
            # return the courses for the specific user
            else:
                return self.request.user.get_courses()


    # Everyone should see
    permission_classes = [
        permissions.IsAuthenticated
    ]

class PostViewSet(ModelViewSet):
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    permission_classes = [
        permissions.AllowAny 
    ]

class MessageViewSet(ModelViewSet):
    model = Message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    permission_classes = [
        permissions.AllowAny
    ]
