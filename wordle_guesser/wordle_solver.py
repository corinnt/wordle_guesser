import csv

dict_0 = {}
dict_1 = {}
dict_2 = {}
dict_3 = {}
dict_4 = {}
dict_list : list[dict[str, set[str]]] = [dict_0, dict_1, dict_2, dict_3, dict_4]
answers_set : set[str] = set()

with open('wordle_guesser/valid_words.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        for word in row:    
            answers_set.add(word)
            index = 0
            for letter in word:
                if letter in dict_list[index].keys(): 
                    # letter has already been added to this dict
                    dict_list[index][letter].add(word)
                else:
                    # add letter to dict for first time
                    dict_list[index][letter] = {word} 
                index+=1

def main():
    user_input = input("guess details> ").lower().split()
    while user_input != "found":
        locked_dict, loose_dict, continue_flag = read_locked_loose(user_input)
        if continue_flag:
            print("possible guesses: " + str(find_guesses(locked_dict, loose_dict)))
        user_input = input("guess details> ").lower().split()

def read_locked_loose(user_input):
    '''takes in user input, returns dictionaries of locked and loose letters mapped to their possible indices.
        error catching needs work.'''
    # locked dict: maps letter to list of existing indices
    locked : dict[str, list[int]] = {}
    # loose dict: maps letter to list of poss indices
    loose : dict[str, list[int]] = {}
    indices = [0, 1, 2, 3, 4]
    lock_loose = -1
    is_index = False
    continue_flag = True
    for i in range(len(user_input)):
        arg = user_input[i] 
        # end program
        if arg == "found":
            print("Congrats!")
            continue_flag = False
        # parsing locked args
        elif arg == "locked:":
            lock_loose = 0
        # parsing loose args
        elif arg == "loose:":
            lock_loose = 1
        # error catching for multicharacter arg or no locked or loose indication
        elif lock_loose < 0:
            print("missing locked or loose flag")
            continue_flag = False
        elif len(arg) > 1:
            print("argument too long at " + str(i))
            continue_flag = False
        # a locked letter is given
        elif lock_loose == 0 and not is_index and arg.isalpha(): 
            try:
                if arg in locked.keys(): # double letter - already has an index list going
                    locked[arg].append(int(user_input[i + 1]))
                else:                    # first instance - make a new index list
                    locked[arg] = [int(user_input[i + 1])]
                is_index = True
            except:
                print("index was not an int")
                continue_flag = False             
        # a locked index is given
        elif lock_loose == 0 and is_index and not arg.isalpha():                    
            try:
                indices.remove(int(arg))
                is_index = False
            except:
                print("'index' was out of range or duplicate @" + str(i) + ", " + arg)
                continue_flag = False
        # a loose letter is given
        elif lock_loose == 1 and arg.isalpha():
            loose[arg] = indices    
        # if you're here god help you
        else: 
            print("incorrect argument (funky one)")
            continue_flag = False
    return locked, loose, continue_flag

def foldl(func, init, seq):
    '''fold left function bc pyret has ruined me'''
    if not seq:
        return init
    else:
        return foldl(func, func(init, seq[0]), seq[1:])

def find_guesses(locked, loose):
    '''takes in dicts of locked and loose letters, returns guesses fitting constraints'''
    set_0 = set()
    set_1 = set()
    set_2 = set()
    set_3 = set()
    set_4 = set()
    set_list = [set_0, set_1, set_2, set_3, set_4]
    locked_indices = []
    # populate suggested set of locked letters
    for letter_ilist in locked.items():
        # locked : dict{letters -> [indices]}
        letter = letter_ilist[0]
        ilist = letter_ilist[1]
        for index in ilist:
            set_list[index] = eval("dict_" + str(index))[letter]
            locked_indices.append(index)
    locked_list = [set_list[i] for i in locked_indices]

    if len(locked_list) > 0:
        locked_set = foldl(lambda x, y: x.intersection(y), locked_list[0], locked_list)
    else: #locked_list is empty
        locked_set = answers_set

    # populate suggested set of loose letters
    letter_list = []
    # loose : dict{letters -> [indices]}
    for letter_ilist in loose.items():
        letter = letter_ilist[0]
        ilist = letter_ilist[1]
        letter_list.append(set())
        for index in ilist:
            i = len(letter_list) - 1
            try:
                letter_list[i] = letter_list[i].union(eval("dict_" + str(index))[letter])
            except:
                print("dictionary skipped at letter " + str(letter) + ", index " + str(index))

    if len(letter_list) > 0:
        loose_set = foldl(lambda x, y: x.intersection(y), letter_list[0], letter_list)
    else: #letter_list is empty
        loose_set = answers_set

    # intersection between locked and loose suggestions -> viable guesses
    guesses = locked_set.intersection(loose_set)
    return guesses    

if __name__ == "__main__":
    main()
