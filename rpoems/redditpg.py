import datetime
import random
import re
import string
import pronouncing
from psaw import PushshiftAPI


def build_corpus(subreddit="", before=datetime.datetime.now(), after=datetime.datetime(2000, 1, 1),
                 limit=2000, author=""):
    # Set up the generator that will build our corpus of comments
    corpus = []
    api = PushshiftAPI()
    gen = api.search_comments(before=int(before.timestamp()), after=int(after.timestamp()),
                              subreddit=subreddit, filter=['body'], author=author)
    comment_count = 0
    for i in gen:
        if comment_count >= limit:
            break
        comment = i.body
        cleaned_comment = re.sub(r"\s\s+", " ", comment)
        cleaned_comment = re.sub(r"\n", " ", cleaned_comment)
        if cleaned_comment != "[removed]" and cleaned_comment != "[deleted]":
            corpus.append(cleaned_comment.strip())
            comment_count += 1

    return corpus


def couplet_rhyming_poem(corpus):
    return custom_rhyme(corpus, "AABBCC")


def villanelle(corpus):
    return build_villanelle(corpus)


def acrostic(corpus, key):
    # Returns a poem in which the first letter of each line corresponds to the letters of the key in order
    return build_acrostic(corpus, key)


def all_alphabet(corpus):
    # Returns a poem in which each of the 26 lines begin with a letter of the alphabet and is in order
    # Recommended limit is 15000
    return build_acrostic(corpus, string.ascii_lowercase)


def magic_nine(corpus):
    return custom_rhyme(corpus, "abacadaba")


def haiku(corpus):
    return custom_syl(corpus, "5-7-5")


def tanka(corpus):
    return custom_syl(corpus, "5-7-5-7-7")


def nonet(corpus):
    return custom_syl(corpus, "9-8-7-6-5-4-3-2-1")


def custom_rhyme(corpus, rhyme_scheme):
    # Returns a poem consisting of the given rhyme scheme

    # Create a dictionary that details how many rhyming comments are needed for each letter
    # Rhyming Scheme "AABBCCC" -> {A:2,B:2,C:3}
    rhyme_count = {}
    for i in rhyme_scheme:
        if i not in rhyme_count:
            rhyme_count[i] = 1
        else:
            rhyme_count[i] += 1

    rhyme_sections = extract_rhyming_lines(corpus)

    # Organize the rhyming sections before by number.
    # Ex: Key 2 will have all rhyme lists of length 2
    # {2:[[might, right], [other, brother], [absurd, stirred]}
    # An approximation meant to explain. Not the exact structure.
    length_dict = {}
    for i in rhyme_sections.values():
        if len(i) not in length_dict:
            length_dict[len(i)] = [i]
        else:
            length_dict[len(i)].append(i)

    try:
        # Match them to the first rhyme dictionary so that each letter will have a list of comments that will complete
        # the rhyme scheme.
        for key, value in rhyme_count.items():
            rhyme_count[key] = pop_random(length_dict[value])

        poem = ""
        for i in range(0, len(rhyme_scheme)):
            letter_rhymes = rhyme_count[rhyme_scheme[i]]
            rhyme = pop_random(letter_rhymes)
            if i != len(rhyme_scheme) - 1:
                poem += rhyme[0] + "\n"
            else:
                poem += rhyme[0]

        return poem
    except (ValueError, KeyError) as e:
        return "Looks like your corpus was too small. Try again?"


def custom_syl(corpus, syl_string):
    syl_dict = organize_syllables(corpus)
    syl_string = syl_string.split("-")
    poem = ""
    try:
        for i in range(0, len(syl_string)):
            syllable_comments = syl_dict[int(syl_string[i])]
            comment = pop_random(syllable_comments)
            if i != len(syl_string) - 1:
                poem += comment + "\n"
            else:
                poem += comment
        return poem
    except (KeyError, ValueError):
        return "Looks like the corpus you chose was too small. Try again"


def extract_rhyming_lines(cache):
    cleaned = []
    phoneme_dict = pronouncing.cmudict.dict()
    # Remove all comments not within the range and ensure that last word has a phonetic equivalent
    for comment in cache:
        if 20 < len(comment) < 100:
            lastword_search = re.search(r"([a-zA-Z]+)[^a-zA-Z]*$", comment)
            if lastword_search:
                word = lastword_search.groups()[0].lower()
                phonemes = phoneme_dict[word]
                if phonemes and not re.search(r"(?:ing|ed|ion)$", word) and not re.search(r"\d[^a-zA-Z]*$", comment):
                    cleaned.append((comment, word))

    # Create a dictionary of word subsets that rhyme. Ex: {-ight:{might, right, tight}
    # Note this is not an exact representation. It is a simplified explanation
    rhyme_subsets = {}
    for comment_pair in cleaned:
        word = comment_pair[1]
        rhyme_subset = pronouncing.rhyming_part(pronouncing.phones_for_word(word)[0])
        if rhyme_subset not in rhyme_subsets:
            rhyme_subsets[rhyme_subset] = [comment_pair]
        elif all(word != pairs[1] for pairs in rhyme_subsets[rhyme_subset]):  # Check to ensure that words don't repeat
            rhyme_subsets[rhyme_subset].append(comment_pair)

    return rhyme_subsets


def build_villanelle(corpus):
    # Selectively pick rhyme groups that fit the villanelle format and return the villanelle
    rhy_sec = extract_rhyming_lines(corpus)
    rhymes = [value for value in rhy_sec.values() if len(value) >= 7]
    poem = ""
    try:
        a_rhyme, b_rhyme = random.sample(rhymes, 2)
        a_1, a_2 = a_rhyme[0][0], a_rhyme[1][0]

        poem += f"{a_1}\n{b_rhyme[0][0]}\n{a_2}\n\n"
        poem += f"{a_rhyme[2][0]}\n{b_rhyme[1][0]}\n{a_1}\n\n"
        poem += f"{a_rhyme[3][0]}\n{b_rhyme[2][0]}\n{a_2}\n\n"
        poem += f"{a_rhyme[4][0]}\n{b_rhyme[3][0]}\n{a_1}\n\n"
        poem += f"{a_rhyme[5][0]}\n{b_rhyme[4][0]}\n{a_2}\n\n"
        poem += f"{a_rhyme[6][0]}\n{b_rhyme[5][0]}\n{a_1}\n{a_2}"
        return poem
    except ValueError:
        return "It appears like the corpus you chose was too small. Try again"


def build_acrostic(cache, key):
    # Dictionary in which key is first letter of the comment, and value is a list of comments that fit the requirement
    key = key.lower()
    first_letter_dict = {}
    cleaned = [comment for comment in cache if 20 < len(comment) < 100 and re.search(r"[a-zA-Z]", comment)]
    for comment in cleaned:
        first_letter = re.search(r"[a-zA-Z]", comment).group(0).lower()
        if first_letter not in first_letter_dict:
            first_letter_dict[first_letter] = [comment]
        else:
            first_letter_dict[first_letter].append(comment)

    # Build a poem with the letter dictionary we have
    poem = ""
    try:
        for index, letter in enumerate(key):
            letter_list = first_letter_dict[letter]
            if index != len(key)-1:
                poem += f"{pop_random(letter_list)}\n"
            else:
                poem += f"{pop_random(letter_list)}"
        return poem
    except (ValueError, KeyError):
        return "Looks like your corpus was too small. Try again?"


def get_syllable_count(word):
    # Return number of syllables or invalid
    pron_list = pronouncing.phones_for_word(word)
    if not pron_list:
        return "invalid"

    return pronouncing.syllable_count(pron_list[0])


def organize_syllables(cache):
    # Organize all comments with known syllables, by the sum of their syllables.
    sum_syl_dict = {}
    for comment in cache:
        words = re.findall(r"[a-zA-Z]+", comment)
        syl_count_comment = [get_syllable_count(word) for word in words]
        if syl_count_comment and "invalid" not in syl_count_comment and not re.search(r"\d", comment):
            total_syl = sum(syl_count_comment)
            if total_syl not in sum_syl_dict:
                sum_syl_dict[total_syl] = [comment]
            else:
                sum_syl_dict[total_syl].append(comment)

    return sum_syl_dict


def pop_random(info_list):
    # Given a list, pop a random element from it
    return info_list.pop(random.randrange(len(info_list)))
