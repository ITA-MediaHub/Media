import grpc
from concurrent import futures

from book_service_pb2_grpc import BookServiceServicer, add_BookServiceServicer_to_server
import book_service_msg_pb2
import models.book as book_model

class BookService(BookServiceServicer):

    def constructBookObject(self, book):
        owner_obj = book_service_msg_pb2.Owner(
            id=book["owner"]["id"],
            username=book["owner"]["username"]
        )

        author_obj_list = []
        for author in book["authors"]:
            author_obj = book_service_msg_pb2.Author(
                last_name=author["last_name"],
                first_name=author["first_name"]
            )
            author_obj_list.append(author_obj)
        
        book_obj = book_service_msg_pb2.Book(
            id=book["id"],
            title=book["title"],
            pub_year=book["pub_year"] if book["pub_year"] is not None else -1,
            owner=owner_obj,
            authors=author_obj_list
        )

        if "cover" in book:
            book_obj.cover.type=book["cover"]["type"]
            book_obj.cover.content=book["cover"]["content"]

        return book_obj

    def GetBooks(self, request, context):
        for book in book_model.getBooks():
            yield book_service_msg_pb2.GetBooksResponse(book=self.constructBookObject(book))

    def GetBookById(self, request, context):
        book_id = request.id
        try:
            book = book_model.getBookById(book_id)
            return book_service_msg_pb2.GetBookByIdResponse(book=self.constructBookObject(book))
        except Exception as e:
            error = book_service_msg_pb2.Error(error_msg=str(e))
            return book_service_msg_pb2.GetBookByIdResponse(error=error)
        
    def GetBooksByOwner(self, request, context):
        owner_id = request.owner_id
        for book in book_model.getBooksByOwner(owner_id):
            yield book_service_msg_pb2.GetBooksByOwnerResponse(book=self.constructBookObject(book))

    def AddBook(self, request, context):
        title = request.book.title
        pub_year = request.book.pub_year if request.book.pub_year != -1 else None
        owner = {
            "id": request.book.owner.id,
            "username": request.book.owner.username
        }
        if request.book.HasField("cover"):
            cover={}
            cover["type"] = request.book.cover.type
            cover["content"] = request.book.cover.content
        else:
            cover = None
        authors = []
        for author in request.book.authors:
            authors.append({"last_name": author.last_name, "first_name": author.first_name if author.first_name != "" else None})
        try:
            book_id = book_model.addBook(title, owner, pub_year, cover, authors)
            return book_service_msg_pb2.AddBookResponse(book_id=book_id)
        except Exception as e:
            error = book_service_msg_pb2.Error(error_msg=str(e))
            return book_service_msg_pb2.AddBookResponse(error=error)
        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_BookServiceServicer_to_server(BookService(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__=="__main__":
    serve()
