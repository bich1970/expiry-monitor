# Create your views here.
from django.shortcuts import render, redirect
from .forms import UploadExcelForm
from .models import ExcelFile
from .utils import process_all_data

# views.py
def upload_file(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            ExcelFile.objects.filter(file=uploaded_file.name).delete()  # Optional: Clean DB record
            ExcelFile(file=uploaded_file).save()  # Save with original name
            return redirect('analyzer:dashboard')
    else:
        form = UploadExcelForm()
    return render(request, 'upload.html', {'form': form})


def dashboard(request):
    try:
        context = process_all_data()
        if 'summary_table' not in context:
            context['summary_table'] = "<p style='color:red;'>No data available.</p>"
    except Exception as e:
        context = {
            'summary_table': f"<p style='color:red;'>Dashboard error: {str(e)}</p>"
        }
    return render(request, 'dashboard.html', context)

