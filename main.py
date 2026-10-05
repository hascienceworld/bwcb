from word_forms.word_forms import get_word_forms
import json


# clear out weird formatting characters
def replace_weird_chars(raw_string):
    transl_table = dict([(ord(x), ord(y)) for x, y in zip(u"‘’´“”–-", u"'''\"\"--")])
    clean = raw_string.translate(transl_table)
    return clean


# remove punctuation
def remove_punctuation(string):
    punc = '!\"#\'$%&*+,-./:;<=>?@()[\\]^_`{|}~'
    for punctuation in punc:
        string = string.replace(punctuation, '')
    return string


# remove possessives
def remove_possessives(list_of_words):
    for item in range(len(list_of_words)):
        word = list_of_words[item]
        if word[len(word) - 2:] == '\'s':
            list_of_words[item] = word[:len(word) - 2]
        elif word[len(word) - 1] == '\'':
            list_of_words[item] = word[:len(word) - 1]
    return list_of_words


# make a new word list, ignoring common words
def remove_common_words(word_list):
    numerals_tuple = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    new_list = [x for x in word_list
                if (x not in common_words_list and x[0] not in numerals_tuple)]
    return new_list


# break down a string into only keywords
def make_word_list(string):
    # make a list of all words in each claim
    new_word_list = string.lower().split()
    # get rid of possessives
    new_word_list = remove_possessives(new_word_list)
    # join to remove punctuation then split back into list
    new_word_list = remove_punctuation(' '.join(new_word_list)).split()
    # keep only keywords of common words
    just_keywords_list = remove_common_words(new_word_list)
    return just_keywords_list


# create a list of keywords from a list of lists of keywords
def create_keywords_dict(list_of_word_lists):
    # list of all keywords
    all_words_string = ' '.join(' '.join(each_list) for each_list in list_of_word_lists)
    all_keywords = all_words_string.split()
    # remove duplicates
    key_words = list(set(all_keywords))
    # alphabetical order
    key_words.sort()
    # build dictionary of keywords and alternative forms
    words_dict = {}
    for word in key_words:
        # get alternative forms for each key word
        forms_dict = get_word_forms(word)
        #print(forms_dict)
        forms_list = [word]
        for form in forms_dict.values():
            # add each new word form to the list
            for item in form:
                if item not in forms_list:
                    forms_list.append(item)
        # add the key word and word forms to dictionary
        words_dict[word] = forms_list
    return words_dict



# open common words as list
common_words_list = []
with open('common_words.txt', 'r', encoding="utf-8") as common_words_file:
    for line in common_words_file:
        line = replace_weird_chars(line)
        line = remove_punctuation(line)
        common_words_list.append(line.strip().lower())

# create ordered lists of claims & sources
claims_list = []
sources_list = []
with open('statements_norepro.txt', 'r', encoding="utf-8") as statements_file:
    # split each line into claim and source, and append to relevant lists in order
    for line in statements_file:
        # clean up
        line = replace_weird_chars(line)
        line = line.strip().strip(")\n")
        # split
        statement = line.rsplit("(", 1)
        # add source to source list
        sources_list.append(statement[1].strip())
        # clean up claim
        claim = statement[0].strip().strip(".")
        # lower first letter
        claim = claim.replace(claim[0], claim[0].lower())
        # add claim to claim list
        claims_list.append(claim)

# get list of keywords in each claim
claims_keys_lists = []
for claim in claims_list:
    claims_keys_lists.append(make_word_list(claim))

# get dictionary of keywords and alternatives
keys_dict = create_keywords_dict(claims_keys_lists)

# save to JSON files
with open('common_words_list.json', 'w') as f:
    json.dump(common_words_list, f, indent=4)
with open('sources_list.json', 'w') as f:
    json.dump(sources_list, f, indent=4)
with open('claims_list.json', 'w') as f:
    json.dump(claims_list, f, indent=4)
with open('claims_keys_lists.json', 'w') as f:
    json.dump(claims_keys_lists, f, indent=4)
with open('keywords_dict.json', 'w') as f:
    json.dump(keys_dict, f, indent=4)

if len(claims_list) == len(claims_keys_lists) and len(claims_list) == len(sources_list):
    print("You have an equal number of claims, sources, and lists of keywords.")
else:
    print("Something went wrong. Check that all your statements are in the format:")
    print("This is a claim ending in a period. (This is a source enclosed in brackets)")
    print("with each statement in a new line in the .txt file.")

