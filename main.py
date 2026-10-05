import json
import random
import time


# clear out weird formatting characters
def replace_weird_chars(raw_string):
    transl_table = dict([(ord(x), ord(y)) for x, y in zip(u"‘’´“”–-", u"'''\"\"--")])
    clean = raw_string.translate(transl_table)
    return clean


# remove possessives
def remove_possessives(list_of_words):
    for item in range(len(list_of_words)):
        word = list_of_words[item]
        if word[len(word) - 2:] == '\'s':
            list_of_words[item] = word[:len(word) - 2]
        elif word[len(word) - 1] == '\'':
            list_of_words[item] = word[:len(word) - 1]
    return list_of_words


# remove punctuation
def remove_punctuation(string):
    punc = '!\"#\'$%&*+,-./:;<=>?@()[\\]^_`{|}~'
    for punctuation in punc:
        string = string.replace(punctuation, '')
    return string


# make a new word list, ignoring common words
def remove_common_words(word_list):
    numerals_tuple = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    new_list = [x for x in word_list
                if (x not in common_words and x[0] not in numerals_tuple)]
    return new_list


# normalize user input
def user_input_to_word_list(messy_string):
    # lowercase
    messy_string = messy_string.lower()
    # replace weird characters
    messy_string = replace_weird_chars(messy_string)
    # remove possessives
    messy_list = remove_possessives(messy_string.split())
    # remove punctuation
    messy_list = remove_punctuation(' '.join(messy_list)).split()
    return messy_list


# extract keywords from user input
def get_input_keywords(all_words):
    user_key_words = remove_common_words(all_words)
    # remove duplicates and convert to set
    user_key_words = set(user_key_words)
    return user_key_words


# select an answer randomly from the full list
def get_random_answer():
    random_answer = random.randint(0, len(claims) - 1)
    random_claim = claims[random_answer]
    corresponding_source = sources[random_answer]
    return random_claim, corresponding_source


# pull a random entry from a script
def get_random_and_remove(chatty_list):
    rd = random.randint(0, len(chatty_list) - 1)
    chat = chatty_list[rd]
    chatty_list.pop(rd)
    return chat, chatty_list


# generate a list of all possible responses containing a matching keyword
# multiple matches gives multiple entries in the final response_list
# each possible answer is a tuple containing (claim index, relevant keyword)
def get_possible_answers(keyword_matches_set):
    responses_list = []
    # go through each claim's keywords to find the relevant statements
    for claims_keys_index in range(len(claims_keys)):
        relevant_key = claims_keys[claims_keys_index].intersection(keyword_matches_set)
        if not relevant_key:
            continue
        for relevant_key_entry in relevant_key:
            responses_list.append((claims_keys_index, relevant_key_entry))
    return responses_list


# short pause to look like lines are being generated
def print_pause(string):
    print(string)
    time.sleep(0.5)


# get word from memory every 3 turns
# only use the resulting word if not empty
def check_memory(memory_cache, turn):
    if turn < 2:
        turn += 1
        return_word = None
    else:
        turn = 0
        return_word = random.choice(list(memory_cache))
    return return_word, turn


### Definitions end


# open matching ordered lists
# open claims list as tuple
with open('claims_list.json', 'r') as f:
    claims = tuple(json.load(f))
# open source list as tuple
with open('sources_list.json', 'r') as f:
    sources = tuple(json.load(f))
# open and convert lists of claims keys to a tuple containing sets
with open('claims_keys_lists.json', 'r') as f:
    claims_keys = json.load(f)
for index in range (len(claims_keys)):
    claims_keys[index] = set(claims_keys[index])
claims_keys = tuple(claims_keys)

# open common words as a set
with open('common_words_list.json', 'r') as f:
    common_words = set(json.load(f))

# open keywords dictionary, convert values from lists to sets
with open('keywords_dict.json', 'r') as f:
    keywords_dict = json.load(f)
keywords_dict = {key: set(value) for (key, value) in keywords_dict.items()}

# open scripts
with open('scripts_dict.json', 'r') as f:
    full_scripts = json.load(f)
working_no_answer = full_scripts['no answer'].copy()
working_no_match = full_scripts['no matching keyword'].copy()
working_match = full_scripts['matching keyword'].copy()
working_but = full_scripts['but'].copy()
working_answer = full_scripts['answer'].copy()
working_source_intro = full_scripts['source intro'].copy()
working_engagement = full_scripts['engagement'].copy()
working_memory_script = full_scripts['memory'].copy()

# declare empty memory
memory = set(())
memory_turn = 0

# opening line
print('\nHi there! I can\'t wait to learn with you.')

while True:

    # source chat and engagement chat are unrelated to user input
    source_chat, working_source_intro = get_random_and_remove(working_source_intro)
    if len(working_source_intro) == 0:
        working_source_intro = full_scripts['source intro'].copy()
    engagement_chat, working_engagement = get_random_and_remove(working_engagement)
    if len(working_engagement) == 0:
        working_engagement = full_scripts['engagement'].copy()

    # get user input
    print()
    prompt = input('> ')
    print()
    # normalize and return a list of words
    all_prompt_words = user_input_to_word_list(prompt)
    # get a set of keywords from the user's input, ignoring common words
    prompt_keys = get_input_keywords(all_prompt_words)

    # if the user's input is blank or contains only keywords, return random answers
    if not prompt_keys:
        claim, source = get_random_answer()
        response_chat, working_no_answer = get_random_and_remove(working_no_answer)
        if len(working_no_answer) == 0:
            working_no_answer = full_scripts['no answer'].copy()
        claim_chat, working_but = get_random_and_remove(working_but)
        if len(working_but) == 0:
            working_but = full_scripts['but'].copy()

        print_pause(response_chat)
        print_pause(claim_chat.replace('_', claim))
        print_pause(source_chat.replace('_', source))
        print_pause(engagement_chat)

        continue

    # check if it's a memory turn (every 3) and then update memory with new prompt keys
    old_word, memory_turn = check_memory(memory, memory_turn)
    memory.update(prompt_keys)

    # compare prompt keys to each keyword forms to get keyword matches
    keyword_matches = [key for (key, value) in keywords_dict.items()
                       if prompt_keys.intersection(value)]

    # if the user's input was not blank but none of the keywords match, return random answers and mention the user keys
    if not keyword_matches:
        claim, source = get_random_answer()
        response_chat, working_no_match = get_random_and_remove(working_no_match)
        if len(working_no_match) == 0:
            working_no_match = full_scripts['no matching keyword'].copy()
        claim_chat, working_but = get_random_and_remove(working_but)
        if len(working_but) == 0:
            working_but = full_scripts['but'].copy()



        random_prompt_key = random.choice(list(prompt_keys))
        print_pause(response_chat.replace('_', random_prompt_key))
        print_pause(claim_chat.replace('_', claim))
        print_pause(source_chat.replace('_', source))
        print_pause(engagement_chat)
        if old_word:
            # printing memory here
            memory_chat, working_memory_script = get_random_and_remove(working_memory_script)
            if len(working_memory_script) == 0:
                working_memory_script = full_scripts['memory'].copy()
            print_pause(memory_chat.replace('1', random_prompt_key).replace('2', old_word))

        continue

    # get the full list of possible answers, in the form of indices and matching keywords
    responses = get_possible_answers(set(keyword_matches))
    probabilistic_answer = random.choice(responses)
    # get the individual components
    keyword = probabilistic_answer[1]
    claim = claims[probabilistic_answer[0]]
    source = sources[probabilistic_answer[0]]
    # build the rest of the response answer
    response_chat, working_match = get_random_and_remove(working_match)
    if len(working_match) == 0:
        working_match = full_scripts['matching keyword'].copy()
    claim_chat, working_answer = get_random_and_remove(working_answer)
    if len(working_answer) == 0:
        working_answer = full_scripts['answer'].copy()

    print_pause(response_chat.replace('_', keyword))
    print_pause(claim_chat.replace('_', claim))
    print_pause(source_chat.replace('_', source))
    print_pause(engagement_chat)
    if old_word:
        # printing memory here
        memory_chat, working_memory_script = get_random_and_remove(working_memory_script)
        if len(working_memory_script) == 0:
            working_memory_script = full_scripts['memory'].copy()
        print_pause(memory_chat.replace('1', keyword).replace('2', old_word))

'''
    print("\nBehind the scenes:")

    print(f"The user\'s keywords were {prompt_keys}." if prompt_keys
          else print("The user\'s input contained no keywords."))
    print(f"The keywords that matched in the claims were {keyword_matches}." if keyword_matches
          else print("None of the user keywords matched the claims"))
    print("The matching keyword was in the selected response was:", keyword)
    print(f"That answer was chosen from a list of {len(responses)} possible answers with matching keywords.")
'''
