import io

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from PyPDF2 import PdfFileReader
from extractor.utils import extract_dates, massage_calendar_dates

@method_decorator(csrf_exempt, name='dispatch')
class ExtractorView(View):
    def post(self, request):
        log_of_extracted_dates = {}
        pdf_files_uploaded = request.FILES

        pdf_keys = pdf_files_uploaded.keys()
        for pdf_key in pdf_keys:
            # Setup PDF Reader
            pdf = pdf_files_uploaded[pdf_key]
            pdfFileObj = pdf.read()
            pdfReader = PdfFileReader(io.BytesIO(pdfFileObj))

            dates_for_curr_pdf = {}
            # Query through individual pdf pages
            for i in range(pdfReader.numPages):
                curr_page = pdfReader.pages[i].extract_text()
                extract_dates(pdf.name, curr_page, dates_for_curr_pdf)

            # After going through whole pdf document we want to update master log
            if dates_for_curr_pdf:
                log_of_extracted_dates.update(dates_for_curr_pdf)

        print(log_of_extracted_dates)

        return_data = {
            'message': 'You are pinging the proper view',
            'log_of_extracted_dates': massage_calendar_dates(log_of_extracted_dates)
        }

        return JsonResponse(return_data, status=201)

