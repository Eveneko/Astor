from django import forms


class LikeForm(forms.Form):
    good_id = forms.IntegerField()
    like = forms.ChoiceField(choices=
                             (('True', 1),
                              ('False', 0),
                              ),
                             label="like",
                             initial="True",
                             widget=forms.widgets.CheckboxInput())

    def clean_good_id(self):
        good_id = int(self.cleaned_data['good_id'])
        return good_id

    def clean_like(self):
        like = str(self.cleaned_data['like'])
        if like == 'False':
            return False
        elif like == 'True':
            return True
        raise Exception('未知复选结果')