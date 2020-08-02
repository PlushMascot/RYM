import psycopg2
import sys

from settings import db_config


def db_insert_image(album):
    """
    :params: album namedtuple("Album", ["artist", "name", "link", "id", "file_path"])
    """

    SQL = "INSERT INTO album_covers(id, artist, name, image)" "VALUES (%s, %s, %s, %s)"

    try:
        with open(album.file_path, "rb") as f:
            image = f.read()
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(SQL, (album.id, album.artist, album.name, psycopg2.Binary(image)))
        conn.commit()
        cur.close()
    except psycopg2.DatabaseError as e:
        print("Database error", e)
        return 0
    except Exception as e:
        print("Error: ", e)
        return 0
    return 1
