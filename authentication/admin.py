import re

from django.contrib import admin

from authentication.models import User


def is_sha256_hash(text):
    # Check if the text contains 'sha256' substring
    if 'sha256' not in text:
        return False

    # Check if the hash has the expected length and format
    sha256_hash_length = 64  # SHA-256 produces a 64-character hex string
    sha256_hash_pattern = r'[a-fA-F0-9]{64}'  # 64 hex characters

    # Find the portion of the string that could be the SHA-256 hash
    possible_hash = re.search(sha256_hash_pattern, text)

    # If there's a match and the whole possible hash is the correct length, it's likely a SHA-256 hash
    if possible_hash and len(possible_hash.group()) == sha256_hash_length:
        return True

    return False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'mobile_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name', 'mobile_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'mobile_number', 'section')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def save_model(self, request, obj, form, change):
        # Get the password from the form if provided
        password = form.cleaned_data.get('password')
        if password:
            print("Password: ", password)
            if not is_sha256_hash(password):
                print("setting password")
                # If the password is not a hash, hash it
                obj.set_password(password)
            # If the password is already a hash, don't rehash it
            else:
                obj.password = password
        elif 'password' in form.changed_data:
            # If password field is modified but no new password is provided, ignore the password field
            form.cleaned_data.pop('password', None)

        super().save_model(request, obj, form, change)
