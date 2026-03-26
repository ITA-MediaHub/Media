import grpc
from book_service_pb2_grpc import BookServiceStub
import book_service_msg_pb2

channel = grpc.insecure_channel("localhost:50051")
stub = BookServiceStub(channel)

def getBooks():
    for book in stub.GetBooks(book_service_msg_pb2.GetBooksRequest()):
        print(book.id, book.title, book.pub_year, book.owner.username)

def getBookById(id):
    return stub.GetBookById(book_service_msg_pb2.GetBookByIdRequest(id=id))

def main():
    getBookById(2)

if __name__=="__main__":
    main()
