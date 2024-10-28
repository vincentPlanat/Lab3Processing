




def find_interruptions(numbers, threshold=1):
    # Sort the list to ensure it's in order
    sorted_numbers = sorted(set(numbers))  # Remove duplicates and sort
    interruptions = []

    for i in range(1, len(sorted_numbers)):
        current = sorted_numbers[i]
        previous = sorted_numbers[i - 1]

        # Check for interruption
        if current - previous > threshold:
            interruptions.append((previous, current))

    return interruptions

if __name__ == '__main__':
    # Example list of numbers
    numbers = [1, 2, 3, 5, 6, 10, 11, 15]

    # Identify interruptions with a threshold of 1
    interruptions = find_interruptions(numbers, threshold=1)

    if interruptions:
        print("Interruptions found:")
        for start, end in interruptions:
            print(f"Gap between {start} and {end}")
    else:
        print("No interruptions found.")
