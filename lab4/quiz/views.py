from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam
from .forms import QuestionForm, ChoiceFormSet


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, "quiz/exam_list.html", {"exams": exams})


def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, "quiz/exam_detail.html", {"exam": exam})


def create_question_view(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            question = form.save()
            formset.instance = question
            formset.save()
            return redirect("exam_list")
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()

    return render(
        request, "quiz/question_form.html", {"form": form, "formset": formset}
    )