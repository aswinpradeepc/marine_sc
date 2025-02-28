from django.contrib import admin

from .models import CommitteeMember, Gallery, Speaker, Sponsor, Faq, Schedule, Committee, OTP, PaperAbstract, Contact, GalleryImage, TravelGrant

admin.site.register(CommitteeMember)
admin.site.register(Speaker)
admin.site.register(TravelGrant)
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

#Gallery
class GalleryImageAdmin(admin.StackedInline):
    model = GalleryImage

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageAdmin]

    class meta:
        model = Gallery
#
# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'subject', 'created_at')
#     search_fields = ('name', 'email', 'subject')
#     list_filter = ('created_at',)