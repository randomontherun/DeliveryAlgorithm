class HashTable:
    def __init__(self):
        self.size = 25
        self.table = [None] * self.size

    # Calculates a hash value for the key
    def hash(self, key):
        hashValue = 0
        for char in str(key):
            hashValue += ord(char)
        return hashValue % self.size

    # Adds a value to the hash table
    def add(self, key, value):
        hashKey = self.hash(key)
        kv = [key, value]

        # Add pair if table is empty at this location
        if self.table[hashKey] is None:
            self.table[hashKey] = list([kv])
            return True
        # If it is not empty, check if key exists and update if so
        else:
            for pair in self.table[hashKey]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            # Otherwise add pair to the end of the table location
            self.table[hashKey].append(kv)
            return True

    # Finds a value in the table
    def lookup(self, key):
        hashKey = self.hash(key)
        if self.table[hashKey] is not None:
            for pair in self.table[hashKey]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Removes value from table
    def remove(self, key):
        hashKey = self.hash(key)
        if self.table[hashKey] is None:
            return False
        for i in range(len(self.table[hashKey])):
            if self.table[hashKey][i][0] == key:
                self.table[hashKey].pop(i)
                return True

    # Prints the key/value pair
    def __str__(self):
        for pair in self.table:
            if pair is not None:
                print(str(pair))
        return ''


# Citing source: I used this video from the WGU C950 course tips as a guide: https://www.youtube.com/watch?v=9HFbhPscPU0