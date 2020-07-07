from django import forms

class CreateForm(forms.Form):
    title = forms.CharField(label="Entry title")
    text = forms.CharField(label="Markdown content for the page", widget=forms.Textarea(attrs={"rows":5, "cols":20}))

class EditForm(forms.Form):
    text = forms.CharField(label="Edit the entry's Markdown content", widget=forms.Textarea())