# BodyWorks ChatBot
A simple rule-following chatbot for our BWCB school lesson.
The factual claims have been adjusted to be mostly wrong. Students will learn that they need to fact-check information from AI chatbots.

The chatbot is designed to be wrong but also very sycophantic. It courts engagement by being agreeable and fawning over the user.
It will respond with a factual claim regardless of the user input, but if the user input contains words that match some claims, the chosen response will match a keyword.

The program is in 2 parts.


Part 1 (keyword) takes in a text file with each line containing a factual claim and a source, in the following format:
This is a factual claim, ending in a period. (THE SOURCE IS CONTAINED IN ROUND BRACKETS)
The text file in mine is called statements_norepro.txt
To replace that with different content, make sure it's in the same format and change the filename in keywordsV2.py
It also requires a text file with each line containing one word, for the list of common words to ignore when generating the keywords list.

Outputs of keyword:
1. claims_keys_list.json (keywords in each individual claim, ordered)
2. claims_list.json (all the claims, ordered)
3. common_words_list.json (list of all the common words, normalized)
4. keywords_dict.json (all the keywords, with alternative word forms)
5. sources_list.json (all the sources, ordered)

Those 5 json files, along with the pre-written scripts in scripts_dict.json, are used for Part 2 (chatbot).
Only Part 2 (chatbot) needs to be running during the lesson.


The chatbot takes user input, normalizes & removes common words to get keywords, and compares keywords in user input to keywords in the factual claims.

If there are no user keywords (ie they either typed nothing or their input is entirely made of common words), the response takes the following format:
One of the options from the no keyword script
One of the options from the but script ("but did you know" etc)
One of the options from the source script
One of the options from the engagement script.

If the user input contains words, but none of them match, the response takes the following format:
One of the options from the no match script, using one of the user input words
One of the options from the but script ("but did you know" etc)
One of the options from the source script
One of the options from the engagement script

If the user input contains words that match a keyword word form, the response takes the following format:
One of the options from the match script, using the keyword match
One of the options from the answer script
One of the options from the source script
One of the options from the engagement script


All user input keywords are appended to a memory variable. Every 3 interactions (in which the user's input contains words), the chatbot will add one of the options from the memory script, using a new user keyword and comparing it to a previously entered keyword.

