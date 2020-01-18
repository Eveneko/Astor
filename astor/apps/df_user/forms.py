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
        if UserInfo.objects.filter(uemail=email).count() > 0:
            raise forms.ValidationError("Email has already been used")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, label='Username')
    password = forms.CharField(max_length=32, label='Password')
    remember_password = forms.ChoiceField(choices=(
                                            ('True', 1),
                                            ('False', 0),
                                        ),
                                        label="Remember me",
                                        initial="True",
                                        widget=forms.widgets.CheckboxInput())

    def clean_username(self):
        # print('cleaned_data:', self.cleaned_data)
        username = self.cleaned_data["username"]
        return username

    def clean_password(self):
        # print('clean_password', self.cleaned_data)
        password = self.cleaned_data["password"]
        return password

    def clean_remember_password(self):
        remember_password = str(self.cleaned_data['remember_password'])
        if remember_password == 'False':
            return False
        elif remember_password == 'True':
            return True
        raise Exception('未知复选结果')

class UserInfoForm(forms.Form):
    # name = forms.CharField(max_length=32)
    uemail = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20)

    # def clean_name(self):
    #     name = self.cleaned_data["name"]
    #     print(name)
    #     if len(name) < 6:
    #         # 没通过检测抛出错误,必须用ValidationError
    #         raise forms.ValidationError("用户名长度不能小于6位")  # 自定义异常
    #     if name.isdigit():
    #         raise forms.ValidationError("用户名不能全为数字")
    #     if UserInfo.objects.filter(uname=name).count() > 0:
    #         raise forms.ValidationError("Username already exists")
    #     return name

    def clean_uemail(self):
        uemail = self.cleaned_data["uemail"]
        # 需要排除本人已经使用的
        if UserInfo.objects.filter(uemail=uemail).count() > 1:
            raise forms.ValidationError("Email has already been used")
        return uemail

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit() or len(phone) != 11:
            raise forms.ValidationError("手机号码格式不对")
        return phone
