import gzip
import sqlite3
import urllib.request
import concurrent.futures


def process_url(
    url,
):
    print(f'processing {url}')

    db_connection = sqlite3.connect(
        database='bigrams.sqlite3',
        timeout=100000,
    )
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS bigrams (
                bigram_first TEXT,
                bigram_second TEXT,
                count INTEGER,
                UNIQUE(bigram_first, bigram_second)
            )
        '''
    )
    db_cursor.execute(
        '''
            CREATE INDEX IF NOT EXISTS count ON bigrams (count)
        '''
    )
    db_connection.commit()

    chunk = []
    with urllib.request.urlopen(
        url=url,
    ) as response:
        with gzip.GzipFile(
            fileobj=response,
        ) as uncompressed:
            for line in uncompressed:
                bigram, _, fragments = line.decode().partition('\t')

                bigram_first, _, bigram_second = bigram.lower().partition(' ')
                bigram_first, _, _ = bigram_first.rpartition('_')
                bigram_second, _, _ = bigram_second.rpartition('_')

                if not bigram_first.isalnum() or not bigram_second.isalnum():
                    continue

                count = 0
                for frag in fragments.split('\t'):
                    count += int(frag.split(',')[1])

                if len(chunk) == 100000:
                    db_cursor.executemany(
                        '''
                            INSERT INTO bigrams
                            VALUES (?, ?, ?)
                            ON CONFLICT (bigram_first, bigram_second) DO
                            UPDATE SET count = count + ?;
                        ''',
                        chunk,
                    )
                    db_connection.commit()
                    chunk.clear()
                else:
                    chunk.append(
                        (
                            bigram_first,
                            bigram_second,
                            count,
                            count,
                        )
                    )

    db_cursor.executemany(
        '''
            INSERT INTO bigrams
            VALUES (?, ?, ?)
            ON CONFLICT (bigram_first, bigram_second) DO
            UPDATE SET count = count + ?;
        ''',
        chunk,
    )
    db_connection.commit()


futures = []
with concurrent.futures.ProcessPoolExecutor(
    max_workers=30,
) as executor:
    urls = [
        f'http://storage.googleapis.com/books/ngrams/books/20200217/eng/2-{i:05d}-of-00589.gz'
        for i in range(0, 589)
    ]
    for url in urls:
        futures.append(executor.submit(process_url, url))

for future in concurrent.futures.as_completed(futures):
    print(f'finished {future.result()}')
