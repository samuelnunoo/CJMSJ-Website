from django.shortcuts import render
from dal import autocomplete
from blogs.forms import PostForm
from users.models import Profile
import re


class ProfileAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Profile.objects.none()

        qs = Profile.objects.all()
        print(qs)


        if self.q:

            qs_id=[Profile.id for Profile in Profile.objects.all() if re.match(self.q, Profile.name(),re.IGNORECASE)] #To ignore case do re.IGNORECASE
            qs=qs.filter(id__in=qs_id)

        return qs

    def get_result_label(self,item):
        return item.name()

    def get_selected_result_label(self, result):
        return result.name()





def submission_form(request):
    return render(request, 'submissions/new-submissions.html', {'form': PostForm})
