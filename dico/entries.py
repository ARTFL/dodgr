"""entries.py
Dictionary entry models"""


class Entry(object):
    """A basic dictionary entry"""

    def __init__(self, prop_dict=None, prop_obj=None):
        """Build a dictionary entry from a dictionary of properties or an
        object with named properties. Headwords should be a list of tuples of
        (headword string, pos string). Examples is a list of strings. Other 
        properties are strings.
        
        prop stands for property (a reserved keyword)
        """

        self.props = ['headwords', 'content', 'examples', 'prons']

        if not (prop_dict or prop_obj):
            raise Exception('You must initialize the dico entry with'
                'either a prop_dict dictionary or prop_obj object.')

        if prop_dict:
            for prop in self.props:
                try:
                    setattr(self, prop, prop_dict[prop])
                except KeyError:
                    setattr(self, prop, None)
        elif prop_obj:
            for prop in self.props:
                setattr(self, prop, getattr(prob_obj, prop))

    def __len__(self):
        """Length of an entry is defined as the length of its content"""
        return len(self.content)

    def __iter__(self):
        """Not sure how useful it is to iterate over an entry's properties,
        but here it is"""
        for prop in self.props:
            yield getattr(self, prop)

    def __unicode__(self):
        """Unicode string representation for a dico entry"""

        entry = u'Headwords:\n'
        for hw in self.headwords:
            entry += hw[0] + ' (' + hw[1] + ')\n'
        if self.prons:
            entry += 'Prons: ' + ', '.join(self.prons) + '\n'
        if self.examples:
            entry += 'Examples:\n' + '\n'.join(self.examples) + '\n'
        if self.content:
            entry += 'Content:\n' + self.content
            
        return entry

    def __str__(self):
        """String representation for a dico entry"""

        return self.__unicode__().encode('utf-8')