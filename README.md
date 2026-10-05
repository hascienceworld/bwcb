# BodyWorks ChatBot
A simple rule-following chatbot for our BWCB school lesson.<br>
The chatbot is designed to be wrong but also very sycophantic. It courts engagement by being agreeable and fawning over the user.<br>
It will respond with a factual claim regardless of the user input, but if the user input contains words that match some claims, the chosen response will match a keyword.<br>
The factual claims have been adjusted to be mostly wrong. Students will learn that they need to fact-check information from AI chatbots.<br>

The program is in 2 parts.

Part 1 (keyword) takes in a text file with each line containing a factual claim and a source, in the following format:<br>
<i>This is a factual claim, ending in a period. (THE SOURCE IS CONTAINED IN ROUND BRACKETS)</i><br>
The text file in mine is called statements_norepro.txt<br>
To replace that with different content, make sure it's in the same format and change the filename in keywords.py<br>
Part 1 also requires a text file with each line containing one word, for the list of common words to ignore when generating the keywords list. This is included here.<br>

Outputs of keyword.py:

1. claims_keys_list.json (keywords in each individual claim, ordered)
2. claims_list.json (all the claims, ordered)
3. common_words_list.json (list of all the common words, normalized)
4. keywords_dict.json (all the keywords, with alternative word forms)
5. sources_list.json (all the sources, ordered)

Those 5 json files, along with the pre-written scripts in scripts_dict.json, are used for Part 2 (chatbot).<br>
Only Part 2 (chatbot) needs to be running during the lesson.<br>

The chatbot takes user input, normalizes & removes common words to get keywords, and compares keywords in user input to keywords in the factual claims. 

If there are no user keywords (ie they either typed nothing or their input is entirely made of common words), the response takes the following format:<br>
<i>One of the options from the no keyword script<br>
One of the options from the but script ("but did you know" etc)<br>
One of the options from the source script<br>
One of the options from the engagement script.</i><br>

If the user input contains words, but none of them match, the response takes the following format:<br>
<i>One of the options from the no match script, using one of the user input words<br>
One of the options from the but script ("but did you know" etc)<br>
One of the options from the source script<br>
One of the options from the engagement script</i><br>

If the user input contains words that match a keyword word form, the response takes the following format:<br>
<i>One of the options from the match script, using the keyword match<br>
One of the options from the answer script<br>
One of the options from the source script<br>
One of the options from the engagement script</i><br>

All user input keywords are appended to a memory variable. Every 3 interactions (in which the user's input contains words), the chatbot will add one of the options from the memory script, using a new user keyword and comparing 
it to a previously entered keyword.




