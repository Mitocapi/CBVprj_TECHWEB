from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from django.shortcuts import render
from django.views.generic.detail import DetailView
from datetime import timezone


# Create your views here.


def benvenuto(request):
    ctx = {"title": "benvenuto"}
    return render(request, template_name="base.html", context=ctx)


def post(request):
    response = "The box, you opened it. <br> I CAME!"
    return HttpResponse(response)


class ListaStudentiView(ListView):
    model = Studente
    template_name = "lista_studenti.html"


class ListaInsegnamentiView(ListView):
    model = Insegnamento
    template_name = "lista_insegnamenti.html"


class ListaInsegnamentiattivi (ListView):
    model = Insegnamento
    template_name = "insegnamenti_attivi.html"

    def get_queryset(self):
        return self.model.objects.exclude(studenti__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = "Insegnamenti Attivi"
        return context


class ListaStudentiIscritti(ListView):
    model = Studente
    template_name= "studenti_iscritti.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titolo"] = "Lista Studenti con Iscrizioni"
        return ctx

    def get_totale_iscrizioni(self):
        count=0
        for i in Insegnamento.objects.all():
            count += i.studenti.all().count()
        return count


class CreateStudenteView(CreateView):
    model = Studente
    template_name = "crea_studente.html"
    fields = "__all__"
    success_url = reverse_lazy("Iscrizioni:listastudenti")


class CreateInsegnamentoView(CreateView):
    model = Insegnamento
    template_name = "crea_insegnamento.html"
    fields = "__all__"
    success_url = reverse_lazy("Iscrizioni:listainsegnamenti")


class DetailInsegnamentoView(DetailView):
    model= Insegnamento
    template_name = "insegnamento.html"


class UpdateInsegnamentoView(UpdateView):
    model = Insegnamento
    template_name = "edit_insegnamento.html"
    fields = "__all__"

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("Iscrizioni:insegnamento", kwargs={'pk': pk})


class DeleteEntityView(DeleteView):
    template_name = "cancella_entry.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        if self.model == Studente:
            entity = "Studente"
        else :
            entity = "Insegnamento"
        ctx["entity"] = entity
        return ctx

    def get_success_url(self):
        if self.model==Studente:
            return reverse("Iscrizioni:listastudenti")
        else:
            return reverse("Iscrizioni:listainsegnamenti")


class DeleteStudentiView(DeleteEntityView):
    model = Studente


class DeleteInsegnamentiView(DeleteEntityView):
    model = Insegnamento


class ListStudenteBySurname(ListaStudentiView):
    def get_queryset(self):
        arg = self.kwargs["surname"]
        qs = self.model.objects.filter(surname__iexact=arg)
        return qs


class ListStudenteByName(ListaStudentiView):
    def get_queryset(self):
        arg = self.kwargs["name"]
        qs = self.model.objects.filter(name__iexact=arg)
        return qs

def CercaStudenteView(request):
    if request.method == "GET" :
        return render(request, template_name="cerca_studente.html")
    else:
        if len(request.POST["name"]) < 1:
            nome = "null"
        else: nome = request.POST["name"]
        if len(request.POST["surname"]) < 1:
            cognome="null"
        else: congnome = request.POST["surname"]
        return redirect("Iscrizioni:studentecercato", name=nome, surname=cognome)


class ListStudenteByNameAndSurname(ListView):
    model = Studente
    template_name="listastudenteinsegnamento.html"

    def get_queryset(self):

        try:
            arg=self.kwargs["name"]
            qs_name = self.model.objects.filter(name__iexact=arg)
        except:
            qs_name=self.model.objects.none()

        try:
            sarg=self.kwargs["surname"]
            qs_surname = self.model.objects.filter(surname__iexact=sarg)
        except:
            qs_surname=self.model.objects.none()

        return (qs_name | qs_surname)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo']= "studenti e loro insegnamenti"
        ls=set()
        for s in self.get_queryset():
            for i in Insegnamento.objects.all():
                if s in i.studenti.all():
                    ls.add(i)

        context['set_ins'] = ls

        return context

