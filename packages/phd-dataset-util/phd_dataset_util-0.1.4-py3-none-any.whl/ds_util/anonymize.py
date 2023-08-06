from multiprocessing import Pool

import numpy as np
import pandas as pd

import nltk

from ds_util.util import get_nearest_value
from ds_util.bloomfilter import create_bf, jaccard_similarity, fill_pos_bf


def anonymize_dataset(ldf,bf_len,k,bf_representation='binary'):
  """
    Aanonymize a dataset with a bloomfilter. 

    - ldf: dataset
    - bf_len: bloomfilter ength
    - k : number of hashfunction 
    - bf_representation [ binary, pos1 ]

  """
  saida =[]
  
  for row in ldf:
    id = row[0]
    bf = create_bf(row[1],bf_len,k,bf_representation=bf_representation)
    saida.append([id,bf])
  
  return saida

# TODO: Implement
# def parallel_anonymize_dataset(df,bf_len,k,bf_representation='binary',cores=2):
#   """
#     Aanonymize a dataset with a bloomfilter. 

#     - ldf: dataset
#     - bf_len: bloomfilter ength
#     - k : number of hashfunction 
#     - bf_representation [ binary, pos1 ]

#   """
#   nparts_df = np.array_split(df, cores)
  
#   params = []
#   for dfa in nparts_df:
#       params.append((dfa,bf_len,k)) #kargs

#   with Pool(processes=cores) as p:
#       r = p.map(anonymize_dataset,params)

#   return r

def rank_dataset(df_a,df_b,bf_representation='binary', bit_power=1):
  '''
    Sort the dataset according to the jaccard simillarity. This method also change
    binary bf represation. It convert the bitaary into np.array(uint8) to be used 
    as input to the classifiers
    
    - bit_power: (default=1), this method is used amplify the power of the signal in the bloomfilter

    return a dataset with ["id1","id2","bf1","bf2","sim","label"]
  '''

  ds = []

  for i in range(0,len(df_a)):
    for j in range(0,len(df_b)):
      id1 = df_a[i][0]
      id2 = df_b[j][0]

      bf1 = df_a[i][1]
      bf2 = df_b[j][1]

      sim = jaccard_similarity(bf1,bf2,bf_representation=bf_representation)

      
      if bf_representation == 'binary':

        bf1 = np.unpackbits(bf1)
        bf2 = np.unpackbits(bf2)

        if bit_power!=1:
          bf1 = bf1 * bit_power
          bf2 = bf2 * bit_power


      linha = [id1,id2,bf1,bf2,sim]
      
      if id1 == id2:
        # labels.append(np.array([1.]))
        linha.append(1)
      else:
        # labels.append(np.array([0]))
        linha.append(0)
      
      ds.append(linha)

  df = pd.DataFrame(ds)      
  df.columns = ["id1","id2","bf1","bf2","sim","label"]
  return df


def extract_sample_from_anonymized(rdf,sample_method='random1',
                                    num_of_random_sample=1,
                                    num_of_negative_example_per_sample=1
                                ):
    """
        - rdf : ranked dataframe
        - sample_mentod
            - random1 : select x (num_of_random_sample * num_of_negative_example_per_sample, default 1) records random from each non matches
            - maxq13 : select x (4 * num_of_negative_example_per_sample) records pairs. From max, quantile 1, median and quantile 3 similarity values
        - num_of_random_sample : number of random sample in random1
        - num_of_negative_example_per_sample: numper of negative example per each positive example

    """
    assert sample_method in ['random1','maxq13']
    ids = rdf.id1.unique()
    sample_df = []

    id = ids[0]

    for id in ids:
        #non matches df
        df_nm = rdf[(rdf.id1 == id) & (rdf.label != 1)] # no_match
        df_m = rdf[(rdf.id1 == id) & (rdf.label == 1)]  # match

        if len(df_m) != 0:
            sample_df.append(df_m.to_numpy()[0]) # remover
            #add no match sample 
            if sample_method == 'random1':
                unique_sim = df_nm.sim.unique()
                sample_unique_sim = np.random.choice(unique_sim,num_of_random_sample)
                for i in sample_unique_sim:
                    s = df_nm[df_nm.sim ==i].sample(num_of_negative_example_per_sample,replace=True)
                    sample_df.append(s.to_numpy()[0])

            elif sample_method == 'maxq13':

                sim_values = df_nm.sim.unique()
                q1 = get_nearest_value(sim_values, df_nm.sim.quantile(0.25))
                me = get_nearest_value(sim_values, df_nm.sim.median())
                q3 = get_nearest_value(sim_values, df_nm.sim.quantile(0.75))
                ma = get_nearest_value(sim_values, df_nm.sim.max())

                for v in [q1,me,q3,ma]:
                    sample_cand = df_nm[df_nm.sim == q3]

                    if len(sample_cand) <= num_of_negative_example_per_sample: # caso o sample_cand nao tenha o numero suficiente de amostras
                        sample_df.append(sample_cand.to_numpy()[0])
                    else: # remove um sample
                        temp = sample_cand.sample(num_of_negative_example_per_sample)
                        sample_df.append(temp.to_numpy()[0])
        else:
          #colocar exemplos negativos
          pass
          if sample_method == 'random1':
            unique_sim = df_nm.sim.unique()
            sample_unique_sim = np.random.choice(unique_sim,num_of_random_sample)
            for i in sample_unique_sim:
              s = df_nm[df_nm.sim ==i].sample(num_of_negative_example_per_sample,replace=True)
              sample_df.append(s.to_numpy()[0])
          elif sample_method == 'maxq13':
            sim_values = df_nm.sim.unique()
            q1 = get_nearest_value(sim_values, df_nm.sim.quantile(0.25))
            me = get_nearest_value(sim_values, df_nm.sim.median())
            q3 = get_nearest_value(sim_values, df_nm.sim.quantile(0.75))
            ma = get_nearest_value(sim_values, df_nm.sim.max())

            for v in [q1,me,q3,ma]:
              sample_cand = df_nm[df_nm.sim == q3]
              if len(sample_cand) <= num_of_negative_example_per_sample: # caso o sample_cand nao tenha o numero suficiente de amostras
                sample_df.append(sample_cand.to_numpy()[0])
              else: # remove um sample
                temp = sample_cand.sample(num_of_negative_example_per_sample)
                sample_df.append(temp.to_numpy()[0])
  
    sample_df = pd.DataFrame(sample_df)
    sample_df.columns = ['id1','id2','bf1','bf2','sim','label']
    return sample_df


def fill_all_posbf(ds,len_max):
    """
      Fill all pos bf to the maximum length
    """
    s = np.asarray(ds)
    l = []
    r = []
    label = []

    for i in range(0,len(s)):    
        bf1 = fill_pos_bf(s[i][2],len_max)
        bf2 = fill_pos_bf(s[i][3],len_max)
        l.append(bf1)
        r.append(bf2)
        label.append(s[i][5])
        
    x = [np.asarray(l),np.asarray(r)]
    y =  np.asarray(ds.label)

    return x,y

def get_max_length_posbf(d1:np.array):
    """
     This method return the number of element of the larger pos bf
     - d1 (np.array) with the bloom filters
    """
    len_max = 0
    for i in range(0,len(d1)):
      if len(d1[i]) > len_max:
        len_max = len(d1[i])
    
    return len_max