from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import *
from .utils import comma_split


class BootstrapHelperForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ["CheckboxInput", "ClearableFileInput", "FileInput"]
        for field in self.fields:
            widget_name = self.fields[field].widget.__class__.__name__
            if widget_name.startswith("Select"):
                self.fields[field].widget.attrs.update(
                    {"class": "simple-select2 w-100"}
                )
            elif widget_name not in fields:
                self.fields[field].widget.attrs.update({"class": "form-control"})


class StaffForm(BootstrapHelperForm, ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"
        exclude = ["user", "storage"]


class AuthorForm(BootstrapHelperForm, ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class ImportForm(BootstrapHelperForm, ModelForm):
    book = forms.ModelChoiceField(
        queryset=Traditional.objects.all().order_by("book__name")
    )

    class Meta:
        model = Import
        fields = ("book", "quantity")


class ExportForm(BootstrapHelperForm, ModelForm):
    book = forms.ModelChoiceField(
        queryset=Traditional.objects.all().order_by("book__name")
    )

    class Meta:
        model = Export
        fields = ("book", "quantity")


class ErrorPaymentForm(BootstrapHelperForm, ModelForm):
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Payment
        fields = ("status", "reason")


class BookForm(BootstrapHelperForm, ModelForm):
    topics = forms.CharField(label="Thể loại", required=True)
    keywords = forms.CharField(label="Từ khóa", required=True)
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all().order_by("name")
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all().order_by("name")
    )

    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            self.fields["topics"].initial = ", ".join(
                x.name for x in instance.topic_set.all()
            )
            self.fields["keywords"].initial = ", ".join(
                x.keyword for x in instance.keyword_set.all()
            )

    def save_extra(self, book):
        topic_list = comma_split(self.cleaned_data.get("topics"))
        keyword_list = comma_split(self.cleaned_data.get("keywords"))

        Topic.objects.filter(book=book).exclude(name__in=topic_list).delete()
        Keyword.objects.filter(book=book).exclude(keyword__in=keyword_list).delete()

        list(
            map(
                lambda topic: Topic.objects.get_or_create(book=book, name=topic),
                topic_list,
            )
        )
        list(
            map(
                lambda keyword: Keyword.objects.get_or_create(
                    book=book, keyword=keyword
                ),
                keyword_list,
            )
        )
