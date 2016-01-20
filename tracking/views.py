from django.shortcuts import render
from django.shortcuts import get_object_or_404 as get_or_404

from django.http import HttpResponse as httpresp
from django.http import HttpResponseRedirect as httprespred

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Block
from .models import DrawingStatus
from .models import Department
from .models import Drawing
from .models import Revision
from .models import Comment
from .models import Reply

from .forms import SearchForm

def _get_username(request):
    if request.user.is_authenticated():
        username = request.user
    else:
        username = None

    return username


def logout_view(request):
    username = request.user
    logout(request)
    return httpresp('''Goodbye {} !<br>
                    You\'ve successfully logged out!<br>
                    <a href="/">return to homepage</a>'''.format(username))


@login_required(login_url='/accounts/login')
def index(request):
    username = _get_username(request)
    return render(request, 'tracking/index.html', {'username':username})
    # return httpresp('Welcome to DRC tracking index')



### Drawing Search ###
def _pull_drawings(formdat):
    if not formdat['drawing_name']:
        return None
    qstr = '^{}$'.format(formdat['drawing_name'].replace('*','.*'))
    dquery = Drawing.objects.filter(name__regex=qstr)
    return dquery

@login_required(login_url='/accounts/login')
def drawing_search(request):
    username = _get_username(request)
    drawings = False
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            drawings = _pull_drawings(form.cleaned_data)

    else:
        form = SearchForm()

    context = {'username':username, 'form':form.as_table(), 
               'drawings':drawings}
    if drawings != False:
        return render(request, 'tracking/drawing_results.html', context)
    return render(request, 'tracking/drawing_search.html', context)


@login_required(login_url='/accounts/login')
def drawing_detail(request, drawing_name):
    info = Drawing.objects.get(name=drawing_name.lower())
    attch = info.get_attachments()
    drawing = {'name':drawing_name, 'desc':info.desc, 'phase':info.phase,
               'received':info.received, 'status':info.status.status,
               'expected':info.expected, 'dep':info.department.name,
               'disc':info.discipline.name, 'kind':info.kind.name,
               'attachments':attch if attch else 'None'}
    context = {'drawing':drawing}
    return render(request, 'tracking/drawing_detail.html', context)
    # return httpresp('detail for {}<br/><br/>{}'\
    #                 .format(drawing_name, 
    #                         [info.desc,
    #                                    info.phase,
    #                                    info.block.name,
    #                                    info.status.status,
    #                                    info.department.name,
    #                                    info.discipline.name,
    #                                    info.kind.name,
    #                                    info.expected]))


@login_required(login_url='/accounts/login')
def attachment(request, file_name):
    pass

# def detail_pdf(request, question_id):
#     try:
#         #question = Question.objects.all().exclude(pdf__endswith='file.pdf')
#         question = Question.objects.get(pk=question_id)
#         if question.pdf != '':
#             filepath = question.pdf
#         else:
#             raise http404('No drawing for question: {}'.format(question.question_text))
#     except Question.DoesNotExist:
#         raise http404('Question does not exist')

#     with open(str(filepath), 'rb') as pdffile:
#         response = httpresp(pdffile.read(), content_type='application/pdf')
#         response['Content-Disposition'] = 'filename=file.pdf'
#         return response
#     #return httpresp(file.read()