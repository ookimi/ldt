# -*- coding: utf-8 -*-
""" Various resources

Various resources of LDT are loaded and available for use elsewhere.

Todo:

    * pylint,
    * unittests

"""

import os

from nltk.corpus import stopwords
# import ldt.load_config.
from ldt.load_config import config as config
from ldt.helpers.exceptions import LanguageError
from ldt.helpers.loading import load_resource as load_resource
#from ldt.helpers import loading

# import ldt.helpers.loading


def lookup_language(language, reverse=False):
    """

    LDT uses mainly 2-letter language codes for language settings; they are
    also used in Wiktionary abd BabelNet. This function converts canonical
    language names to codes and vice versa.

    Args:
        language (str): a `2-letter language code <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages#Two-letter_codes>`_
        reverse (bool): if True, returns the language code for the language

    Returns:
        (str): the canonical name of that language

    Raises:
        LanguageError: the language was not found
    """
    # lang_dict = ldt.helpers.loading.load_resource(path=os.path.join(
    #     config["path_to_resources"], "language_codes.yaml"), lowercasing=False,
    #     format="yaml")
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "generic_files/language_codes.yaml")
    lang_dict = load_resource(file_path, lowercasing=False, format="yaml")
    if not reverse:
        try:
            return lang_dict[language]
        except KeyError:
            raise LanguageError(lang_dict[language] +
                                ": no such language code defined. If it is  "
                                "supposed to be supported, check the "
                                "definition in the file " + file_path)
    else:
        if not language[0].isupper():
            language = language.capitalize()
        for k in lang_dict.keys():
            if lang_dict[k] == language:
                return k
        raise LanguageError(language + ": no such language defined. If it is "
                                       "supposed to be supported, check the "
                                       "definition in the file " + file_path)

def load_stopwords(language):

    """
    A function to load NLTK stopword lists for the supported languages. At
    the moment, that includes danish, dutch, english, finnish, french,
    german, hungarian, italian, norwegian, portuguese, russian, spanish,
    swedish, turkish

    Args:
        language (str): the language for which NLTK stopwords should be loaded

    Returns:
        (frozenset): the set of stopwords
    """

    if len(language) == 2:
        language = lookup_language(language).lower()
    try:
        stopWords = frozenset(stopwords.words(language))
        return stopWords
    except OSError:
        return frozenset()

def update_dict(dict1, dict2):
    """Helper for :meth:`_productive_morphology`."""
    for field in dict1:
        if field in dict2:
            dict1[field] += dict2[field]
    for field in dict2:
        if not field in dict1:
            dict1[field] = dict2[field]
    for field in dict1:
        if dict1[field]:
            dict1[field] = list(set(dict1[field]))
    return dict1
