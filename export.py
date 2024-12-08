import sqlite3
from pprint import pprint
import inquirer

def highlights_from_book(cur, contentID):
    sql = "SELECT '#' || row_number() OVER (PARTITION BY B.Title ORDER BY T.ChapterProgress, T.DateModified) AS row_number, "\
    "T.Text AS text "\
    "FROM content AS B "\
    "JOIN bookmark AS T ON B.ContentID = T.VolumeID "\
    f"WHERE T.Text != '' AND T.Hidden = 'false' AND B.ContentID = '{contentID}' "\
    "ORDER BY T.ChapterProgress, T.DateModified "

    return cur.execute(sql).fetchall()

def book_list(cur):
    sql = "SELECT "\
    "  IFNULL(ContentID,'') as 'id', "\
    "  IFNULL(Title,'') as 'title', "\
    "  IFNULL(Attribution,'') as 'author', "\
    "  IFNULL(Publisher,'') as 'publisher', "\
    "  IFNULL(ISBN,0) as 'isbn', "\
    "  IFNULL(date(DateCreated),'') as 'releaseDate', "\
    "  IFNULL(Series,'') as 'series', "\
    "  IFNULL(SeriesNumber,0) as 'seriesNumber', "\
    "  IFNULL(AverageRating,0) as 'rating', "\
    "  IFNULL(___PercentRead,0) as 'readPercent', "\
    "  IFNULL(CASE WHEN ReadStatus>0 THEN datetime(DateLastRead) END,'') as 'lastRead', "\
    "  IFNULL(___FileSize,0) as 'fileSize', "\
    "  IFNULL(CASE WHEN Accessibility=1 THEN 'Store' ELSE CASE WHEN Accessibility=-1 THEN 'Import' ELSE CASE WHEN Accessibility=6 THEN 'Preview' ELSE 'Other' END END END,'') as 'source' "\
    "FROM content "\
    "WHERE ContentType=6 "\
    "AND ___UserId IS NOT NULL "\
    "AND ___UserId != '' "\
    "AND ___UserId != 'removed' "\
    "AND MimeType != 'application/x-kobo-html+pocket' "\
    "AND EXISTS ( "\
    "  SELECT 1 "\
    "  FROM bookmark "\
    "  WHERE bookmark.VolumeID = content.ContentID "\
    "  AND bookmark.Text != '' "\
    "  AND bookmark.Hidden = 'false' "\
    ") "\
    "ORDER BY Source desc, Title"

    return cur.execute(sql).fetchall()

dbfile = './2023-01-06.sqlite'
con = sqlite3.connect(dbfile)
cur = con.cursor()

# reading all table names
# table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
# here is you table list
# print(table_list)
options = [(f"{b[1]} - {b[2]}", b[0]) for b in book_list(cur)]
# book = book_list(cur)[0][0]
# print(highlights_from_book(cur, book))

# Be sure to close the connection
con.close()
questions = [
    inquirer.Checkbox(
        "interests",
        message="Select Books to Export Notes For",
        choices=options
    ),
]

answers = inquirer.prompt(questions)

pprint(answers)