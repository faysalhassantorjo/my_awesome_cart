from django.http import HttpResponse
def my_middleware(get_response):
    print("One time initial")
    def before(request):
        print("Before view")
        response = get_response(request)
        print("After view")
        return response
    return before


#that was function based middleware
class MiddleWare:
    def __init__(self,get_response):
        self.get_response = get_response
        print("One time initial Classssssssssss")

    def __call__(self,request):
        print("Before view classsssssssssssss")
        response = self.get_response(request)
        print("After view classssssssssssss")
        return response
    #this executes just before view
    def process_view(request, *args , **kwargs ):
        print("this is process view classsssss")
        #return HttpResponse("there will no view executed")
        #in this case the view will not execute ... if return None then views will be executed
        return  None
        

    def process_exception(self ,request, exception):
        msg = exception
        return HttpResponse(msg)