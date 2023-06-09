from jsonrpcserver import method, serve, Success, InvalidParams
from library.library_manager import Library

@method
def handle_request(request):
    if request == 'list_books':
        return Success(Library().list_books())

    return InvalidParams(f"Invalid Request {request}")

serve('localhost', 5001)
