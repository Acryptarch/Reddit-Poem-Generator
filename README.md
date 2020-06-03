# Reddit Poem Generator
Rpoems is a simple library that uses psaw (PushiftIO wrapper) and various different tactics to generate poetry from a corpus of reddit comments which are defined by various parameters.

## Requirements
- Python 3.6+

## Installing 
Install with:
```bash
pip install rpoems
```

# Documentation
An important method in this library is the build corpus method which generates a cache of comments given certain parameters
```python
import rpoems
from datetime import datetime as dt

before = dt(2018, 8, 22)
after = dt(2018, 8, 20)

corpus = rpoems.build_corpus(subreddit="AskReddit", before=before, after=after, limit=3000)

```

### Parameters
- `subreddit` `(str)`: The name of the subreddit you want to collect comments from. Defaults to `subreddit=""` which means that comments are collected from any subreddit. (Use at your own risk. I didn't implement a profanity filter)
- `before` `(datetime)`: Any comments collected will be before this data. Defaults to `before=datetime.datetime.now()` which means that any comment before the time this progam runs is fair game.
- `after` `(datetime)`: Any comments collected will be after this data. Defaults to `after=datetime.datetime(2000, 1, 1)`
- `limit` `(int)`: The maximum number of comments that will be collected. People tend to underestimate how many comments are present within a certain time-span. The default of `limit=2000` will be good enough for most poems
- `author` `(str)`: From which author should the comments be from. Defaults to `author=""`. This feature is not functioning as well as I hoped due to issues with the Pushshift API. Best not to use it.

```python
import rpoems
# For examples sake, I will build a different corpus, but you can definitely use the corpus from before.
corpus = rpoems.build_corpus(limit=2000)

# We now have many different types of poems we can build. I will go over one option in the coding example
poem = rpoems.couplet_rhyming_poem(corpus)
print(poem)
'''
We did it. Racism is no more. Have achieved world peace.
Tbh NES Ice Hockey player was one of my most wanted characters pre-release
and whatever you do, don't go to chauvin's florida address
you can't win in ace attorney, so it is not imperative for him to progress
Am I better off just getting BotW instead of Smash, then?
And my basic math skills have been foiled again...
'''
```
`couplet_rhyming_poem` is one method used to create a poem from a corpus. The others will be detailed below
### Poem Generating Methods
- `couplet_rhyming_poem(corpus)`: Generates a poem with rhyme scheme AABBCC given a corpus of comments
- `vilanelle(corpus)`: Generates a vilanelle given a corpus of comments
- `haiku(corpus)`: Generates a haiku given a corpus of comments
- `acrostic(corpus, key)`: Generates a poem in which the first letter of each line are the letters in `str` key in order
- `custom_rhyme(corpus, rhyme_scheme)`: Generates a poem given a corpus and a `str` rhyme_scheme
  - `rhyme_scheme` is a string of capital letters. Examples include "AABCC", "CCCDDD", "AAABBC", "ZZSSY"
- `custom_syl(corpus, syl_string)`: Generates a poem given a corpus and the amount of syllables in each line
  - `syl_string` is a `str` in which numbers are split by "-". Example inputs include "9-4-2", "1-2-3", "5-4-5"
- `tanka(corpus)`: Generates a poem with syllable sequence "5-7-5-7-7" given a corpus of comments
- `nonet(corpus)`: Generates a poem with a syllable sequence of "9-8-7-6-5-4-3-2-1" given a corpus of comments
- `magic_nine(corpus)`: Generates a poem with a rhyme scheme "ABACADABA" given a corpus of comments
- `all_alphabet(corpus)`: Generates a poem in which the first letter of each line is a letter of the alphabet in order
