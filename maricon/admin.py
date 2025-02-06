from django.contrib import admin
from .models import CommitteeMember, Gallery, Speaker, Sponsor, Faq, Schedule, Committee, OTP, PaperAbstract, Contact

admin.site.register(CommitteeMember)
admin.site.register(Gallery)
# admin.site.register(Sponsor)
# admin.site.register(Faq)
# admin.site.register(Schedule)


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp', 'created_at')


@admin.register(PaperAbstract)
class PaperAbstractAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'created_at','presentation')
    search_fields = ('title', 'authors')
    list_filter = ('created_at', 'theme','presentation')

class SpeakerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            old_order = form.initial['order']
        else:
            old_order = None
        all_speakers = list(Speaker.objects.all().order_by('order'))
        if old_order != obj.order:
            all_speakers = [speaker for speaker in all_speakers if speaker.id != obj.id]
            all_speakers.insert(obj.order - 1, obj)
            for index, speaker in enumerate(all_speakers):
                speaker.order = index + 1
                speaker.save()
        super().save_model(request, obj, form, change)

admin.site.register(Speaker, SpeakerAdmin)

#
# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'subject', 'created_at')
#     search_fields = ('name', 'email', 'subject')
#     list_filter = ('created_at',)