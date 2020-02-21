from django import forms



class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    fullname = forms.CharField(max_length=30)
    email = forms.EmailField()
    content = forms.CharField(label='', widget=forms.Textarea)
