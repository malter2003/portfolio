from django.forms import ModelForm
from .models import *

#create class for project form
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields =('title', 'about')

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields =('title', 'contact_email', 'is_active', 'about')        