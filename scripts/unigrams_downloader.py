import gzip
import sqlite3
import urllib.request


db_connection = sqlite3.connect(
    database='unigrams.sqlite3',
    timeout=10,
)
db_cursor = db_connection.cursor()
db_cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS unigrams (
            unigram TEXT,
            count INTEGER,
            UNIQUE(unigram)
        )
    '''
)
db_cursor.execute(
    '''
        CREATE INDEX IF NOT EXISTS count ON unigrams (count)
    '''
)
db_connection.commit()

urls = [
    f'http://storage.googleapis.com/books/ngrams/books/20200217/eng/1-{i:05d}-of-00024.gz'
    for i in range(0, 24)
]
for url in urls:
    print(f'processing {url}')

    with urllib.request.urlopen(
        url=url,
    ) as response:
        with gzip.GzipFile(
            fileobj=response,
        ) as uncompressed:
            for line in uncompressed:
                fragments = line.decode().split('\t')
                unigram = fragments[0].lower()
                if not unigram.isalnum():
                    continue

                count = 0
                for frag in fragments[1:]:
                    year, number_of_instances, volume = frag.split(',')
                    count += int(number_of_instances)

                db_cursor.execute(
                    '''
                        INSERT INTO unigrams
                        VALUES (?, ?)
                        ON CONFLICT (unigram) DO
                        UPDATE SET count = count + ?;
                    ''',
                    (
                        unigram,
                        count,
                        count,
                    ),
                )

db_connection.commit()
