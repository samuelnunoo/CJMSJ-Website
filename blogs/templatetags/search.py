from django import template
from django.shortcuts import redirect
register=template.Library()

@register.simple_tag
def search(query):
    if query==None:
        return
    else:
        print("query1",query,"query2",)
        #return redirect("/blogs/?q={}".format(query))