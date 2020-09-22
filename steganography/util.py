''' Common Utility '''
def seed_generator(key):
    seed = 0
    for c in key:
        seed += ord(c)
    return seed

if __name__ == "__main__":
    print(seed_generator('STEGANOGRAFI'))