import rpoems
# For examples sake, I will build a different corpus, but you can definitely use the corpus from before.
corpus = rpoems.build_corpus(subreddit="smashbros", limit=2000)

# We now have many different types of poems we can build. I will go over one option in the coding example
poem = rpoems.couplet_rhyming_poem(corpus)
print(poem)
