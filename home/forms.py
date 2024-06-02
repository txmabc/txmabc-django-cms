from django import forms

class ClassifiedsAdminForm(forms.ModelForm): 
 
 
  def __init__(self,*args, **kwargs): 
     super(ClassifiedsAdminForm, self).__init__(*args, **kwargs) 
     self.fields['testujemy'] = forms.CharField(label = "test") 
