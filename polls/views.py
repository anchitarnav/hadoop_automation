from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess
import datetime
from .forms import FilterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'polls/index.html')
        else:
            return render(request, 'polls/auth.html', {'invalid':'true'})
    return render(request, 'polls/auth.html')

def auth_logout(request):
    logout(request)
    return redirect(auth_login)

@login_required
def index(request):
	template = loader.get_template('polls/index.html')
	context={}
	return HttpResponse(template.render(context,request))

@login_required
def hadoopadmin(request):
    id = request.GET.get('id','')
    useroutput = r'Any required output will be shown here'
    if id == '1':
        result = subprocess.run(['hadoop','dfsadmin','-report'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    if id == '2':
        result = subprocess.run(['hadoop','dfsadmin','-safemode','get'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    if id == '3':
        result = subprocess.run(['hadoop','dfsadmin','-safemode','enter'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    if id == '4':
        result = subprocess.run(['hadoop','dfsadmin','-safemode','leave'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    return render(request, 'polls/hadoopadmin.html', {'useroutput':useroutput})

@login_required
def hadoopfsck(request):
    id = request.GET.get('id','')
    useroutput = r'Any required output will be shown here'
    if id == '1':
        result = subprocess.run(['hadoop','fsck','/','-openforwrite'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    if id == '2':
        result = subprocess.run(['hadoop','fsck','/','-files'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    if id == '3':
        result = subprocess.run(['hadoop','fsck','/','-blocks'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    if id == '4':
        result = subprocess.run(['hadoop','fsck','/','-locations'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    if id == '5':
        result = subprocess.run(['hadoop','fsck','/','-racks'], stdout=subprocess.PIPE)
        useroutput = result.stdout.decode('utf-8').replace('\n','<br>')
    return render(request, 'polls/hadoopfsck.html', {'useroutput':useroutput})

@login_required
def files_add(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = myfile.name + '_' +str(datetime.datetime.now().strftime('%H_%M_%S'))
        file_save = fs.save(filename, myfile)
        #uploaded_file_url = fs.url(filename)
        uploaded_file_url = settings.MEDIA_ROOT+'/'+filename
        p = subprocess.Popen(['hadoop','fs','-put',uploaded_file_url,'/'], stdout=subprocess.PIPE)
        return render(request, 'polls/files_add.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'polls/files_add.html')

@login_required
def files_view(request):
    return render(request, 'polls/files_view.html')

@login_required
def jobview(request):
    return render(request, 'polls/jobview.html')

@login_required
def jobadd(request):
    if request.method == 'POST':
        
        form = FilterForm(request.POST or None)
        jarname = ''
        handlename = ''
        filename = ''
        if form.is_valid():
            jarname = form.cleaned_data.get('jar_by')
            handlename = form.cleaned_data.get('handle_by')
            filename = form.cleaned_data.get('filename_by')
        else:
            jarname = "Form was invalid"

        fullpath = '/usr/share/hadoop/'+jarname
        location = '/'+filename
        output_location = '/output_'+filename+str(datetime.datetime.now().strftime('%H_%M_%S'))
        p = subprocess.Popen(['hadoop','jar',fullpath,handlename,location,output_location], stdout=subprocess.PIPE)
        return render(request, 'polls/jobadd.html', {'form':form,'jarname':jarname,'handlename':handlename,'filename':filename})

    form = FilterForm()
    return render(request, 'polls/jobadd.html', {'form':form})
