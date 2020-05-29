import datetime
import random
import re
import pronouncing
from psaw import PushshiftAPI


def build_corpus(subreddit="", before=datetime.datetime.now(), after=datetime.datetime(2000, 1, 1),
                 limit=1000, author=""):
    # Set up the generator that will build our corpus of comments
    corpus = []
    api = PushshiftAPI()
    gen = api.search_comments(before=int(before.timestamp()), after=int(after.timestamp()),
                              subreddit=subreddit, filter=['body'], limit=limit, author=author)

    for i in gen:
        comment = i.body
        cleaned_comment = re.sub(r"\s\s+", " ", comment)
        cleaned_comment = re.sub(r"\n", " ", cleaned_comment)
        corpus.append(cleaned_comment)

    return corpus


def couplet_rhyming_poem(corpus):
    rhymes = extract_rhymes(corpus)
    return build_rhyme_couplets(rhymes)


def villanelle(corpus):
    rhymes = extract_rhymes(corpus)
    return build_villanelle(rhymes)


def epigram(corpus, spell):
    return build_epigram(corpus, spell)


def haiku(corpus):
    return build_haiku(corpus)


def extract_rhymes(cache):
    cleaned = []
    phoneme_dict = pronouncing.cmudict.dict()
    # Remove all comments not within the range and ensure that last word has a phonetic equivalent
    for comment in cache:
        if 20 < len(comment) < 100:
            lastword_search = re.search(r"\b(\w+)\W*$", comment)
            if lastword_search is not None:
                word = lastword_search.groups()[0].lower()
                phonemes = phoneme_dict[word]
                if phonemes and re.search(r"(?:ing|ed|ion)$", word) is None:
                    cleaned.append((comment, word))

    # Create a dictionary of word subsets that rhyme.
    rhyme_sections = {}
    for comment_pair in cleaned:
        word = comment_pair[1]
        rhyme_sec = pronouncing.rhyming_part(pronouncing.phones_for_word(word)[0])
        if rhyme_sec not in rhyme_sections:
            rhyme_sections[rhyme_sec] = [comment_pair]
        elif all(word != pairs[1] for pairs in rhyme_sections[rhyme_sec]):
            rhyme_sections[rhyme_sec].append(comment_pair)

    return rhyme_sections


def build_rhyme_couplets(rhy_sec):
    # Select pairs of couplets that rhyme and return the poem built from them
    rhymes = [value for value in rhy_sec.values() if len(value) >= 2]
    chosen = random.sample(rhymes, 3)
    poem = "Rhyming Couplets\n"
    for i in chosen:
        couplet = random.sample(i, 2)
        poem += f"{couplet[0][0]}\n{couplet[1][0]}\n"
    return poem


def build_villanelle(rhy_sec):
    # Selectively pick rhyme groups that fit the villanelle format and return the villanelle
    rhymes = [value for value in rhy_sec.values() if len(value) >= 7]
    poem = "Villanelle\n"
    try:
        a_rhyme, b_rhyme = random.sample(rhymes, 2)
        a_1, a_2 = a_rhyme[0][0], a_rhyme[1][0]

        poem += f"{a_1}\n{b_rhyme[0][0]}\n{a_2}\n\n"
        poem += f"{a_rhyme[2][0]}\n{b_rhyme[1][0]}\n{a_1}\n\n"
        poem += f"{a_rhyme[3][0]}\n{b_rhyme[2][0]}\n{a_2}\n\n"
        poem += f"{a_rhyme[4][0]}\n{b_rhyme[3][0]}\n{a_1}\n\n"
        poem += f"{a_rhyme[5][0]}\n{b_rhyme[4][0]}\n{a_2}\n\n"
        poem += f"{a_rhyme[6][0]}\n{b_rhyme[5][0]}\n{a_1}\n{a_2}\n"
        return poem
    except ValueError:
        print("It appears like the corpus you chose was too small. Try again")


def build_epigram(cache, key):
    # Create a dictionary in which key is first letter of the comment, and value is the comment
    key = key.lower()
    key = ''.join(key.split())
    key = list(key)
    letter_dict = {}
    cleaned = [comment for comment in cache if 20 < len(comment) < 100 and re.search(r"\w", comment)]
    for comment in cleaned:
        first = re.search(r"\w", comment).group(0).lower()
        if first not in letter_dict:
            letter_dict[first] = [comment]
        else:
            letter_dict[first].append(comment)

    # Selectively pick letters that match up tho the key to the epigram and return the epigram
    poem = "Epigram\n"
    try:
        for letter in key:
            letter_list = letter_dict[letter]
            poem += f"{letter_list.pop(random.randrange(len(letter_list)))}\n"
        return poem
    except (ValueError, KeyError):
        print("Looks like your corpus was too small. Try again?")


def get_syllable_count(word):
    # Return number of syllables or invalid
    pron_list = pronouncing.phones_for_word(word)
    if not pron_list:
        return "invalid"

    return pronouncing.syllable_count(pron_list[0])


def build_haiku(cache):
    lines = []
    five_syl = []
    seven_syl = []

    # Pick comments that contain only words from cmudict
    for i in cache:
        trimmed = re.sub(r"[.,?:;!]", "", i)
        trimmed = trimmed.strip()
        words_exist = re.fullmatch(r"[\w\s]+", trimmed)
        if words_exist:
            lines.append(trimmed)

    # Organize comments into lists that are five syllables and seven syllables
    for comment in lines:
        words = re.findall(r"\w+", comment)
        syl_ndo = list(map(get_syllable_count, words))
        if "invalid" not in syl_ndo:
            syl_count = sum(syl_ndo)
            if syl_count == 5:
                five_syl.append(comment)
            if syl_count == 7:
                seven_syl.append(comment)

    # Build a haiku from our syllables lists and return it
    try:
        beg_end = random.sample(five_syl, 2)
        mid = random.sample(seven_syl, 1)
        poem = f"\nHaiku\n{beg_end[0]}\n{mid[0]}\n{beg_end[1]}\n"
        return poem
    except ValueError:
        print("Oops. Look like the corpus you choose was too small")


def check_iamb(comment):
    # Return if the words in the string is in iambic pentameter
    iamb = "01" * 5
    words = re.findall(r"\w+", comment)
    sum_stress = ""
    for word in words:
        if get_syllable_count(word.lower()) == "invalid":
            return False

        stress = pronouncing.stresses_for_word(word.lower())
        match_found = False
        for i in stress:
            if iamb.startswith(sum_stress + i):
                sum_stress += i
                match_found = True
                break
        if not match_found:
            return False
    if sum_stress == iamb:
        print(comment + "****" + sum_stress)
