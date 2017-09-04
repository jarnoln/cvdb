import json
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .create_resume import create_resume


@api_view(['POST'])
def submit_resume(request):
    """ Submit resume """
    data = JSONParser().parse(request)
    response = create_resume(data, request.user)
    return response


@api_view(['POST'])
def submit_resume_file(request):
    """ Submit resume """
    resume_file = request.FILES['json_file']
    # print('resume file=%s' % resume_file)
    file_content = resume_file.read()
    data = json.loads(file_content.decode('utf-8'))
    response = create_resume(data, request.user)
    return response
