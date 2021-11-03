import gzip
import msgpack
import sqlite3
import math


unigrams_connection = sqlite3.connect(
    database='unigrams.sqlite3',
    timeout=10,
)
unigrams_db_cursor = unigrams_connection.cursor()

bigrams_connection = sqlite3.connect(
    database='bigrams.sqlite3',
    timeout=10,
)
bigrams_db_cursor = bigrams_connection.cursor()

unigrams = {
    unigram: float(count)
    for unigram, count in unigrams_db_cursor.execute(
        '''
            SELECT word, count
            FROM unigrams
            ORDER BY count DESC
            LIMIT 1000000;
        '''
    )
}
unigrams_total_count = sum(unigrams.values())

bigrams = {}
bigrams_total_count = 0
for bigram_first, bigram_second, count in bigrams_db_cursor.execute(
    '''
        SELECT bigram_first, bigram_second, count
        FROM bigrams
        ORDER BY count DESC
        LIMIT 100000;
    '''
):
    bigram_first = bigram_first.decode()
    bigram_second = bigram_second.decode()

    if bigram_first in bigrams:
        bigrams[bigram_first][bigram_second] = float(count)
    else:
        bigrams[bigram_first] = {
            bigram_second: float(count)
        }

    bigrams_total_count += count

bigrams_processed = {}
for bigram_first, inner in bigrams.items():
    for bigram_second, count in inner.items():
        if bigram_first in unigrams:
            if bigram_first not in bigrams_processed:
                bigrams_processed[bigram_first] = {}
            bigrams_processed[bigram_first][bigram_second] = math.log10(
                (count / bigrams_total_count) /
                (unigrams[bigram_first] / unigrams_total_count)
            )

unigrams_processed = {
    unigram: math.log10(count / unigrams_total_count)
    for unigram, count in unigrams.items()
}
unigrams_processed['unigrams_total_count'] = unigrams_total_count

with gzip.GzipFile(
    filename='unigrams.msgpack.gz',
    mode='wb',
) as compressed_file:
    compressed_file.write(msgpack.packb(unigrams_processed))

with gzip.GzipFile(
    filename='bigrams.msgpack.gz',
    mode='wb',
) as compressed_file:
    compressed_file.write(msgpack.packb(bigrams_processed))
