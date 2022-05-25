from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ResolveNumberPlateForm
from .service import resolve_number


class ResolveNumberPlateView(TemplateView):
    template_name = 'resolve_number_plate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResolveNumberPlateForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ResolveNumberPlateForm(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            image_name = fs.save(image.name, image)
            path = fs.path(image_name)
            context = resolve_number(path)
        context['form'] = form
        return render(request, self.template_name, context)
