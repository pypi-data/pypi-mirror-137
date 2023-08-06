import itertools

BATCH_SIZE = 1000


def batched(thing, size=BATCH_SIZE):
    i = iter(thing)

    while True:
        r = list(itertools.islice(i, size))

        if not r:
            break

        yield r
