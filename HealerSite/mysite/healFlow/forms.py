from django import forms


class NameForm(forms.Form):
    name = forms.CharField(label='your_name', max_length=100)
    job = forms.CharField(label='your_name', max_length=100)
    weapon_damage = forms.CharField(label='your_name', max_length=100)
    mind = forms.CharField(label='your_name', max_length=100)
    determination = forms.CharField(label='your_name', max_length=100)


class AbilityForm(forms.Form):
    time = forms.CharField(label='time', max_length=100)
