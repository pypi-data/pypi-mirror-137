from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from sitelfl.models.recreated_urls import Recreated_urls


@JsonResponseWithException()
def Recreated_urls_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Recreated_urls.objects.
                select_related().
                get_range_rows1(
                request=request,
                # function=Recreated_urlsManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Recreated_urls_Add(request):
    return JsonResponse(DSResponseAdd(data=Recreated_urls.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Recreated_urls_Update(request):
    return JsonResponse(DSResponseUpdate(data=Recreated_urls.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Recreated_urls_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Recreated_urls.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Recreated_urls_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Recreated_urls.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Recreated_urls_Info(request):
    return JsonResponse(DSResponse(request=request, data=Recreated_urls.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Recreated_urls_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Recreated_urls.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
