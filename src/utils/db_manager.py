import sqlite3


class DBManager:

    def __init__(self):
        # Connect to the SQLite database using a context manager
        try:
            self.connection_obj = sqlite3.connect("mymusicdb.sqlite")
            # Create a cursor object
            self.cursor = self.connection_obj.cursor()
            table_creation_query = ['''
            CREATE TABLE IF NOT EXISTS music_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    genre TEXT,
    artist TEXT,
    album TEXT,
    title TEXT,
    isrc TEXT UNIQUE,
    spotify_id TEXT UNIQUE
);''', '''CREATE TABLE IF NOT EXISTS file_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duration INTEGER,
    audio_codec TEXT NOT NULL,
    frames INTEGER NOT NULL,
    frame_rate REAL NOT NULL,
    channels TEXT NOT NULL,
    sample_width TEXT NOT NULL,
    bitrate REAL NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    iscr TEXT UNIQUE NOT NULL,
    music_info_id INTEGER,
    FOREIGN KEY (music_info_id) REFERENCES music_info(id)
);''', ''' CREATE INDEX idx_file_path ON file_info(file_path);''']

            # Execute the query to create the table
            for i in table_creation_query:
                continue
                self.cursor.execute(i)
                # Commit the changes
                self.connection_obj.commit()

        except Exception as e:
            print(e)

    def select_query(self, query):
        try:
            self.cursor.execute(query)
            existing_data = self.cursor.fetchall()
            return existing_data
        except Exception as e:
            print(query, "failed", e)
            return None

    def insert_record(self, table_name, record, force_update=False):
        # Check if the key (name) already exists
        key = "file_path"  # if table_name == "file_info" else "file_path"
        quer = 'SELECT {0} FROM {1} WHERE {0}="{2}"'.format(key, table_name, record[key])
        self.cursor.execute(quer)
        existing_data = self.cursor.fetchone()

        if existing_data:
            if force_update:
                self.update_record(table_name, record)
            else:
                pass
                # print(existing_data)
                # raise ValueError(f"Data with id already exists in the database.")
        else:
            columns = ', '.join(record.keys())
            try:
                values_placeholder = ', '.join(
                    ["\'{}\'".format(str(x)) if isinstance(x, str) else str(x) for x in record.values()])

                query = f'INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})'
                print(query)
                self.cursor.execute(query)
                # Commit the changes (required after INSERT)
                self.connection_obj.commit()
            except:
                values_placeholder = ', '.join(
                    ["\"{}\"".format(str(x)) if isinstance(x, str) else str(x) for x in record.values()])

                query = f'INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})'
                print(query)
                self.cursor.execute(query)
                # Commit the changes (required after INSERT)
                self.connection_obj.commit()
            # print(f"DB insert successful")

    def update_record(self, table_name, record):
        key = "file_path" # if table_name == "file_info" else "spotify_id"
        self.cursor.execute('SELECT {0} FROM {1} WHERE {0}="{2}"'.format(key, table_name, record[key]))
        existing_data = self.cursor.fetchone()

        if not existing_data:
            raise ValueError(f"Data with id doesn't exist in the database.")
        else:
            set_clause = ', '.join(["\"{}\"".format(str(x)) if isinstance(x, str) else str(x) for x in record.values()])

            key = "file_path"  # if table_name == "file_info" else "spotify_id"

            query = f'UPDATE {table_name} SET {set_clause} WHERE {key} = {record[key]}'

            # Add record_id to the tuple of values
            values = tuple(record.values())

            self.cursor.execute(query, values)
            print(f"DB update successful")

        # Commit the changes (required after INSERT)
        self.connection_obj.commit()

    def add_file_to_db(self):
        self.dbobj.insert_record("file_info", self.audio_quality_data.to_dict())

    def add_music_info_to_db(self):
        self.dbobj.insert_record("music_info", self.music_info)

    def add_to_db(self):
        try:
            self.audio_quality_data.file_path = self.windows_path_to_posix_relative(self.audio_quality_data.file_path)
            self.music_info.file_path = self.audio_quality_data.file_path
            self.add_music_info_to_db()
        except Exception as e:
            print("Music info table not updated", self.audio_quality_data.file_path, e)
        try:
            self.add_file_to_db()
        except Exception as e:
            print("File info table not updated", self.audio_quality_data.file_path, e)

    def __del__(self):
        self.connection_obj.close()
