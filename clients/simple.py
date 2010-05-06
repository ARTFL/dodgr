import loaders
import dico

loader = loaders.Separated('../data/test/test.tab')
test_dico = dico.Simple(loader)

print 'All entries:'
for entry in test_dico:
    print "Headword: ", entry[0], "Definition:", entry[1]
print

words = ['snort', 'dodger', 'not in there']

for word in words:
    definition = test_dico.define(word)
    if definition:
        print "Entry for '" + word + "':", definition
        print
    else:
        print "'" + word + "'", "is undefined"
        print
