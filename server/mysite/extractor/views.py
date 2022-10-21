import io

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage


from PyPDF2 import PdfFileReader
from extractor.utils import extract_dates, norm_cal_data


@method_decorator(csrf_exempt, name='dispatch')
class ExtractorView(View):
    def post(self, request):
        log_of_extracted_dates = {}
        pdf_files_uploaded = request.FILES

        pdf_keys = pdf_files_uploaded.keys()
        # Process individual pdf docs
        for pdf_key in pdf_keys:
            # Setup PDF Reader
            pdf = pdf_files_uploaded[pdf_key]
            pdfFileObj = pdf.read()
            pdfReader = PdfFileReader(io.BytesIO(pdfFileObj))

            # Store in FileSystemStorage
            file_storage = FileSystemStorage()
            file_storage_save = file_storage.save(pdf.name, pdf)
            file_url = request.build_absolute_uri(
                '/')[:-1] + file_storage.url(file_storage_save)

            dates_for_curr_pdf = {}
            # Process individual pdf pages
            for i in range(pdfReader.numPages):
                curr_page = pdfReader.pages[i].extract_text()
                extract_dates(pdf.name, curr_page,
                              dates_for_curr_pdf, file_url)

            if dates_for_curr_pdf:
                log_of_extracted_dates.update(dates_for_curr_pdf)

        return_data = {
            'message': 'You are pinging the proper view',
            'log_of_extracted_dates': norm_cal_data(log_of_extracted_dates)
        }

        return JsonResponse(return_data, status=201)
