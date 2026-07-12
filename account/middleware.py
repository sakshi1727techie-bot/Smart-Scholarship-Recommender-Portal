from django.http import JsonResponse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        print("AdminAccessMiddleware initialized")
        self.get_response = get_response

    def __call__(self, request):
        print("AdminAccessMiddleware called")
        print("request.path:", request.path)
        print("request.method:", request.method)

        # Allow only GET and POST
        if request.method not in ["GET", "POST"]:
            return JsonResponse(
                {"error": "Invalid request method"},
                status=405
            )

        # Allow only these paths
        allowed_paths = ["/api/", "/admin/"]

        if any(request.path.startswith(path) for path in allowed_paths):
            return self.get_response(request)

        return JsonResponse(
            {"error": "Invalid request path"},
            status=403
        )