from random import randrange

def get_numbers(threshold, range_to):
    numbers =[]
    test = True
    while threshold!=0:
        get_number = randrange(1,range_to+1)
        if get_number not in numbers or len(numbers)==0:
            numbers.append(get_number)
            threshold-=1
    return set(sorted(numbers))


def try_match(attempt, random_choice, my_input_sorted):

    if random_choice == my_input_sorted:
        is_not_success = False
    else:
        is_not_success = True

    return attempt, is_not_success

def get_parially_results(partially_results, random_choice, my_input_sorted):

    result = len(random_choice & my_input_sorted)

    if result not in partially_results:
        partially_results[result] = 1
    else:
        partially_results[result] = partially_results[result]+1

    return partially_results


def try_lotto(input_value):
    range_to = 49
    my_input = input_value.split(",")
    my_input = [int(number) for number in my_input if int(number)>0 and int(number)<=range_to]


    is_not_success = True
    attempt = 0
    my_input_sorted = set(sorted(my_input))
    len_my_input = len(my_input_sorted)
    partially_results = dict()

    while is_not_success:
        random_choice = get_numbers(len_my_input, range_to)
        attempt, is_not_success = try_match(attempt, random_choice, my_input_sorted)
        partially_results = get_parially_results(partially_results, random_choice, my_input_sorted)

        attempt += 1
        if attempt % 1000000 == 0:
            print(f'--- number of attempts: {int(attempt/1000000)} {"millions" if attempt/1000000 >1 else "million "}  --- random choice: {random_choice}--- my_choice: {my_input_sorted} ---')
    print(f'--- number of attempts: {attempt}  --- random choice: {random_choice} --- my_choice: {sorted(my_input)} ---')
    print(f'number of attempts: {attempt}. Detailed information about partially matched before you win {partially_results}')


if __name__ == '__main__':
    try_lotto('1,2,3,4,5,6')