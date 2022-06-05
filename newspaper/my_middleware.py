

class ChoiceGadgetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        if request.gadget == 'mobile':
            prefix = '/mobile'
        elif request.gadget == 'pk':
            prefix = '/pk'
        response.template_name = prefix + response.template_name
        return response