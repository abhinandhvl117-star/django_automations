from django.shortcuts import render, redirect
from .utils import check_csv_error, get_all_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages
from .tasks import import_data_task

def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(
            file=file_path,
            model_name=model_name
        )

        absolute_path = upload.file.path

        try:
            check_csv_error(absolute_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        import_data_task.delay(absolute_path, model_name)
                
        # showing success message
        messages.success(request, "Import was success, we will notify you once its done.")  
        
        return redirect('import_data')
    else:
        custom_models = get_all_models()
        context = {
            'custom_models': custom_models
        }
        
    return render(request, 'dataentry/importdata.html', context)
