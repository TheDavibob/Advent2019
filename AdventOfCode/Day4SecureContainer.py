def number_numbers(minimum, maximum):
    # create a list of currently valid numbers
    numbers = [i for i in range(minimum, maximum+1)]
    numbers_remaining = numbers.copy()
    for number in numbers:
        print(number)
        str_number = str(number)
        deleteThis = False
        for idx in range(len(str_number) - 1):
            if int(str_number[idx]) > int(str_number[idx + 1]):
                deleteThis = True
                break

        if not deleteThis:
            # Check for repetitions
            deleteThis = True
            for idx in range(len(str_number) - 1):
                if int(str_number[idx]) == int(str_number[idx + 1]):
                    deleteThis = False
                    break

        if deleteThis:
            numbers_remaining.remove(number)

    return numbers_remaining, len(numbers_remaining)


#nums, count = number_numbers(234208, 765869)
#print(nums)
#print(count)