
# Make book list
books = [
    {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"title": "Dune", "author": "Frank Herbert"},
    {"title": "Neuromancer", "author": "William Gibson"},
    {"title": "Watchmen", "author": "Alan Moore"},
    {"title": "The Martian", "author": "Andy Weir"},
]

# Func to get first 3 entries in list
def firstThreeBooks():
    return books[0:3]

# Example Students and their ID #'s
studentDB = {
    "Alice": "S0012345",
    "Bob": "S0012346",
    "Charlie": "S0012347",
}

# Returns student id based on name. 
# returns none if no student
def getStudentId(name: str, default=None):
    return studentDB.get(name, default)
