def main():
    n = 10
    a, b = 0, 1
    fib_sequence = []
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    
    print("The first 10 Fibonacci numbers are:")
    print(fib_sequence)

if __name__ == "__main__":
    main()
