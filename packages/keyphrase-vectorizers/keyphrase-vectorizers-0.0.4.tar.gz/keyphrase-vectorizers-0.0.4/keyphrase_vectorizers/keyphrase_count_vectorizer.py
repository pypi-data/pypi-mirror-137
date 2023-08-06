"""
.. _spaCy pipeline: https://spacy.io/models
.. _stopwords available in NLTK: https://github.com/nltk/nltk_data/blob/gh-pages/packages/corpora/stopwords.zip
.. _POS-tags: https://github.com/explosion/spaCy/blob/master/spacy/glossary.py
.. _regex pattern: https://docs.python.org/3/library/re.html#regular-expression-syntax
.. _spaCy part-of-speech tags: https://github.com/explosion/spaCy/blob/master/spacy/glossary.py
"""

import warnings
from typing import List

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.deprecation import deprecated

from keyphrase_vectorizers.keyphrase_vectorizer_mixin import _KeyphraseVectorizerMixin


class KeyphraseCountVectorizer(_KeyphraseVectorizerMixin, BaseEstimator):
    """
    KeyphraseCountVectorizer

    KeyphraseCountVectorizer converts a collection of text documents to a matrix of document-token counts.
    The tokens are keyphrases that are extracted from the text documents based on their part-of-speech tags.
    The matrix rows indicate the documents and columns indicate the unique keyphrases. Each cell represents the count.
    The part-of-speech pattern of keyphrases can be defined by the ``pos_pattern`` parameter.
    By default, keyphrases are extracted, that have 0 or more adjectives, followed by 1 or more nouns.
    A list of extracted keyphrases matching the defined part-of-speech pattern can be returned after fitting via :class:`get_feature_names_out()`.

    Attention:
        If the vectorizer is used for languages other than English, the ``spacy_pipeline`` and ``stop_words`` parameters
        must be customized accordingly.
        Additionally, the ``pos_pattern`` parameter has to be customized as the `spaCy part-of-speech tags`_  differ between languages.
        Without customizing, the words will be tagged with wrong part-of-speech tags and no stopwords will be considered.

    Parameters
    ----------
    spacy_pipeline : str, default='en_core_web_sm'
            The name of the `spaCy pipeline`_, used to tag the parts-of-speech in the text. Standard is the 'en' pipeline.

    pos_pattern :  str, default='<J.*>*<N.*>+'
        The `regex pattern`_ of `POS-tags`_ used to extract a sequence of POS-tagged tokens from the text.
        Standard is to only select keyphrases that have 0 or more adjectives, followed by 1 or more nouns.

    stop_words : str, default='english'
            Language of stopwords to remove from the document, e.g.'english.
            Supported options are `stopwords available in NLTK`_.
            Removes unwanted stopwords from keyphrases if 'stop_words' is not None.

    lowercase : bool, default=True
        Whether the returned keyphrases should be converted to lowercase.

    multiprocessing : bool, default=False
            Whether to use multiprocessing for spaCy part-of-speech tagging.
            If True, spaCy uses all cores to tag documents with part-of-speech.
            Depending on the platform, starting many processes with multiprocessing can add a lot of overhead.
            In particular, the default start method spawn used in macOS/OS X (as of Python 3.8) and in Windows can be slow.
            Therefore, carefully consider whether this option is really necessary.

    binary : bool, default=False
        If True, all non zero counts are set to 1.
        This is useful for discrete probabilistic models that model binary events rather than integer counts.

    dtype : type, default=np.int64
        Type of the matrix returned by fit_transform() or transform().
    """

    def __init__(self, spacy_pipeline: str = 'en_core_web_sm', pos_pattern: str = '<J.*>*<N.*>+',
                 stop_words: str = 'english', lowercase: bool = True, multiprocessing: bool = False,
                 binary: bool = False, dtype: np.dtype = np.int64):

        self.spacy_pipeline = spacy_pipeline
        self.pos_pattern = pos_pattern
        self.stop_words = stop_words
        self.lowercase = lowercase
        self.multiprocessing = multiprocessing
        self.binary = binary
        self.dtype = dtype

    def fit(self, raw_documents: List[str]) -> object:
        """
        Learn the keyphrases that match the defined part-of-speech pattern from the list of raw documents.

        Parameters
        ----------
        raw_documents : iterable
            An iterable of strings.

        Returns
        -------
        self : object
            Fitted vectorizer.
        """

        self.keyphrases = self._get_pos_keyphrases(document_list=raw_documents,
                                                   stop_words=self.stop_words,
                                                   spacy_pipeline=self.spacy_pipeline,
                                                   pos_pattern=self.pos_pattern,
                                                   lowercase=self.lowercase, multiprocessing=self.multiprocessing)

        # set n-gram range to zero if no keyphrases could be extracted
        if self.keyphrases:
            self.max_n_gram_length = max([len(keyphrase.split()) for keyphrase in self.keyphrases])
            self.min_n_gram_length = min([len(keyphrase.split()) for keyphrase in self.keyphrases])
        else:
            raise ValueError(
                "Empty keyphrases. Perhaps the documents do not contain keyphrases that match the 'pos_pattern' parameter or only contain stop words.")

        return self

    def fit_transform(self, raw_documents: List[str]) -> List[List[int]]:
        """
        Learn the keyphrases that match the defined part-of-speech pattern from the list of raw documents
        and return the document-keyphrase matrix.
        This is equivalent to fit followed by transform, but more efficiently implemented.

        Parameters
        ----------
        raw_documents : iterable
            An iterable of strings.

        Returns
        -------
        X : array of shape (n_samples, n_features)
            Document-keyphrase matrix.
        """

        self.keyphrases = self._get_pos_keyphrases(document_list=raw_documents,
                                                   stop_words=self.stop_words,
                                                   spacy_pipeline=self.spacy_pipeline,
                                                   pos_pattern=self.pos_pattern,
                                                   lowercase=self.lowercase, multiprocessing=self.multiprocessing)

        # set n-gram range to zero if no keyphrases could be extracted
        if self.keyphrases:
            self.max_n_gram_length = max([len(keyphrase.split()) for keyphrase in self.keyphrases])
            self.min_n_gram_length = min([len(keyphrase.split()) for keyphrase in self.keyphrases])
        else:
            raise ValueError(
                "Empty keyphrases. Perhaps the documents do not contain keyphrases that match the 'pos_pattern' parameter or only contain stop words.")

        return CountVectorizer(vocabulary=self.keyphrases, ngram_range=(self.min_n_gram_length, self.max_n_gram_length),
                               lowercase=self.lowercase, binary=self.binary, dtype=self.dtype).fit_transform(
            raw_documents=raw_documents)

    def transform(self, raw_documents: List[str]) -> List[List[int]]:
        """
        Transform documents to document-keyphrase matrix.
        Extract token counts out of raw text documents using the keyphrases
        fitted with fit.

        Parameters
        ----------
        raw_documents : iterable
            An iterable of strings.

        Returns
        -------
        X : sparse matrix of shape (n_samples, n_features)
            Document-keyphrase matrix.
        """

        # triggers a parameter validation
        if not hasattr(self, 'keyphrases'):
            raise NotFittedError("Keyphrases not fitted.")

        return CountVectorizer(vocabulary=self.keyphrases, ngram_range=(self.min_n_gram_length, self.max_n_gram_length),
                               lowercase=self.lowercase, binary=self.binary, dtype=self.dtype).transform(
            raw_documents=raw_documents)

    def inverse_transform(self, X: List[List[int]]) -> List[List[str]]:
        """
        Return keyphrases per document with nonzero entries in X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Document-keyphrase matrix.

        Returns
        -------
        X_inv : list of arrays of shape (n_samples,)
            List of arrays of keyphrase.
        """

        # triggers a parameter validation
        if not hasattr(self, 'keyphrases'):
            raise NotFittedError("Keyphrases not fitted.")

        return CountVectorizer(vocabulary=self.keyphrases, ngram_range=(self.min_n_gram_length, self.max_n_gram_length),
                               lowercase=self.lowercase, binary=self.binary, dtype=self.dtype).inverse_transform(X=X)

    @deprecated(
        "get_feature_names() is deprecated in scikit-learn 1.0 and will be removed "
        "with scikit-learn 1.2. Please use get_feature_names_out() instead."
    )
    def get_feature_names(self) -> List[str]:
        """
        Array mapping from feature integer indices to feature name.

        Returns
        -------
        feature_names : list
            A list of fitted keyphrases.
        """

        # triggers a parameter validation
        if not hasattr(self, 'keyphrases'):
            raise NotFittedError("Keyphrases not fitted.")

        # raise DeprecationWarning when function is removed from scikit-learn
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return CountVectorizer(vocabulary=self.keyphrases,
                                       ngram_range=(self.min_n_gram_length, self.max_n_gram_length),
                                       lowercase=self.lowercase, binary=self.binary,
                                       dtype=self.dtype).get_feature_names()
        except AttributeError:
            raise DeprecationWarning("get_feature_names() is deprecated. Please use 'get_feature_names_out()' instead.")

    def get_feature_names_out(self) -> np.array(str):
        """
        Get fitted keyphrases for transformation.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed keyphrases.
        """

        # triggers a parameter validation
        if not hasattr(self, 'keyphrases'):
            raise NotFittedError("Keyphrases not fitted.")

        return CountVectorizer(vocabulary=self.keyphrases, ngram_range=(self.min_n_gram_length, self.max_n_gram_length),
                               lowercase=self.lowercase, binary=self.binary, dtype=self.dtype).get_feature_names_out()
