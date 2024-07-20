from django import forms


class WeatherForm(forms.Form):
    city = forms.CharField(
        label="Введите название города:",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
