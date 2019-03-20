from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from django.forms.models import BaseInlineFormSet


CollectionTitleChildFormSet = inlineformset_factory(
    CollectionTitle, CollectionTitleChild,
    fields=['name', 'language'], extra=2, can_delete=True
    )


class BaseTitleChildFormset(BaseInlineFormSet):
    
    def add_fields(self, form, index):
        super(BaseTitleChildFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = CollectionTitleChildFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix='child-%s-%s' % (form.prefix, CollectionTitleChildFormSet.get_default_prefix()))

    def is_valid(self):
        result = super(BaseTitleChildFormset, self).is_valid()
        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
        return result

    def save(self, commit=True):
        result = super(BaseTitleChildFormset, self).save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)
        return result


class CollectionTitleForm(forms.ModelForm):

    class Meta:
        model = CollectionTitle
        exclude = ()

# CollectionTitleFormSet = inlineformset_factory(
#     Collection, CollectionTitle, form=CollectionTitleForm,
#     fields=['name', 'language'], extra=1, can_delete=True
#     )

CollectionTitleFormSet = inlineformset_factory(
    Collection, CollectionTitle, form=CollectionTitleForm,
    formset=BaseTitleChildFormset,
    fields=['name', 'language'], extra=1, can_delete=True)



class CollectionForm(forms.ModelForm):

    class Meta:
        model = Collection
        exclude = ['created_by', ]

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('subject'),
                Field('owner'),
                Fieldset('Add titles',
                    Formset('titles')),
                Field('note'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
                )
            )
