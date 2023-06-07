from jsonrpcserver import method, serve, Success, InvalidParams

@method
def process_request(request):
    if request == 'list_books':
        return Success("List of Books")

    return InvalidParams(f"Invalid Request {request}")

serve('localhost', 5001)
