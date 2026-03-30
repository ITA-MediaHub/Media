import time
import unittest
import grpc
import os
from pathlib import Path
import threading
import sqlite3
from book_service.grpc_interface.book_service_pb2_grpc import BookServiceStub
import book_service.grpc_interface.book_service_msg_pb2 as grpc_messages
import book_service.grpc_server
import book_service.setup_db as db

class TestEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = Path(__file__).resolve().parent.parent
        db_path = base_dir / "book_service/db/test.sqlite3"
        cls.db_path = str(db_path)
        
        db_path.unlink()
        os.environ["DATABASE"] = cls.db_path
        db.setup(cls.db_path, str(base_dir / "book_service/db/setup.sql"))

        def run_server():
            cls.server = book_service.grpc_server.serve()
            cls.server.start()
            cls.server.wait_for_termination()

        cls.thread = threading.Thread(target=run_server, daemon=True)
        cls.thread.start()

        time.sleep(0.5)

        cls.channel = grpc.insecure_channel("localhost:50051")
        cls.client = BookServiceStub(cls.channel)

    @classmethod
    def tearDownClass(cls):
        cls.channel.close()
        cls.server.stop(0)

    def tearDown(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.executescript("""
            DELETE FROM book_has_author;
            DELETE FROM author;
            DELETE FROM book;
            DELETE FROM cover;
            DELETE FROM owner;
            DELETE FROM sqlite_sequence WHERE name IN ("book_has_author", "author", "book", "cover", "owner");
        """)
        cursor.close()

    def test_no_books(self):
        for response in self.client.GetBooks(grpc_messages.GetBooksRequest()):
            self.fail("Recieved response when there should be none.")

    def test_get_books(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (1, "owner1"))
        cursor.executemany("INSERT INTO book (title, owner_id) VALUES (?, ?)", [("book1", 1), ("book2", 1)])
        cursor.close()

        responses = []

        for response in self.client.GetBooks(grpc_messages.GetBooksRequest()):
            responses.append(response)

        self.assertEqual(len(responses), 2)
        self.assertEqual(responses[0].book.title, "book1")
        self.assertEqual(responses[1].book.title, "book2")
        self.assertEqual(responses[0].book.owner.id, 1)
        self.assertEqual(responses[1].book.owner.id, 1)
        self.assertEqual(responses[0].book.owner.username, "owner1")
        self.assertEqual(responses[1].book.owner.username, "owner1")

    def test_get_book_by_id(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (1, "owner1"))
        cursor.execute("INSERT INTO book (title, owner_id) VALUES (?, ?)", ("book1", 1))
        cursor.close()

        response = self.client.GetBookById(grpc_messages.GetBookByIdRequest(id=1))
        self.assertEqual(response.WhichOneof("GetBookByIdResponseOneOf"), "book")
        self.assertEqual(response.book.id, 1)
        self.assertEqual(response.book.title, "book1")
        self.assertEqual(response.book.owner.id, 1)
        self.assertEqual(response.book.owner.username, "owner1")

    def test_get_book_by_id_non_existant(self):
        response = self.client.GetBookById(grpc_messages.GetBookByIdRequest(id=1))
        self.assertEqual(response.WhichOneof("GetBookByIdResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

    def test_get_books_by_owner(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.executemany("INSERT INTO owner (id, username) VALUES (?, ?)", [(1, "owner1"), (2, "owner2")])
        cursor.executemany("INSERT INTO book (title, owner_id) VALUES (?, ?)", [("book1", 1), ("book2", 2)])
        cursor.close()

        responses = []

        for response in self.client.GetBooksByOwner(grpc_messages.GetBooksByOwnerRequest(owner_id=2)):
            responses.append(response)

        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].WhichOneof("GetBooksByOwnerResponseOneOf"), "book")
        self.assertEqual(responses[0].book.title, "book2")
        self.assertEqual(responses[0].book.owner.id, 2)

    def test_add_book_success(self):
        book_obj = grpc_messages.Book(
            title="book1",
            pub_year=-1,
            owner=grpc_messages.Owner(id=1, username="owner1")
        )
        response = self.client.AddBook(grpc_messages.AddBookRequest(book=book_obj))
        self.assertEqual(response.WhichOneof("AddBookResponseOneOf"), "book_id")
        self.assertHasAttr(response, "book_id")

        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("SELECT * FROM book")
        results = cursor.fetchall()
        cursor.close()
        self.assertEqual(len(results), 1)

    def test_add_book_bad_title(self):
        book_obj = grpc_messages.Book(
            title="",
            pub_year=-1,
            owner=grpc_messages.Owner(id=1, username="owner1")
        )
        response = self.client.AddBook(grpc_messages.AddBookRequest(book=book_obj))
        self.assertEqual(response.WhichOneof("AddBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("SELECT * FROM book")
        self.assertIsNone(cursor.fetchone())
        cursor.close()

    def test_add_book_bad_year(self):
        book_obj = grpc_messages.Book(
            title="book1",
            pub_year=-50,
            owner=grpc_messages.Owner(id=1, username="owner1")
        )
        response = self.client.AddBook(grpc_messages.AddBookRequest(book=book_obj))
        self.assertEqual(response.WhichOneof("AddBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("SELECT * FROM book")
        self.assertIsNone(cursor.fetchone())
        cursor.close()

    def test_add_book_no_owner(self):
        book_obj = grpc_messages.Book(
            title="book1",
            pub_year=-1
        )
        response = self.client.AddBook(grpc_messages.AddBookRequest(book=book_obj))
        self.assertEqual(response.WhichOneof("AddBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("SELECT * FROM book")
        self.assertIsNone(cursor.fetchone())
        cursor.close()

    def test_add_book_bad_owner(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (1, "owner1"))

        book_obj = grpc_messages.Book(
            title="book1",
            pub_year=-1,
            owner=grpc_messages.Owner(id=1, username="wrong_username")
        )
        response = self.client.AddBook(grpc_messages.AddBookRequest(book=book_obj))
        self.assertEqual(response.WhichOneof("AddBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

        
        cursor.execute("SELECT * FROM book")
        self.assertIsNone(cursor.fetchone())
        cursor.close()
    
    def test_add_book_bad_cover(self):
        book_obj = grpc_messages.Book(
            title="book1",
            pub_year=-1,
            owner=grpc_messages.Owner(id=1, username="owner1"),
            cover=grpc_messages.Cover(type="text/plain", content=bytes())
        )
        response = self.client.AddBook(grpc_messages.AddBookRequest(book=book_obj))
        self.assertEqual(response.WhichOneof("AddBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("SELECT * FROM book")
        self.assertIsNone(cursor.fetchone())
        cursor.close()

    def test_add_book_bad_author(self):
        book_obj = grpc_messages.Book(
            title="book1",
            pub_year=-1,
            owner=grpc_messages.Owner(id=1, username="owner1"),
            authors=[grpc_messages.Author(last_name="")]
        )
        response = self.client.AddBook(grpc_messages.AddBookRequest(book=book_obj))
        self.assertEqual(response.WhichOneof("AddBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("SELECT * FROM book")
        self.assertIsNone(cursor.fetchone())
        cursor.close()

    def test_update_book_success(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (1, "owner1"))
        cursor.execute("INSERT INTO book (title, pub_year, owner_id) VALUES (?, ?, ?)", ("book1", 1970, 1))

        response = self.client.UpdateBook(grpc_messages.UpdateBookRequest(id=1, title="new_title", pub_year=2000))
        self.assertEqual(response.WhichOneof("UpdateBookResponseOneOf"), "success")
        self.assertHasAttr(response.success, "success_msg")
        cursor.execute("SELECT title, pub_year FROM book WHERE id=?", (1,))
        row = cursor.fetchone()
        self.assertEqual(row[0], "new_title")
        self.assertEqual(row[1], 2000)

        cursor.close()

    def test_update_book_bad_data(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (1, "owner1"))
        cursor.execute("INSERT INTO book (title, pub_year, owner_id) VALUES (?, ?, ?)", ("book1", 1970, 1))

        response = self.client.UpdateBook(grpc_messages.UpdateBookRequest(id=1, title=""))
        self.assertEqual(response.WhichOneof("UpdateBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

        cursor.execute("SELECT title FROM book WHERE id=?", (1,))
        row = cursor.fetchone()
        self.assertEqual(row[0], "book1")

        cursor.close()

    def test_update_book_non_existant(self):
        response = self.client.UpdateBook(grpc_messages.UpdateBookRequest(id=1, title="new_title", pub_year=2000))
        self.assertEqual(response.WhichOneof("UpdateBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

    def test_remove_book_cover_success(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (1, "owner1"))
        cursor.execute("INSERT INTO cover (id, type, content) VALUES (?, ?, ?)", (1, "image/png", bytes()))
        cursor.execute("INSERT INTO book (title, pub_year, owner_id, cover_id) VALUES (?, ?, ?, ?)", ("book1", 1970, 1, 1))

        response = self.client.RemoveBookCover(grpc_messages.RemoveBookCoverRequest(id=1))
        self.assertEqual(response.WhichOneof("RemoveBookCoverResponseOneOf"), "success")
        self.assertHasAttr(response.success, "success_msg")

        cursor.execute("SELECT * FROM cover")
        self.assertIsNone(cursor.fetchone())

        cursor.close()

    def test_remove_book_cover_non_existant(self):
        response = self.client.RemoveBookCover(grpc_messages.RemoveBookCoverRequest(id=1))
        self.assertEqual(response.WhichOneof("RemoveBookCoverResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

    def test_remove_book_cover_already_no_cover(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (1, "owner1"))
        cursor.execute("INSERT INTO book (title, pub_year, owner_id) VALUES (?, ?, ?)", ("book1", 1970, 1))

        response = self.client.RemoveBookCover(grpc_messages.RemoveBookCoverRequest(id=1))
        self.assertEqual(response.WhichOneof("RemoveBookCoverResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")

        cursor.close()

    def test_remove_book_success(self):
        cursor = sqlite3.connect(TestEndpoints.db_path, autocommit=True).cursor()
        cursor.execute("INSERT INTO owner (id, username) VALUES (?, ?)", (1, "owner1"))
        cursor.execute("INSERT INTO book (id, title, pub_year, owner_id) VALUES (?, ?, ?, ?)", (1, "book1", 1970, 1))

        response = self.client.RemoveBook(grpc_messages.RemoveBookRequest(id=1))
        self.assertEqual(response.WhichOneof("RemoveBookResponseOneOf"), "success")
        self.assertHasAttr(response.success, "success_msg")

        cursor.execute("SELECT * FROM book")
        self.assertIsNone(cursor.fetchone())

        cursor.close()

    def test_remove_book_non_existant(self):
        response = self.client.RemoveBook(grpc_messages.RemoveBookRequest(id=1))
        self.assertEqual(response.WhichOneof("RemoveBookResponseOneOf"), "error")
        self.assertHasAttr(response.error, "error_msg")
