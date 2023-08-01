from django.contrib import admin
from django.apps import apps

# Register your models here.

#Register all other models
class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        #field = super(model, self).formfield_for_choice_field(db_field, request, **kwargs)
        #field.widget.attrs['size'] = '25'
        super(ListAdminMixin, self).__init__(model, admin_site)



models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})

    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        # admin.site.unregister(model)
        pass
