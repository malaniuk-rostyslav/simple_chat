from django.contrib import admin
from .models import Thread, Message
from django import forms


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sender":
            thread_id = request.resolver_match.kwargs.get('object_id')
            if thread_id:
                thread = Thread.objects.get(pk=thread_id)
                kwargs["queryset"] = thread.participants.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ThreadAdminForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'

    def clean_participants(self):
        participants = self.cleaned_data['participants']
        if len(participants) > 2:
            raise forms.ValidationError('A Thread can have only up to 2 participants.')
        return participants


class ThreadAdmin(admin.ModelAdmin):
    form = ThreadAdminForm
    list_display = ('id', 'created', 'updated')
    inlines = [MessageInline]
    readonly_fields = ('created', 'updated') 


admin.site.register(Thread, ThreadAdmin)