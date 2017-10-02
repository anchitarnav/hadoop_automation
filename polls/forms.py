from django import forms
from django.conf import settings
import subprocess

def get_my_choices():
    tempfilenames = settings.MEDIA_ROOT+'/'+'tempfilenames'
    filenames = settings.MEDIA_ROOT+'/'+'filenameindex'
    result = subprocess.run(['hadoop','fs','-ls','/'], stdout=subprocess.PIPE)
    f1=open(tempfilenames,'w+')
    f1.write(result.stdout.decode('utf-8'))
    f1.close()
    lines = open(tempfilenames).readlines()
    open(tempfilenames, 'w').writelines(lines[1:])
    with open(tempfilenames) as fp, open (filenames,'w') as newfile:
        for line in fp.read().splitlines():
            reqfile = line.split('/')
            print (reqfile[1])
            newfile.writelines(reqfile[1]+'\n')
    with open(filenames) as fp:
        FILE_NAMES = [(i,i) for i in fp.read().splitlines() ]
        return FILE_NAMES


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['filename_by'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=get_my_choices() )
    JAR_CHOICES = [
        ('hadoop-examples-1.2.1.jar', 'hadoop-examples-1.2.1.jar'),
    ]
    HANDLE_CHOICES = (
    	('wordcount', 'wordcount'),
    )
    #filter_by = forms.ChoiceField(choices = FILTER_CHOICES)
    jar_by = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=JAR_CHOICES)
    handle_by = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=HANDLE_CHOICES)
    #filename_by = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=get_my_choices())
