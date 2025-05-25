from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import MemberLoginForm, OtpVerificationForm
from Utils import otp_email_send, otp_generator, reg_no_to_email
from .models import Member, Otp
from django.contrib.auth import get_user_model

User = get_user_model()

def student_login_view(request):
    if request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            reg_no = form.cleaned_data['reg_no']
            password = form.cleaned_data['password']
            user = authenticate(request, username=reg_no, password=password)

            if user is not None:
                # otp generate and send
                otp_code = otp_generator.otp_generate()
                otp = Otp.objects.create(otp_code=otp_code, reg_no=reg_no)
                otp.save()

                email = reg_no_to_email.generate_email_from_regno(reg_no)
                if otp_email_send.sendEmail(reg_no, otp_code, email):
                    messages.success(
                        request, "OTP sent to your email. Please check your inbox.")
                    return redirect('otp_verification')
                    
                
                else:
                    messages.error(
                        request, "Failed to send OTP. Please try again later.")
                    return redirect('student_login')

            else:
                messages.error(
                    request, "Invalid registration number or password.")
    else:
        form = MemberLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def otp_verification_view(request):
    if request.method == 'POST':
        form = OtpVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            reg_no = form.cleaned_data['reg_no']

            try:
                otp = Otp.objects.get(otp_code=otp_code, reg_no=reg_no)

                # Log the user in
                user = User.objects.get(reg_no=reg_no)
                login(request, user)

                messages.success(request, "OTP verified successfully.")
                return redirect('student_dashboard')

            except Otp.DoesNotExist:
                messages.error(request, "Invalid OTP. Please try again.")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
    else:
        form = OtpVerificationForm()

    return render(request, 'accounts/otp_verification.html', {'form': form})
@login_required
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        messages.success(request, "Logged out successfully.")
        form = MemberLoginForm()
        # return render(request, 'accounts/login.html', {'form': form})
        return redirect('student_login')
    else:
        messages.error(request, "Invalid request.")
        return redirect('student_login')
    

@staff_member_required
def filter_members(request):
    faculty = request.GET.get('faculty')
    year = request.GET.get('year')

    members = Member.objects.none()
    if faculty and year:
        try:
            year = int(year)
            members = Member.objects.filter(
                faculty=faculty, year_of_study=year)
        except ValueError:
            pass

    return JsonResponse({
        'members': [
            {'id': m.id, 'name': f"{m.firstname} {m.secondname}"} for m in members
        ]
    })
