from django.db.models.query import QuerySet
from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import FormView,CreateView,TemplateView,View,UpdateView,DetailView,ListView
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator 
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from app.models import *
from app.forms import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
from app.decorator import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.

decs=[login_required,never_cache]


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user_register.html'
    success_url = reverse_lazy('signin')

    def form_valid(self, form):
        form.instance.role = 'user'
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("signin")


class AdminRegistrationView(CreateView):
    model = User
    form_class = AdminRegistrationForm
    template_name = 'admin_register.html'
    success_url = reverse_lazy('signin')

    def form_valid(self, form):
        form.instance.role = 'admin'
        return super().form_valid(form)


class PoliceRegistrationView(CreateView):
    model = PoliceProfile
    form_class = PoliceRegistrationForm
    template_name = 'police_register.html'
    success_url = reverse_lazy('adminindex')

    def form_valid(self, form):
        form.instance.role = 'police'
        return super().form_valid(form) 
@method_decorator(decs,name="dispatch")  

class UserIndexView(TemplateView):
    template_name="user_index.html"


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            if user.role == 'user':
                return redirect('userindex')
            elif user.role == 'police':
                return redirect('policeindex')
            else:
                return redirect('adminindex')
        return super().form_invalid(form) 

@method_decorator(decs,name="dispatch")  

class PoliceIndexView(TemplateView):
    template_name="police_index.html"
      
@method_decorator(decs,name="dispatch")  

class AdminIndexView(TemplateView):
    template_name="admin_index.html"  

class signoutView(View):
    def get(self,request,*args,**kwargs):
         logout(request)
         return redirect("signin")      

@method_decorator(decs,name="dispatch")  

class UserprofileAddView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'userprofile.html'
    success_url = reverse_lazy('userindex')

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]
    
@method_decorator(decs,name="dispatch")  
  
class UpdateUserProfileView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'edituserprofile.html'
    success_url = reverse_lazy('userindex')

    def get_object(self, queryset=None):
        # Get the profile object for the current user if it exists, otherwise return None
        return UserProfile.objects.get_or_create(user=self.request.user)[0]  
     
@method_decorator(decs,name="dispatch")  

class UserListView(ListView):
    template_name="userlist.html"    
    model=UserProfile
    context_object_name="data" 

@method_decorator(decs,name="dispatch")  

class SpecifiedUser(DetailView):
    model = UserProfile
    template_name = 'userlist.html'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get("pk")
        try:
            user = User.objects.get(pk=user_id)
            return UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        except UserProfile.DoesNotExist:
            raise Http404("UserProfile does not exist for the specified user")

    

# class PoliceprofileAddView(UpdateView):
#     model = PoliceProfile
#     form_class = PoliceProfileForm
#     template_name = 'add_policestation.html'
#     success_url = reverse_lazy('adminindex')

#     def get_object(self, queryset=None):
#         return PoliceProfile.objects.get_or_create(user=self.request.user)[0]
    
@method_decorator(decs,name="dispatch")  

class ComplaintView(CreateView):
    model= Complaint
    form_class = ComplaintForm
    template_name = 'complaint.html'
    success_url = reverse_lazy('userindex')

    def form_valid(self, form):
        form.instance.complainant = self.request.user
        return super().form_valid(form)    
    
@method_decorator(decs,name="dispatch")  

class ComplaintListView(ListView):
    model = Complaint
    template_name = 'police_compalint_list.html'
    context_object_name = 'complaints'  

@method_decorator(decs,name="dispatch")  

class AdminComplaintListView(ListView):
    model = Complaint
    template_name = 'admincomplaint_list.html'
    context_object_name = 'complaint'     




@method_decorator(decs,name="dispatch")  

class SaftytipsView(CreateView):
    model= Saftytips
    form_class = SaftytipsForm
    template_name = 'safty_tips.html'
    success_url = reverse_lazy('adminindex')

@method_decorator(decs,name="dispatch")  

class SafetyTipListView(ListView):
    model = Saftytips
    template_name = 'saftytips_list.html'  # Replace 'safetytip_list.html' with your actual template
    context_object_name = 'saftytips'   
    
# class PoliceUpdateView(UpdateView):
#     template_name="add_policestation.html"  
#     form_class=PoliceProfileForm
#     model=PoliceProfile  
#     def get_success_url(self):
#         return reverse("adminindex")
@method_decorator(decs,name="dispatch")  
    
class PoliceDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        PoliceProfile.objects.get(id=id).delete()
        return redirect("adminindex")
@method_decorator(decs,name="dispatch")  
   
class PoliceUpdateView(UpdateView):
    template_name="editpolicestation.html"  
    form_class=PoliceProfileForm
    model=PoliceProfile  
    def get_success_url(self):
        return reverse("adminindex")
    
@method_decorator(decs,name="dispatch")  
   
class policestationListView(ListView):
    model = PoliceProfile
    template_name = 'police_list.html'
    context_object_name = 'police'    

  
@never_cache
@login_required
def approve_complaint(request, pk):
    comp = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        comp.status = 'approved'
        comp.save()
        return redirect('policeindex')
    return redirect('complaintlist')  

@method_decorator(decs,name="dispatch")  

class UserComplaintListView(ListView):
    model = Complaint
    template_name = 'complaint_list.html'
    context_object_name = 'complaints'  

    def get_queryset(self):
        qs=Complaint.objects.filter(complainant=self.request.user)
        return qs
    


 
@never_cache
@login_required
def sos_view(request):
    # Here you can add logic to handle the SOS request, like sending notifications or alerts.
    # For demonstration purposes, we'll just return a simple response.
    return HttpResponse("SOS signal sent!")   

 
@never_cache
@login_required
def search_view(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = PoliceProfile.objects.filter(station_name__icontains=query)
            return render(request, 'search_results.html', {'results': results, 'query': query})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})


@method_decorator(decs,name="dispatch")  

class AdminUserListView(ListView):
    template_name="adminuserlist.html"    
    model=UserProfile
    context_object_name="data" 


@never_cache
@login_required 
def view_alerts(request):
    alerts = Alert.objects.all()
    return render(request, 'alerts/view_alerts.html', {'alerts': alerts}) 
   
 
@never_cache
@login_required
def send_alertview(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.save()
            return redirect('alert_sent')
    else:
        form = AlertForm()
    return render(request, 'send_alert.html', {'form': form})

 
@never_cache
@login_required
def alert_sentview(request):
    return render(request, 'alert_sent.html')


@never_cache
@login_required
def view_alertsview(request):
    if request.user.is_staff:
        alerts = Alert.objects.all()
        return render(request, 'view_alerts.html', {'alerts': alerts})
    else:
        return redirect('policeindex')

 
@never_cache
@login_required
def sendmail(request):
    user_location = request.user.user_profile.location
    print(user_location)
    police_profiles = PoliceProfile.objects.filter(police_station_location=user_location)
    for profile in police_profiles:
        police_email = profile.email
        message = f"Hello,\n\n{request.user.username} is in trouble and needs help.\n Here the user location {request.user.user_profile.location}  \n Here the user's guardian's name and phone number {request.user.user_profile.guardian_name}, {request.user.user_profile.guardian_phone} \n Here the user Phone number {request.user.user_profile.phone}  \n\nRegards,\nYour Website Team"
        send_mail(
            "Women Safety",  # Subject
             message,  # Message
            "womensafety33@gmail.com",  # Sender's email
            [police_email],  # Recipient's email
            fail_silently=False,
        )

    return redirect("userindex")



class IndexView(TemplateView):
    template_name="home.html"

 