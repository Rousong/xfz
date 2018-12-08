from django import forms
from apps.forms import FormMixin
from news.models import News, Banner
from course.models import Course


class EditNewsCategory(forms.Form, FormMixin):
    pk = forms.IntegerField()
    name = forms.CharField(max_length=10)


class WriteNewsForm(forms.ModelForm, FormMixin):
    category_pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time', 'updated_time',
                   'is_deleted']


class AddBannerForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Banner
        fields = ('priority', 'image_url', 'link_to')


class PubCourseForm(forms.ModelForm, FormMixin):
    category_pk = forms.IntegerField()
    teacher_pk = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ('category', 'teacher', 'pub_time', 'updated_time',
                   'is_deleted')
