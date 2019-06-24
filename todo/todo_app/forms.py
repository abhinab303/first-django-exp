from django import forms

class InviteForm(forms.Form):
    user_id = forms.IntegerField()
