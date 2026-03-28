import grpc
from book_service_pb2_grpc import BookServiceStub
import book_service_msg_pb2

channel = grpc.insecure_channel("localhost:50051")
stub = BookServiceStub(channel)

def getBooks():
    for response in stub.GetBooks(book_service_msg_pb2.GetBooksRequest()):
        print(response.book.id, response.book.title, response.book.pub_year, response.book.owner.username)

def getBookById(id):
    response = stub.GetBookById(book_service_msg_pb2.GetBookByIdRequest(id=id))
    field = response.WhichOneof("GetBookByIdResponseOneOf")
    if field == "error":
        print(response.error.error_msg)
    elif field == "book":
        print(response.book.title)
    else: raise ValueError("Invalid response recieved")

def addBookTest():

    # remember to set unset pub_years to -1 instead of sending empty since it will store as 0

    title = "MyBook"
    owner = {"id": 10, "username": "Špela"}
    book_obj = book_service_msg_pb2.Book(title=title, owner=book_service_msg_pb2.Owner(id=owner["id"], username=owner["username"]))
    response = stub.AddBook(book_service_msg_pb2.AddBookRequest(book=book_obj))
    field = response.WhichOneof("AddBookResponseOneOf")
    if field == "error":
        print(response.error.error_msg)
    elif field == "book_id":
        print(response.book_id)
    else: raise ValueError("Invalid response recieved")

def main():
    addBookTest()

if __name__=="__main__":
    main()
