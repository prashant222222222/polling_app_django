from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
)

from django.views.generic.detail import SingleObjectMixin
from main import models, forms

from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.
# mixim donot handle views , it handles data of single object


class Index(ListView):
    model = models.Question
    template_name = 'main/index.html'
    #context_object_name = 'question_list'
    # default context name for
    # list view is - model_name(lowercase)_list


# we want to store information so form view
class Question(PermissionRequiredMixin, SingleObjectMixin, FormView):
    # singleobjectmixin or any mixin ddoesnot support rendering view so use basedetailview
    model = models.Question
    template_name = 'main/question.html'
    form_class = forms.AnswerForm
    permission_required = 'can_add_answer'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['answer'] = models.Answer.objects.get(
            question=self.get_object(),
            user=self.request.user
        )
        return data

    # def form_invalid(self, form):
    #     obj = form.save(commit=False)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.question = self.get_object()
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

        # return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
