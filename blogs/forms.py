from django import forms
from .models import Post
from PIL import Image
from ckeditor.widgets import CKEditorWidget
from dal import autocomplete
from users.models import Profile







class PostForm(forms.ModelForm):

    '''x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    '''
    Profiles = forms.ModelChoiceField(queryset=Profile.objects.all().filter(complete=True).filter(email_confirmed=True),
                                      widget=autocomplete.ModelSelect2Multiple(url='profile-autocomplete'))

    class Meta:
        model=Post
        Content=forms.CharField(widget=CKEditorWidget())



        fields=('Title','Image','Content','Description','Profiles') #,'x','y','width','height',
        widgets={

            'Title':forms.TextInput( attrs={'style':"border:none; color:black; font-size:2em;", 'placeholder':'Page Title'}),
            'Image':forms.FileInput(attrs={'accept':'image/*'}),
            'Content':forms.Textarea(attrs={'style':'border:none',}),
            'Description': forms.Textarea(attrs={'cols':100,'rows':4,'style':'resize: none; width:100%;'}),

        }




