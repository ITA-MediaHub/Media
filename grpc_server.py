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
            pub_year=book["pub_year"],
            owner=owner_obj,
            authors=author_obj_list
        )

        if "cover" in book:
            cover_obj = book_service_msg_pb2.Cover(
                type=book["cover"]["type"],
                content=book["cover"]["content"]
            )
            book_obj.cover = cover_obj

        return book_obj

    def GetBooks(self, request, context):
        for book in book_model.getBooks():
            yield self.constructBookObject(book)

    def GetBookById(self, request, context):
        book_id = request.id
        book = book_model.getBookById(book_id)
        return self.constructBookObject(book)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_BookServiceServicer_to_server(BookService(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__=="__main__":
    serve()
