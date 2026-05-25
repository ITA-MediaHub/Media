import grpc
from book_service.grpc_interface.book_service_pb2_grpc import BookServiceStub
import book_service.grpc_interface.book_service_msg_pb2 as grpc_messages

channel = grpc.insecure_channel("localhost:3000")
stub = BookServiceStub(channel)

def getBooks():
    for response in stub.GetBooks(grpc_messages.GetBooksRequest()):
        print(response.book.id, response.book.title, response.book.pub_year, response.book.owner.username)

def getBookById(id):
    response = stub.GetBookById(grpc_messages.GetBookByIdRequest(id=id))
    field = response.WhichOneof("GetBookByIdResponseOneOf")
    if field == "error":
        print(response.error.error_msg)
    elif field == "book":
        print(response.book.title)
    else: raise ValueError("Invalid response recieved")

def addBookTest():

    # remember to set unset pub_years to -1 instead of sending empty since it will store as 0

    title = "MyBook"
    owner = {"id": 1, "username": "asda"}
    book_obj = grpc_messages.Book(title=title, owner=grpc_messages.Owner(id=owner["id"], username=owner["username"]))
    response = stub.AddBook(grpc_messages.AddBookRequest(book=book_obj, token=".."))
    field = response.WhichOneof("AddBookResponseOneOf")
    if field == "error":
        print(response.error.error_msg)
    elif field == "book_id":
        print(response.book_id)
    else: raise ValueError("Invalid response recieved")

def updateBookTest():
    request = grpc_messages.UpdateBookRequest(id=1, title="NewBook", token="")
    response = stub.UpdateBook(request)
    field = response.WhichOneof("UpdateBookResponseOneOf")
    if field == "error":
        print(response.error.error_msg)
    elif field == "success":
        print(response.success.success_msg)

def removeBookCoverTest():
    request = grpc_messages.RemoveBookCoverRequest(id=1, token="..")
    response = stub.RemoveBookCover(request)
    field = response.WhichOneof("RemoveBookCoverResponseOneOf")
    if field == "error":
        print(response.error.error_msg)
    elif field == "success":
        print(response.success.success_msg)


def main():
    addBookTest()
    #updateBookTest()
    #removeBookCoverTest()

if __name__=="__main__":
    main()
