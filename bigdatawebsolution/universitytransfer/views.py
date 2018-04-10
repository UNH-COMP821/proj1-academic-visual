from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "index.html"

class AboutPageView(TemplateView):
    template_name = "about.html"

# Add this view
class DataPageView(TemplateView):
    def get(self, request, **kwargs):
        # we will pass this context object into the
        # template so that we can access the data
        # list in the template
        context = {
            'data': [
                {
                    'name': 'Celeb 1',
                    'worth': '3567'
                },
                {
                    'name': 'Celeb 2',
                    'worth': '2300'
                },
                {
                    'name': 'Celeb 3',
                    'worth': '1000'
                },
                {
                    'name': 'Celeb 4',
                    'worth': '4567'
                },
                {
                    'name': 'Celeb 5',
                    'worth': '7890'
                },
                {
                    'name': 'Celeb 6',
                    'worth': '12000'
                },
                {
                    'name': 'Celeb 7',
                    'worth': '8960'
                },
                {
                    'name': 'Celeb 8',
                    'worth': '6700'
                }
            ]
        }

        return render(request, 'data.html', context)
