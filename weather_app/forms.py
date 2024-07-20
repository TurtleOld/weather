from django import forms


class WeatherForm(forms.Form):
    city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
