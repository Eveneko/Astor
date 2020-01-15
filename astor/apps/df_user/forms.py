from django import forms
from .models import UserInfo


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32, label='Username')
    password = forms.CharField(max_length=32, label='Password')
    confirm_pwd = forms.CharField(max_length=32, label='Confirm Password')
    email = forms.EmailField(label='Email')

    def clean_username(self):
        # print('cleaned_data:', self.cleaned_data)
        username = self.cleaned_data["username"]
        if len(username) < 6:
            # 没通过检测抛出错误,必须用ValidationError
            raise forms.ValidationError("用户名长度不能小于6位")  # 自定义异常
        if username.isdigit():
            raise forms.ValidationError("用户名不能全为数字")
        if UserInfo.objects.filter(uname=username).count() > 0:
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password(self):
        # print('clean_password', self.cleaned_data)
        password = self.cleaned_data["password"]
        return password

    def clean_confirm_pwd(self):
        # print('clean_confirm_pwd', self.cleaned_data)
        confirm_pwd = self.cleaned_data["confirm_pwd"]
        if confirm_pwd != self.cleaned_data["password"]:
            raise forms.ValidationError("两次密码不一致")
        return confirm_pwd

    def clean_email(self):
        # print('clean_email', self.cleaned_data)
        email = self.cleaned_data["email"]
        return email
