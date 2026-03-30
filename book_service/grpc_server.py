import grpc
from concurrent import futures
import os

from book_service.grpc_interface.book_service_pb2_grpc import BookServiceServicer, add_BookServiceServicer_to_server
import book_service.grpc_interface.book_service_msg_pb2 as grpc_messages
import book_service.models.book as book_model

class BookService(BookServiceServicer):

    def constructBookObject(self, book):
        owner_obj = grpc_messages.Owner(
            id=book["owner"]["id"],
            username=book["owner"]["username"]
        )

        author_obj_list = []
        for author in book["authors"]:
            author_obj = grpc_messages.Author(
                last_name=author["last_name"],
                first_name=author["first_name"]
            )
            author_obj_list.append(author_obj)
        
        book_obj = grpc_messages.Book(
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
            yield grpc_messages.GetBooksResponse(book=self.constructBookObject(book))

    def GetBookById(self, request, context):
        book_id = request.id
        try:
            book = book_model.getBookById(book_id)
            return grpc_messages.GetBookByIdResponse(book=self.constructBookObject(book))
        except Exception as e:
            error = grpc_messages.Error(error_msg=str(e))
            return grpc_messages.GetBookByIdResponse(error=error)
        
    def GetBooksByOwner(self, request, context):
        owner_id = request.owner_id
        for book in book_model.getBooksByOwner(owner_id):
            yield grpc_messages.GetBooksByOwnerResponse(book=self.constructBookObject(book))

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
            return grpc_messages.AddBookResponse(book_id=book_id)
        except Exception as e:
            error = grpc_messages.Error(error_msg=str(e))
            return grpc_messages.AddBookResponse(error=error)
        
    def UpdateBook(self, request, context):
        id = request.id
        title = request.title if request.title else None
        pub_year = request.pub_year if request.pub_year != -1 else None
        if request.HasField("owner"):
            owner = {
                "id": request.owner.id,
                "username": request.owner.username
            }
        else: 
            owner = None
        if request.HasField("cover"):
            cover={}
            cover["type"] = request.cover.type
            cover["content"] = request.cover.content
        else:
            cover = None
        authors = []
        for author in request.authors:
            authors.append({
                "last_name": author.last_name,
                "first_name": author.first_name if author.first_name else None
            })

        try:
            book_model.updateBook(id, title, owner, pub_year, cover, authors)
            success = grpc_messages.Success(success_msg="Book successfully updated.")
            return grpc_messages.UpdateBookResponse(success=success)
        except Exception as e:
            error = grpc_messages.Error(error_msg=str(e))
            return grpc_messages.UpdateBookResponse(error=error)

    def RemoveBookCover(self, request, context):
        book_id = request.id
        try:
            book_model.removeBookCover(book_id)
            success = grpc_messages.Success(success_msg="Cover successfully removed.")
            return grpc_messages.RemoveBookCoverResponse(success=success)
        except Exception as e:
            error = grpc_messages.Error(error_msg=str(e))
            return grpc_messages.RemoveBookCoverResponse(error=error)
        
    def RemoveBook(self, request, context):
        book_id = request.id
        try:
            book_model.removeBook(book_id)
            success = grpc_messages.Success(success_msg="Book successfully removed.")
            return grpc_messages.RemoveBookResponse(success=success)
        except Exception as e:
            error = grpc_messages.Error(error_msg=str(e))
            return grpc_messages.RemoveBookResponse(error=error)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_BookServiceServicer_to_server(BookService(), server)
    server.add_insecure_port("localhost:50051")
    return server

if __name__=="__main__":
    server = serve()
    server.start()
    server.wait_for_termination()
