import csv

from django.conf import settings
from django.conf.urls.defaults import patterns
from django.contrib import admin
from django.core.urlresolvers import get_callable
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import CsvFile


class CsvFileAdmin(admin.ModelAdmin):
    list_display = ("csv", "added_on")

    class Meta:
        css = {"all": "csv/style.css"}

    def get_urls(self):
        urls = super(CsvFileAdmin, self).get_urls()
        csv_urls = patterns("",
            (r'^(?P<object_id>\d+)/validate/$', self.admin_site.admin_view(self.validate_view))
        )
        return csv_urls + urls

    def validate_view(self, request, object_id, extra_context=None):
        context = {}
        if extra_context is not None:
            context.update(extra_context)

        instance = self.get_object(request, object_id)
        content_type_key = instance.content_type.natural_key()
        context["instance"] = instance
        context["app_label"] = instance._meta.app_label
        context["opts"] = instance._meta

        if (hasattr(settings, "CSV_ADMIN_CONTENT_FORMS") and
            content_type_key in settings.CSV_ADMIN_CONTENT_FORMS):
            # Look up the form path for this file's content type.
            form_path = settings.CSV_ADMIN_CONTENT_FORMS.get(content_type_key)
            form_class = get_callable(form_path)
            reader = csv.DictReader(instance.csv)

            initial_data = []
            rows = 0
            invalid_rows = 0
            for row in reader:
                rows += 1
                form_instance = form_class(row)
                if form_instance.is_valid():
                    # Ignore valid forms for now.
                    pass
                else:
                    initial_data.append(row)
                    invalid_rows += 1

            # One or more rows contain invalid data.
            if invalid_rows > 0:
                # Create a form class with one form for each invalid row.
                formset_class = formset_factory(form_class, extra=0)

                if request.method == "POST":
                    formset = formset_class(request.POST, request.FILES)
                else:
                    formset = formset_class(initial=initial_data)

                if formset.is_valid():
                    # Save all forms.
                    pass
                else:
                    # Display remaining errors.
                    #raise Exception(formset.errors)
                    pass
            else:
                # All rows are valid. Save all forms.
                pass

            context["formset"] = formset
            context["rows"] = rows
            context["invalid_rows"] = invalid_rows
        else:
            self.message_user(
                request,
                """Set a form for the content type "%s" in the Django
                CSV_ADMIN_CONTENT_FORMS setting.""" % instance.content_type
            )

        # TODO: allow the user to specify their own template.
        return render_to_response("admin/csv_admin/validate_form.html",
                                  context,
                                  context_instance=RequestContext(request))

admin.site.register(CsvFile, CsvFileAdmin)
