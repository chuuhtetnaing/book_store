with open('book582.csv') as csvfile:
   for column in csv.reader(csvfile, delimiter='^'):
      b = Book(isbn = column[0], text_reviews_count = column[1], asin = column[2],is_ebook = eval(column[3].capitalize()),average_rating = column[4],kindle_asin = column[5],description = column[6],book_format = column[7],link = column[8],authors = column[9],publisher = column[10],num_pages = column[11],publication_day = column[12],isbn13 = column[13],publication_month = column[14],publication_year = column[15],url = column[16],image_url = column[17],book_id = column[18],ratings_count = column[19],work_id = column[20],title = column[21],title_without_series = column[22])
      b.save()

with open('book582_user100_genres.csv') as csvfile:
   for column in csv.reader(csvfile):
      b = Book.objects.get(book_id=column[0])
      g = Genre.objects.get(genre = column[1])
      g.books.add(b)
      g.save()