import mmh3
import random

random.seed(0)


class BloomFilter:

    def __init__(self, m, k):

        self._T = [False for _ in range(m)]
        self._hash_seeds = [random.randint(1024, 1024 ** 2) for _ in range(k)]

        print(f"Initialized Bloom filter with {m} elements, {k} hash functions")

    def add(self, item):
        for hash_seed in self._hash_seeds:
            bit_idx = mmh3.hash128(str(item), hash_seed) % len(self._T)
            self._T[bit_idx] = True

    def __contains__(self, item):
        for hash_seed in self._hash_seeds:
            bit_idx = mmh3.hash128(str(item), hash_seed) % len(self._T)
            if not self._T[bit_idx]:
                return False
        return True

    def add_from_file(self, fn):
        """
        Add items from a comma-delimited text file
        IN:
            fn: path to text file
        OUT:
            items: list of added items
        """
        items = []
        for line in open(fn, 'r'):
            items += line.split(',')
        for item in items:
            self.add(item)
        return items

    def test_from_file(self, fn):
        """
        Check if items in file exist in structure
        IN:
            fn: path to comma-delimited text file
        OUT:
            items: list of checked items
            results: list, result ("YES"/"NO") per item
        """

        items = []
        for line in open(fn, 'r'):
            items += line.split(',')
        results = []
        for item in items:
            result = "YES" if item in self else "NO"
            print(f"Item={item} Result={result}")
            results.append(result)
        return items, results


# ==============================================================================

def test(inputs_file, test_file):
    print("~ TESTING BLOOM FILTER ~")

    # initialize:
    m = 32 * 1000
    k = 10
    bloom_filter = BloomFilter(m, k)

    # load data:
    input_items = []
    for line in open(INPUTS_FILE, 'r'):
        input_items += line.split(',')

    test_items = []
    for line in open(TEST_FILE, 'r'):
        test_items += line.split(',')

    # append:
    for item in input_items:
        bloom_filter.add(item)

    # test:
    success = []
    for item in test_items:
        bloom_result = item in bloom_filter
        groud_truth = item in input_items
        success.append(bloom_result == groud_truth)
        outcome = "Success!" if success[-1] else "FAILED!"
        print(f"{outcome} Item={item}, Bloom says: {bloom_result}")

    print(f"Score: {sum(success)}/{len(success)}")

    pass


def main():
    bloom = BloomFilter(100, 10)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
               'i', 'j', 'h', 'k', 'l', 'm', 'n',
               'p', 'r', 'o', 'w', 'q']
    # First insertion of letters into the bloom filter
    for letter in letters:
        bloom.add(letter)

    # Membership existence for already inserted letters
    # There should not be any false negatives
    for letter in letters:
        if letter in bloom:
            print('{} is in bloom filter as wished'.format(letter))
        else:
            print('Something is not right for {}'.format(letter))
            print('FALSE NEGATIVE')

    # Membership existence for not inserted letters
    # There could be false positives
    other_characters = ['this', 'is', 'the', 'worst', 'thing', 'happened', 'to',
                     'me', 'Id', 'like', 'this', 'to', 'be',
                     'over', 'asap', 'so', 'I could', 'play', 'in my',
                     'playstion']
    for other_character in other_characters:
        if other_character in bloom:
            print('{} isnt in bloom, but a false positive'.format(other_character))
        else:
            print('{} is not in the bloom filter as wished'.format(other_character))


if __name__ == '__main__':
    main()

    import time

    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
