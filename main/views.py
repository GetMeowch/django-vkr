from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .checklabs import check_on_properties

def index(request):
    if request.method == 'POST' and 'uploadfileinput' in request.FILES:
        files = request.FILES.getlist('uploadfileinput')
        fs = FileSystemStorage()
        for f in files:
            print(f.name)
            fs.save(f.name, f)
        folder = fs.location
        print(folder)
        font = request.POST.get("select_font", False)
        alignment = request.POST.get("select_alignment", False)
        interval = request.POST.get("select_interval", False)
        fontSize = request.POST.get("select_font_size", False)
        indFirst = request.POST.get("indent_of_first_line", False)
        indLeft = request.POST.get("indent_of_left", False)
        indRight = request.POST.get("indent_of_right", False)
        file_name, is_zip = check_on_properties(folder, font, int(alignment), float(interval), int(fontSize), float(indFirst), float(indLeft), float(indRight))
        file_url = fs.url(file_name)
        if is_zip:
            load_text = ".zip архив"
        else:
            load_text = ".docx файл"
        return render(request, "main/index.html", {
            'file_url': file_url,
            'load_text': load_text
        })
    return render(request, "main/index.html")