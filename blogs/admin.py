from django.contrib import admin
from .models import Post
from django.contrib.admin import SimpleListFilter


# Register your models here.



class Approve(SimpleListFilter):

    title=('Title name')

    parameter_name='Approved'

    def lookups(self,request,model_admin):
        return (
            (
                (True,('All Approved')),
                (False,('A')))
        )


    def queryset(self,request,queryset):
        if self.value()==True:
            queryset=queryset.filter(Approved=True)
            return queryset.filter(Approved=True)
        elif self.value()==False:
            return queryset.filter(Approved=False)
        else:
            return queryset


class AdminBlog(admin.ModelAdmin):
    list_filter=('Approved','Featured',)
    list_display=( 'Title','Approved','Featured')


admin.site.register(Post,AdminBlog)
