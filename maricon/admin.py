from django.contrib import admin

from .models import CommitteeMember, Gallery, Speaker, Sponsor, Faq, Schedule, Committee, OTP, PaperAbstract, Contact, GalleryImage, TravelGrant, AccommodationApplication


admin.site.register(CommitteeMember)
admin.site.register(AccommodationApplication)
admin.site.register(Speaker)
admin.site.register(TravelGrant)
# admin.site.register(Sponsor)
# admin.site.register(Faq)
# admin.site.register(Schedule)
from import_export.admin import ExportMixin
from import_export import resources, fields, widgets




@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp', 'created_at')




class PaperResource(resources.ModelResource):

    user_email = fields.Field(
        attribute='user',
        column_name='user_email',
        widget=widgets.CharWidget()
    )
    def dehydrate_abstract(self, paper):
        return f"https://icmbgsd25.cusat.ac.in/media/{paper.file}"

    def dehydrate_user_email(self, paper):
        return paper.user.email if paper.user else "No User"

    class Meta:
        model = PaperAbstract
        fields = ['title', 'authors', 'user_email', 'abstract',
                  'keywords', 'organization', 'theme', 'presentation']



@admin.register(PaperAbstract)
class PaperAbstractAdmin(ExportMixin,admin.ModelAdmin):
    list_display = ('title', 'authors', 'created_at','presentation')
    search_fields = ('title', 'authors')
    list_filter = ('created_at', 'theme','presentation')
    resource_classes = [PaperResource]


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