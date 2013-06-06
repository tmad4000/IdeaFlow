import os, sys
sys.path.append(os.path.abspath("../"))
from d4d import d4d


d4d.normalize("books",
"""
knowledge PartOf book
page PartOf book
book UsedFor reading

knowledge PartOf magazine
page PartOf magazine
magazine UsedFor reading

ice HasProperty cold
page PartOf newspaper
newspaper UsedFor reading
""", principal_component_count=None) #value of 100 causes below how_true_is to return close to zero.
                                  #value of 3 yields below how_true_is result of 0.48
                                  
#same thing but closer to English:
d4d.normalize("books", """
Knowledge is part of books. 
A Page is part of a book.
Books are used for reading.

Knowledge is part of a magazine.
A page is part of a magazine.
Magazines are used for reading.

Ice has the property of cold.
Page is part of a newspaper.
Newspapers are used for reading.
""", separator=".")


d4d.books.how_true_is("knowledge", "PartOf", "newspaper") #this assertion is NOT in the input assertions,
                                                          #so the 'truth' of it is infered by
                                                          #analogy of common sense reasoning
print(d4d.books)

