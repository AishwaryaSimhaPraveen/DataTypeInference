from django.http import JsonResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .data_type_inference import infer_data_types  # Import your data type script
from .models import ProcessedData
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@csrf_exempt  # Consider using CSRF tokens for production
def handle_file_upload(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        file = request.FILES['file']

        try:
            result = infer_data_types(file)  # Call your data type inference function

            # Save the processed data to the database
            for item in result:  # item should be dict with column_name and inferred_data_type
                ProcessedData.objects.create(
                    column_name=item['column_name'], 
                    inferred_data_type=item['inferred_data_type']
                )

            # Return JSON response instead of rendering HTML for React
            return JsonResponse(result, safe=False)

        except Exception as e:
            logger.error(f"Error processing file: {e}")  # Log the error
            return JsonResponse({'error': f"Error processing file: {e}"}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
