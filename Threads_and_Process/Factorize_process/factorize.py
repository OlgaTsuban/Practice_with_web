import time
import os
import concurrent.futures


# Synchronous: factorize_number(number) and factorize(*number)
def factorize_number(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize(*number):
    result = []
    for num in number:
        result.append(factorize_number(num))
    return result

# Parallel: factorize_worker(num) and factorize_worker(*numbers)
def factorize_worker(num):
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        return factors

def factorize_parallel(*numbers):
    cpuCount = os.cpu_count() #if you need you can find cpu amont on your laptop
    print(f"cpuCount : {cpuCount}")
    with concurrent.futures.ProcessPoolExecutor(cpuCount) as executor:
        results = list(executor.map(factorize_worker, numbers))
    return results


if __name__ == "__main__":
    start_time = time.time()

    #use this to Synchronous implementation
    a, b, c, d  = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    
    end_time = time.time()

    print(f"Synchronous execution took {end_time - start_time:.4f} seconds.")

    #use this to Parallel implementation
    """a, b, c, d  = factorize_parallel(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    
    end_time = time.time()

    print(f"Parallel execution took {end_time - start_time:.4f} seconds.")"""
