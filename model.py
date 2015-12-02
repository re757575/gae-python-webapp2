from google.appengine.ext import ndb


class Book(ndb.Model):
    title = ndb.StringProperty(required=True)
    author = ndb.StringProperty()


def AllBooks():
    return Book.query()


def UpdateBook(id, title, author):
    book = Book(id=id, title=title, author=author)
    book.put()
    return book


def InsertBook(title, author):
    book = Book(title=title, author=author)
    book.put()
    return book


def DeleteBook(id):
    key = ndb.Key(Book, id)
    key.delete()
