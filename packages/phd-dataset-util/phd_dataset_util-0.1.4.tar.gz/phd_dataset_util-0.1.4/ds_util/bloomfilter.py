import xxhash
import nltk
import bitarray
import numpy as np

from ds_util import generate_ngrams


def create_bf(word,bf_len,k,bf_representation='binary'):
    """
        For a given string (representing a record), this method creates a new bloom filter.

        word : string to be encoded
        bf_len : bloom filter length
        k : number of hash function
        
        bf_representation : the re
            - binary (default) : the regular bf, a bitarray with 0 and 1's
            - pos1 : this represatation return a a integer list with the positions of ones in the filter

        It is important to mention that:
            - pos1 representation might generate filter of diferent lenght, requiring a regularization
    """
    assert bf_representation in ['binary', 'pos1']

    # gerando os ngrams
    ngrams = generate_ngrams(word)
    bf = []

    #filtro vazio
    if bf_representation == 'binary':
        bf = bitarray.bitarray(bf_len)
        bf.setall(0)

        for n_gram in ngrams:
            for seed in range(k):
                pos=xxhash.xxh64(n_gram, seed=seed).intdigest() % bf_len
                bf[pos] = 1
        # end binary bf
    elif bf_representation == 'pos1':
        for n_gram in ngrams:
            for seed in range(k):
                pos=xxhash.xxh64(n_gram, seed=seed).intdigest() % bf_len
                bf.append(pos)
        
        bf = np.unique(np.asarray(bf,dtype=np.uint16))
        # end pos1 bf

    return bf


def jaccard_similarity(filter1, filter2, bf_representation='binary'):

    """
        Calculates the jaccard index between 2 bloom filters

        - filter1 : bitarray.bitarray or list depending on the bf representation
        - filter2 : bitarray.bitarray or list depending on the bf representation

        return : number between 0 and 1
    """

    # Brasileiro, i've coded this part using this website [1]
    # Please check this, chunk of code. It may contain error :p
    # 1 -http://blog.demofox.org/2015/02/08/estimating-set-membership-with-a-bloom-filter/

    assert bf_representation in ['binary', 'pos1']

    if bf_representation=='binary':
        assert type(filter1) == bitarray.bitarray
        assert type(filter2) == bitarray.bitarray 

        intersection = (filter1 & filter2).count(True)
        union = (filter1 | filter2).count(True)
    elif bf_representation=='pos1':
        assert type(filter1) == np.ndarray
        assert type(filter2) == np.ndarray
        intersection = len(list(set(filter1).intersection(filter2)))
        union = (len(set(filter1)) + len(set(filter2))) - intersection

    
    if union == 0:
        return 0

    return float(intersection) / union


def fill_pos_bf(bf,new_bf_length):
    """
        To this representation be used in ML aplication it should have the same length.
        This method fills the pos bf with zeros at the end 
    """
    try:
        z = np.zeros(new_bf_length-len(bf))
    except ValueError:
        print(len(bf)) #corrigir aqui quado for menor
        print(new_bf_length)
    return np.concatenate((bf,z))