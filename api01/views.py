from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


@api_view(['POST'])
def submit_resume(request):
    """ Submit trace """
    data = JSONParser().parse(request)
    return JsonResponse(data, status=200, safe=False)
    # serializer = TraceSerializer(data=data)
    # if serializer.is_valid():
    #    serializer.save()
    #    return JsonResponse(serializer.data, status=201)
    # else:
    #    return JsonResponse(serializer.errors, status=400)
