

class T(object):

    a = f"""

    CREATE TABLE IF NOT EXISTS 1
    (
        id                                               INTEGER PRIMARY KEY,
        2   BLOB NOT NULL,
        3  INT NOT NULL,
        4  INT NOT NULL
    );

    """

    b = f"""

    CREATE TABLE IF NOT EXISTS 1
    (
        id                                               INTEGER PRIMARY KEY,
        2   BLOB NOT NULL,
        3  INT NOT NULL,
        4  INT NOT NULL
    );

    """

ls = []
for k, v in T.__dict__.items():
    if '_' in k:
        continue
    ls.append(v)

print(len(ls))

