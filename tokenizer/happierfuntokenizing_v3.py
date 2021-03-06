#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code implements a basic, Twitter-aware tokenizer.

A tokenizer is a function that splits a string of text into words. In
Python terms, we map string and unicode objects into lists of unicode
objects.

There is not a single right way to do tokenizing. The best method
depends on the application.  This tokenizer is designed to be flexible
and this easy to adapt to new domains and tasks.  The basic logic is
this:

1. The tuple regex_strings defines a list of regular expression
   strings.

2. The regex_strings strings are put, in order, into a compiled
   regular expression object called word_re.

3. The tokenization is done by word_re.findall(s), where s is the
   user-supplied string, inside the tokenize() method of the class
   Tokenizer.

4. When instantiating Tokenizer objects, there is a single option:
   preserve_case.  By default, it is set to True. If it is set to
   False, then the tokenizer will downcase everything except for
   emoticons.

The __main__ method illustrates by tokenizing a few examples.

I've also included a Tokenizer method tokenize_random_tweet(). If the
twitter library is installed (http://code.google.com/p/python-twitter/)
and Twitter is cooperating, then it should tokenize a random
English-language tweet.
"""

######################################################################

import re
import html.entities
######################################################################
# The following strings are components in the regular expression
# that is used for tokenizing. It's important that phone_number
# appears first in the final regex (since it can contain whitespace).
# It also could matter that tags comes after emoticons, due to the
# possibility of having text like
#
#     <:| and some text >:)
#
# Most imporatantly, the final element should always be last, since it
# does a last ditch whitespace-based tokenization of whatever is left.

# This particular element is used in a couple ways, so we define it
# with a name:
emoticon_string = r"""
    (?:
      [<>]?
      [:;=8>]                    # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpPxX/\:\}\{@\|\\] # mouth      
      |
      [\)\]\(\[dDpPxX/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8<]                    # eyes
      [<>]?
      |
      <[/\\]?3                         # heart(added: has)
      |
      \(?\(?\#?                   #left cheeck
      [>\-\^\*\+o\~]              #left eye
      [\_\.\|oO\,]                #nose
      [<\-\^\*\+o\~]              #right eye
      [\#\;]?\)?\)?               #right cheek
    )"""

# The components of the tokenizer:
regex_strings = (
    # Phone numbers:
    r"""
    (?:
      (?:            # (international)
        \+?[01]
        [\-\s.]*
      )?            
      (?:            # (area code)
        [\(]?
        \d{3}
        [\-\s.\)]*
      )?    
      \d{3}          # exchange
      [\-\s.]*   
      \d{4}          # base
    )"""
    ,
    # Emoticons:
    emoticon_string
    ,    
    # http:
    # Web Address:
    r"""(?:(?:http[s]?\:\/\/)?(?:[\w\_\-]+\.)+(?:com|net|gov|edu|info|org|ly|be|gl|co|gs|pr|me|cc|us|gd|nl|ws|am|im|fm|kr|to|jp|sg)(?:\/[\s\b$])?)"""
    ,
    r"""(?:http[s]?\:\/\/)"""   #need to capture it alone sometimes
    ,
    #command in parens:
    r"""(?:\[[\w_]+\])"""   #need to capture it alone sometimes
    ,
    # HTTP GET Info
    r"""(?:\/\w+\?(?:\;?\w+\=\w+)+)"""
    ,
    # HTML tags:
    r"""(?:<[^>]+\w=[^>]+>|<[^>]+\s\/>|<[^>\s]+>?|<?[^<\s]+>)"""
    #r"""(?:<[^>]+\w+[^>]+>|<[^>\s]+>?|<?[^<\s]+>)"""
    ,
    # Twitter username:
    r"""(?:@[\w_]+)"""
    ,
    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
    ,
    # Remaining word types:
    r"""
    (?:[\w][\w'\-_]+[\w])       # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots. 
    |
    (?:\S)                         # Everything else that isn't whitespace.
    """
    )

######################################################################
# This is the core tokenizing regex:
    
word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)

# The emoticon string gets its own regex so that we can preserve case for them as needed:
emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)

# These are for regularizing HTML entities to Unicode:
html_entity_digit_re = re.compile(r"&#\d+;")
html_entity_alpha_re = re.compile(r"&\w+;")
amp = "&amp;"

hex_re = re.compile(r'\\x[0-9a-z]{1,4}')

######################################################################

class Tokenizer:
    def __init__(self, preserve_case=False, use_unicode=True):
        self.preserve_case = preserve_case
        self.use_unicode = use_unicode

    def tokenize(self, s):
        """
        Argument: s -- any string or unicode object
        Value: a tokenize list of strings; conatenating this list returns the original string if preserve_case=False
        """        
        # Try to ensure unicode:
        if self.use_unicode:
            try:
                s = str(s)
            except UnicodeDecodeError:
                s = str(s).encode('string_escape')
                s = str(s)
        # Fix HTML character entitites:
        s = self.__html2unicode(s)
        s = self.__removeHex(s)
        # Tokenize:
        words = word_re.findall(s)
        #print words #debug
        # Possible alter the case, but avoid changing emoticons like :D into :d:
        if not self.preserve_case:            
            words = map((lambda x : x if emoticon_re.search(x) else x.lower()), words)
        
        return words


    def __html2unicode(self, s):
        """
        Internal metod that seeks to replace all the HTML entities in
        s with their corresponding unicode characters.
        """
        # First the digits:
        ents = set(html_entity_digit_re.findall(s))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    s = s.replace(ent, chr(entnum))	
                except:
                    pass
        # Now the alpha versions:
        ents = set(html_entity_alpha_re.findall(s))
        ents = filter((lambda x : x != amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:            
                s = s.replace(ent, chr(htmlentitydefs.name2codepoint[entname]))
            except:
                pass                    
            s = s.replace(amp, " and ")
        return s

    def __removeHex(self, s):
        return hex_re.sub(' ', s)


###############################################################################

if __name__ == '__main__':
    #tok = Tokenizer(preserve_case=True)
    #tok = Tokenizer(preserve_case=False)
    tokenizer = Tokenizer(use_unicode=self.use_unicode)

    import sys

    samples = (
        u"RT @ #happyfuncoding: this is a typical Twitter tweet :-)",
        u"It's perhaps noteworthy that phone numbers like +1 (800) 123-4567, (800) 123-4567, and 123-4567 are treated as words despite their whitespace.",
        u'Something </sarcasm> about <fails to break this up> <3 </3 <\\3 mañana vergüenza güenza création tonterías tonteréas <em class="grumpy">pain</em> <meta name="viewport" content="width=device-width"> <br />',
        u"This is more like a Facebook message with a url: http://www.youtube.com/watch?v=dQw4w9WgXcQ, youtube.com google.com https://google.com/ ",
        u"HTML entities &amp; other Web oddities can be an &aacute;cute <em class='grumpy'>pain</em> >:(",
        )

    if len(sys.argv) > 1 and (sys.argv[1]):
        samples = sys.argv[1:]

    for s in samples:
        print("======================================================================")
        print(s)
        tokenized = tok.tokenize(s)
        print("\n".join(tokenized).encode('utf8', 'ignore') if tok.use_unicode else "\n".join(tokenized))