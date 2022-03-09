from django.contrib import admin
from .models import UserModel, MovieModel, TvModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    fieldsets =(
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'email')}),
        (_('Permission'), {'fields': ('is_superuser',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (_('Personal Info'), {'fields': ('name', 'email',)}),
        (_('Permission'), {'fields': ('is_superuser',)}),
    )

    list_display = ('id', 'email', 'name', 'username',)
    list_filter = ('is_superuser',)
    filter_horizontal = ()
    search_fields = ('email', 'name', 'username')
    ordering = ('name',)


@admin.register(MovieModel)
class MovieAdmin(BaseUserAdmin):
    fieldsets =(
        (None, {'fields': ('id', 'title')}),
        (_('Data'), {'fields': ('overview', 'genres', 'tagline', )}),
    )

    # add_fieldsets = (
    #     (None, {'fields': ('username', 'password1', 'password2')}),
    #     (_('Personal Info'), {'fields': ('name', 'email',)}),
    # )

    list_display = ('id', 'title',)
    list_filter = ()
    filter_horizontal = ()
    search_fields = ('title', )
    ordering = ('-popularity',)

@admin.register(TvModel)
class MovieAdmin(BaseUserAdmin):
    fieldsets =(
        (None, {'fields': ('id', 'title')}),
        (_('Data'), {'fields': ('overview', 'genres', 'tagline', )}),
    )

    # add_fieldsets = (
    #     (None, {'fields': ('username', 'password1', 'password2')}),
    #     (_('Personal Info'), {'fields': ('name', 'email',)}),
    # )

    list_display = ('id', 'title',)
    list_filter = ()
    filter_horizontal = ()
    search_fields = ('title', )
    ordering = ('title', )

