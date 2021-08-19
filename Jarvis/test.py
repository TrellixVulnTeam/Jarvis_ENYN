import random
import time

if __name__ == "__main__":
    for i in range(10):
        print(10-i)
        time.sleep(1)
    filme = ["suicide", "le truck"]
    print(random.choice(filme))