from django.db.models import Q, Avg, Count, Sum, Min, Max, Subquery

# SELECT statement
Book.objects.all()
== "SELECT * FROM book"

Book.objects.values("ISBN", "name", "price")
== "SELECT ISBN, name, price FROM book"


# LIMIT clause
Book.objects.first()
== "SELECT * FROM book LIMIT 1"

Book.objects.all()[5:10]
== "SELECT * FROM book LIMIT 5 OFFSET 5"


# WHERE CLAUSE
Book.objects.filter(ISBN="123")
== "SELECT * FROM book WHERE ISBN='123'"

Book.objects.filter(name__endswith='abc', price__lt=90000, price__gt=60000)
== "SELECT * FROM book WHERE name LIKE '%abc' AND price < 9000 AND price > 60000"

# NOT, OR, IN
Book.objects.filter(~Q(ISBN='123'))
== "SELECT * FROM book WHERE NOT ISBN='123'"

Book.objects.filter(Q(ISBN='123')|Q(name='abc'))
== "SELECT * FROM book WHERE ISBN='123' OR name='abc' "

subquery = Book.objects.values(name__gt='abc')
Book.objects.filter(name__in=Subquery(subquery))
== "SELECT * FROM book WHERE name IN (SELECT name FROM book U0 WHERE U0.name > 'abc')"


# JOIN clause
Book.objects.filter(keyword__keyword_contains='vu')
== "SELECT book.* FROM book INNER JOIN keyword ON book.ISBN = keyword.bookISBN WHERE keyword.keyword LIKE '%vu%' "

Book.objects.values("publisher__name")
== "SELECT publisher.name FROM book INNER JOIN publisher ON book.publisherId = publisher.id"


# AGGREGATE
Book.objects.aggregate(max_price=Max('price'))
== "SELECT MAX(price) as max_price FROM book"

Book.objects.aggregate(min_price=Min('price'), avg_price=Avg('price'))
== "SELECT MIN(price) AS min_price, AVG(price) AS avg_price FROM book"


# GROUP BY
Book.objects.annotate(avg_rating=Avg('review__rating'))
== "SELECT book.*, AVG(review.rating) as avg_rating FROM book INNER JOIN review ON review.bookISBN=book.ISBN GROUP BY book.ISBN"


# HAVING
Book.objects.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=3)
== SELECT book.*, AVG(review.rating) AS avg_rating 
FROM book INNER JOIN review ON review.bookISBN=book.ISBN 
GROUP BY book.ISBN HAVING AVG(review.rating) >= 3


# ORDER BY
Book.objects.order_by("price")
== "SELECT * FROM book ORDER BY price"

Book.objects.order_by("-price")
== "SELECT * FROM book ORDER BY price DESC"