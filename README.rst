PNWMoths Modifications
======================
This fork has gained some specific modifications for the PNWMoths application.

A csv_file column is populated with the current filename.
Elevation field is converted to ft if an elevation_units column is present
that contains "m".

Django CSV admin
================

The simplest possible tool for uploading, validating, editing, and importing CSV
data into Django models.

Configuring forms for CSV data
------------------------------

CSV data are treated as form data. As such, they need to be validated before
they can be imported into Django models. Define forms to validate your data for
specific content types using the following setting in your Django settings.

::

    CSV_ADMIN_CONTENT_FORMS = {
        ("app_label", "model"): "myapp.forms.MyModelForm"
    }

The key for the ``CSV_ADMIN_CONTENT_FORMS`` dictionary is the natural key
returned by the content type you've associated with your CSV data file. The
value for each key is a Python path string for the form by which your data will
be validated.

Defining forms
--------------

Forms for CSV data validation must be instances of the Django ``Form`` class and
implement a ``save()`` method that stores the resulting database object in the
``instance`` attribute.

Settings
--------------

``CSV_ADMIN_CONTENT_FORMS``
    [type: dictionary] Maps content types to form classes that can be used to
    import CSV data associated with those types. Each key is a natural key for
    the ``ContentType`` model (i.e., an app_label and model tuple). Each value
    is a Python path string to a ``Form`` class or subclass.

``CSV_ADMIN_TEMPLATE``
    [default: "admin/csv_admin/validate_form.html"] Path to a template for the
    validation view. The context includes ``formset``, ``invalid_row_count``,
    ``row_count``, ``too_many_rows``, ``max_invalid_forms``, ``instance``, and
    ``opts``. The default template subclasses Django admin's "change_form.html".

``CSV_ADMIN_USE_TRANSACTIONS``
    [default: ``False``] Indicates whether you want saves to occur within a
    transaction or not. If your database supports transactions, set this to
    ``True``. If this setting is ``False`` and an error occurs during a save,
    the application will try to clean up any previously saved records from that
    request to maintain a consistent database state.
