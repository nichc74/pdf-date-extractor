from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View

import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from extractor.utils import extract_dates

@method_decorator(csrf_exempt, name='dispatch')
class ExtractorView(View):
    def post(self, request):
        print(request)
        test_string = "checking for the date: 10-10-2020 and I hope it works"
        result = extract_dates(test_string)
        # decode the data
        # data = json.loads(request.body.decode("utf-8"))
        # import pprint
        # pprint.pprint(data)

        # name = data.get('name')
        # price = data.get('price')
        # quantity = data.get('quantity')

        # product = Product.objects.create(name=name, price=price, quantity=quantity)
        
        return_data = {
            'message': 'You are pinging the proper view',
            'result': result
        }

        return JsonResponse(return_data, status=201)


def index():
    return HttpResponse('Hello World!')
