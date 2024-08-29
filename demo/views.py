from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from urllib.request import Request
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
import iclockhelper
from demo.models import (
    Profile,
    ProfileLogs
)
from demo.serializers import (
    GetProfileRequestSerializer,
    GetProfileResponseSerializer
)


@api_view(['GET', 'POST'])
def print_data(request):
    if request.method == 'POST':
        data = request.data
    else:
        data = {}

    query_params = request.query_params

    print(f"Params: {query_params}")
    print(f"Data: {data}")

    response_data = {
        'params': query_params,
        'data': data
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def cdataView(request):
    zk_request = create_request(request)
    cdata_req = iclockhelper.CdataRequest.from_req(zk_request)

    # if cdata_req.table == iclockhelper.TableEnum.attlog:
    print("Attendance Log Entry:", cdata_req)

    return HttpResponse('OK')


@api_view(['POST'])
def fdataView(request):
    return HttpResponse('OK')


@api_view(['GET'])
def getreqView(request):
    zk_request = create_request(request)
    get_req = iclockhelper.GetRequest.from_req(zk_request)
    # print("getview", get_req)
    return HttpResponse('OK', status=200)


@api_view(['POST'])
def devpostView(request):
    return HttpResponse('OK')


def create_request(req) -> iclockhelper.Request:
    return iclockhelper.Request(
        headers=req.headers,
        method=req.method,
        url=req.build_absolute_uri(),
        data=req.body,
    )


@api_view(['GET'])
def get_profile(request):
    request_serializer = GetProfileRequestSerializer(data=request.query_params)
    if request_serializer.is_valid():
        employee_id = request_serializer.validated_data.get('employee_id')
        profile = Profile.objects.get(employee_id=employee_id)

        entry_log = ProfileLogs.objects.filter(
            profile_id=profile.id, log_type='1'
        ).order_by('created').first()
        exit_log = ProfileLogs.objects.filter(
            profile_id=profile.id, log_type='2'
        ).order_by('created').first()

        if entry_log and exit_log:
            time_difference = exit_log.log_timestamp - entry_log.log_timestamp
            hours = time_difference.seconds // 3600
            minutes = (time_difference.seconds % 3600) // 60
            seconds = time_difference.seconds % 60
            time_difference_formatted = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            time_difference_formatted = None

        entry_log_time = entry_log.log_timestamp.strftime(
            '%Y-%m-%d %H:%M:%S'
        ) if entry_log else None
        exit_log_time = exit_log.log_timestamp .strftime(
            '%Y-%m-%d %H:%M:%S'
        ) if exit_log else None

        response_data = {
            "id": profile.id,
            "employee_id": profile.employee_id,
            "name": profile.name,
            "email": profile.email,
            "entry_log_time": entry_log_time if entry_log_time else None,
            "exit_log_time": exit_log_time if exit_log_time else None,
            "time_difference": (
                time_difference_formatted
            ) if time_difference_formatted else None,
        }
        response_serializer = GetProfileResponseSerializer(response_data)
        return Response(response_serializer.data,
                        status=status.HTTP_200_OK)
    return Response(request_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def cdataView(request):
#     zk_request = create_request(request)
#     cdata_req = iclockhelper.CdataRequest.from_req(zk_request)

#     if cdata_req.attendance_log and cdata_req.attendance_log.transactions:
#         for transaction in cdata_req.attendance_log.transactions:
#             if transaction.pin:
#                 if cdata_req.sn == 'TDBD240400216':
#                     log_type = '1'
#                 elif cdata_req.sn == 'TDBD240400215':
#                     log_type = '2'
#                 else:
#                     log_type = '0'

#                 profile, created = Profile.objects.get_or_create(
#                     employee_id=transaction.pin,
#                 )

#                 ProfileLogs.objects.create(
#                     profile_id=profile,
#                     log_type=log_type,
#                     log_timestamp=transaction.server_datetime
#                 )


#     return HttpResponse('OK')


# @api_view(['POST'])
# def getreqView(request):
#     zk_request = create_request(request)
#     get_req = iclockhelper.GetRequest.from_req(zk_request)

#     return HttpResponse('OK', status=200)


# @api_view(['POST'])
# def fdataView(request):
#     return HttpResponse('OK')


# @api_view(['POST'])
# def devpostView(request):
#     return HttpResponse('OK')


# def create_request(req) -> iclockhelper.Request:
#     return iclockhelper.Request(
#         headers=req.headers,
#         method=req.method,
#         url=req.build_absolute_uri(),
#         data=req.body,
#     )
