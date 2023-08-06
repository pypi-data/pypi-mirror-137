import numpy as np
import pandas as pd
import nltk

def generate_ngrams(word,ngrams=2,pad=False):
    """
    Generate (plain ngrams) of a string (word)
    """
    if pad:
        grams =  nltk.ngrams(word, ngrams,pad_left=True, pad_right=True,left_pad_symbol='$',right_pad_symbol='$')
    else:
        grams = nltk.ngrams(word, ngrams)
    saida = []

    # try:
    for gram in grams:
        saida.append(''.join(str(gram)))
    # except TypeError:
    #     print(type(word))
    #     print(word)
        # print(list(grams))
        # print(saida)

  
    return saida

def pre_process_raw(df,atts,ngrams=2,pad=False):
    """
        Pre-processing raw data: generate the bi-grams to be anonymized
        - remove spaces

        return: the preprocessed dataset the mand and maximum number (maior) of ngram in the dataset
    """
    ldf = []
    maior = 0
    soma_media = 0
    count = 0

    for row in df.iterrows():
        id = row[1][0]
        qid = ''
        for i in range(1,len(atts)):
            try:
                for w in row[1][i].split(): #removendo espacos
                    qid += str(w)
            except AttributeError:
                qid += str(row[1][i])
        
        #
        qid = str(qid)
        
        n_grams = generate_ngrams(qid,ngrams=ngrams,pad=pad)
        soma_media += len(n_grams)
        count += 1

        if len(n_grams) >  maior:
            maior = len(n_grams)

        ldf.append([id,qid])

    media_ngram = int(soma_media/count)
    return ldf, media_ngram, maior

def extract_sample(df1,sample_size,duplicate_rate=0.1,
                    df2=[],
                    return_raw_sample=False,
                    atts='all'):
    """
        Extract a sample from a dataset (or a pair of dataset, if df2 parameter is set)
        - sample_size : number of records
        - duplicate_rate: percent of duplicated (0...1)
        - df2: the second dataset to be extracted
        - return_raw_sample (default False): return the raw sample, for debug.
        - atts

        return df_a,df_b,mean_ngram,max_ngram ( raw_dfa, raw_dfb )
    """
    assert duplicate_rate <= 1
    assert duplicate_rate > 0

    num_of_duplicated_records_df_b = int(sample_size * duplicate_rate)
    num_of_no_duplicated_records_df_b = sample_size - num_of_duplicated_records_df_b
    
    df_a = df1.sample(sample_size)
    if len(df2) == 0:
        df_b = pd.concat([df1.sample(num_of_no_duplicated_records_df_b),
                            df_a.sample(num_of_duplicated_records_df_b) #corrigido
                        ])
    else:
        df_b = pd.concat([df2.sample(num_of_no_duplicated_records_df_b),
                            df_a.sample(num_of_duplicated_records_df_b)
                        ])

    #seleciona attributos
    if type(atts) != list:
        atts = list(df_a.columns)
    else:
        #filter attributes
        df_a = df_a[atts]
        df_b = df_b[atts]

    #preprocessa os dados
    df_a_proc , df_a_mean_ngram, df_a_max_ngram = pre_process_raw(df_a,atts)
    df_b_proc , df_b_mean_ngram, df_b_max_ngram = pre_process_raw(df_b,atts)
    #max and mean number of ngram in the sample
    max_ngram = max(df_a_max_ngram,df_a_max_ngram)
    mean_ngram = int( (df_a_mean_ngram+df_b_mean_ngram)/2 )

    if return_raw_sample:
        return df_a_proc,df_b_proc,mean_ngram,max_ngram,df_a,df_b
    else:
        return df_a_proc,df_b_proc,mean_ngram,max_ngram

