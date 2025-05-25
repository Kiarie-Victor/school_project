from django import forms

class MemberLoginForm(forms.Form):
    reg_no = forms.CharField(max_length=100, label='Registration Number',  widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Registration Number',
    }))

    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))


class OtpVerificationForm(forms.Form):
    reg_no = forms.CharField(label='Registration Number', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Registration Number',
    }))

    otp_code = forms.CharField(label='OTP Code', max_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter OTP Code',
    }))


