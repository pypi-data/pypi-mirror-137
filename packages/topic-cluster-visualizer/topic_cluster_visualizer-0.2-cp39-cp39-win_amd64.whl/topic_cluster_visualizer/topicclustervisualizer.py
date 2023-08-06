####u is word, v is topic
####j is word, i is topic
####w is word, z is topic

from math import *

import re
import time
import itertools

import numpy as np
import pandas as pd

import nltk
from nltk.stem import PorterStemmer
#from nltk.corpus import stopwords

from gensim.models import Word2Vec, KeyedVectors
from collections import Counter

from tqdm.auto import tqdm, trange

from factor_analyzer import Rotator

from functionc import onepl_lsrm_cont_missing

import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class TopicClusterVisualizer:
    def __init__(self, target_data):
        self.filter_terms = {'p.001', 'find', 'z9.738', 'n102', 'p0.0001', 'p.05', 'p0.03', 'n1427', 'sd', 'coronaviru', 'case',
                             'number', 'studi', 'date', 'result', 'hope', 'refer', 'major', 'b', 'n', 'besid', 'ie', 'l.', 'fact',
                             'e.g.', 'h', 'p', 'half', 'virus', 'viru', 'disease', 'coronavirus', 'data', 'rate', 'factor',
                             'method', 'test', 'model', 'analysis', 'health', 'death', 'measure'}
        
        self.corpus = None
        
        self.target_data = target_data
        
        self.vector_size = 256
        self.window = 3
        self.min_count = 1
        self.worker = 4
        self.sg = 1
        self.negative = 20

        self.epochs = 1

        self.near_term_topn_val = 10
        
    ##### 1.

    def _get_terms(self, text):
        
        ps = PorterStemmer()
        #stopwords = set(stopwords.words('english'))
        
        filter_terms = self.filter_terms
        
        def clean(text): 
            return re.sub(r'[^a-zA-Z0-9\-]', ' ', text).lower()

        def word_tokenize(text): 
            return nltk.word_tokenize(text)

        def pos_tagging(tokens, pos_filter={"NN", "JJ"}):
            tagged = nltk.pos_tag(tokens)
            nouns = [w for (w, pos) in tagged if pos[:2] in pos_filter]
            meaningful = [w for (w, pos) in tagged if pos[:2] in "JJ" and "-" in w]
            return nouns + meaningful

        def stemming(tokens): 
            return [ps.stem(t) for t in tokens]

        def filtering(tokens): 
            return [t for t in tokens if t not in filter_terms]
        
        text = clean(text)
        tokens = word_tokenize(text)
        nouns = pos_tagging(tokens)
        stemmed = stemming(nouns)
        filtered = filtering(stemmed)

        return ",".join(filtered) if filtered else stemmed

    def _train_corpus(self, corpus, train_data, keywords):
        
        near_term_topn_val = self.near_term_topn_val

        corpus_4_train = [lst.split(",") for lst in train_data if lst]

        model = Word2Vec(sentences=corpus_4_train, 
                        
                        size=self.vector_size, 
                        window=self.window,
                        min_count=self.min_count, 
                        workers=self.worker, 
                        sg=self.sg, 
                        negative=self.negative,
                        
                        iter=self.epochs)

        def nearest_terms_func(term, near_term_topn):
            if term in model.wv.vocab: 
                return [x[0] for x in model.wv.most_similar(term, topn=near_term_topn)]
            return []

        min_freq = 3

        total_abs_terms = [word for words in corpus if words for word in words]
        abs_terms = [term for term, freq in Counter(total_abs_terms).items() if freq >= min_freq]

        total_kwd_terms = [word for words in keywords.values if words for word in words.split(",")]
        kwd_terms = [term for term, freq in Counter(total_kwd_terms).items() if freq >= min_freq]

        print("# total terms: before train corpus - {:,}, keywords - {:,}".format(len(total_abs_terms), len(total_kwd_terms)))
        print("# used terms for corpus: before train corpus - {:,}, keywords - {:,}".format(len(abs_terms), len(kwd_terms)))

        nearest_terms = set()
        for term in kwd_terms:
            terms = nearest_terms_func(term, near_term_topn_val)
            if terms:
                nearest_terms.update(terms)

        # 키워드 기반으로, word2vec 에서 단어로 선정된 애들 중에서 각 키워드들이랑 가까운 단어만 엄선해서 얘들로 새로운 앱스트랙 재료 (vocab3) 
        # 만들고 각 앱스트랙의 tokened 단어들 중 이 vocab3에 들어있을 경우에만 생존시킨다

        terms = set(abs_terms) & set(nearest_terms)
        vocab_set = set(terms)

        trained_corpus = corpus.map(lambda x: set(x) & vocab_set).map(lambda x: list(x))
        
        return trained_corpus
    
    
    def preprocess(self, train_data = None, keywords = None, train = False):
        
        try:
            target_data=pd.Series(self.target_data)
        except ValueError:
            print("Input data need to be pandas.Series.")

        print("# raw data: {:,}".format(target_data.shape[0]))
        
        corpus = target_data.dropna().map(lambda x: self._get_terms(x)).dropna().str.split(",")
        
        if train:
            train_data = pd.Series(train_data).dropna().map(lambda x: self._get_terms(x))
            keywords = pd.Series(keywords).dropna().map(lambda x: self._get_terms(x))
            
            if (not train_data.empty) + (not keywords.empty) == 1:
                print("No train data or keywords. Return non-trained corpus. Saved in .corpus attribute.")
                self.corpus = corpus
            print("Return trained corpus. Saved in .corpus attribute.")
            self.corpus = self._train_corpus(corpus, train_data, keywords)
        
        else:
            print("Return non-trained corpus. Saved in .corpus attribute.")
            self.corpus = corpus
        
        

        
    ##### 2.
            
    def _gibbs_sampler_LDA(self, niter, V, B, num_topics, b, alpha=1., beta=0.1):
        print ("======= Biterm model =======")
        print ("Corpus length: " + str(len(b)))
        print ("Number of topics: " + str(num_topics))
        print ("alpha: " + str(alpha) + " beta: " + str(beta))
        
        
        
        Z =  np.zeros(B, dtype=int)
        Nwz = np.zeros((V, num_topics), dtype=int)
        Nz = np.zeros(num_topics, dtype=int)

        theta = np.random.dirichlet([alpha]*num_topics, 1)[0]
        
        print()
        
        for ibi, bi in tqdm(enumerate(b), total = len(b), position=0, leave=True, desc = "Sampling Nwz, Nz"):
            topics = np.random.choice(num_topics, 1, p=theta)[0]
            Nwz[bi[0], topics] += 1
            Nwz[bi[1], topics] += 1
            Nz[topics] += 1
            Z[ibi] = topics
            
        for it in range(niter):
            print()
            
            print("Iteration: " + str(it + 1) + "/" + str(niter))
            Nzold = np.copy(Nz)
            
            for ibi, bi in tqdm(enumerate(b), total = len(b), position=0, leave=True, desc = "Gibbs Sampling parameter"):
                Nwz[bi[0], Z[ibi]] -= 1
                Nwz[bi[1], Z[ibi]] -= 1
                Nz[Z[ibi]] -= 1
                pz = (Nz + alpha)*(Nwz[bi[0],:]+beta)*(Nwz[bi[1],:]+beta)/(Nwz.sum(axis=0)+beta*V)**2
                pz = pz/pz.sum()
                Z[ibi] = np.random.choice(num_topics, 1, p=pz)
                Nwz[bi[0], Z[ibi]] += 1
                Nwz[bi[1], Z[ibi]] += 1
                Nz[Z[ibi]] += 1      
            print ("Variation between iterations:  " + str(np.sqrt(np.sum((Nz-Nzold)**2))))

        return Nz, Nwz, Z
    
    def _pbd(self, doc, names): #probability of biterm in document. 
        ret = []
        retnames = []
        for term1 in set(doc):
            cnts = 0
            for term2 in doc:
                if term1 == term2: cnts +=1
            ret.append(cnts/len(doc))
            retnames.append(term1)
        if names: return retnames
        else: return ret
    
    def _BTM(self, tokenized_docs, niter, num_topics #TODO
            , alpha, beta):

        for _ in tqdm(["a"], position=0, leave=True, desc = "Preprocessing…"):
            tokenized_docs = pd.Series([text for text in tokenized_docs if len(tokenized_docs)>3]).dropna()
            N = len(tokenized_docs)
            
            dictionary = np.array(pd.Series(list(set([word for text in tokenized_docs for word in text]))).dropna())
            V = len(dictionary)

            btmp = [[(np.where(dictionary==word1)[0][0], np.where(dictionary==word2)[0][0]) 
                        for iword1, word1 in enumerate(text) for iword2, word2 in enumerate(text) if iword1 < iword2] 
                    for text in tokenized_docs]

            b = list(itertools.chain(*btmp))
            B = len(b)

        Nz, Nwz, Z = self._gibbs_sampler_LDA(niter=niter, V=V, B=B, num_topics=num_topics, b=b, alpha=alpha, beta=beta) #//TODO

        phiwz = (Nwz)/np.tile((Nwz.sum(axis=0)+V*beta),(V,1))
        thetaz = (Nz + alpha)/(B + num_topics*alpha)
        
        word_coefvar = np.std(phiwz, axis = 1)/np.mean(phiwz, axis = 1)
        word_maxprob = np.max(phiwz, axis=1)
        
        return {"phiwz":phiwz, "thetaz":thetaz, "dictionary":dictionary, 
                "word_coefvar":word_coefvar, "word_maxprob":word_maxprob
                }


    ##### 3.
    
    def _LSIRM(self, 
               
               phiwz, 
               dictionary, 
               word_maxprob,
               
               num_percentage,
               ndim, niter, nburn, nthin, nprint,
               
               jump_beta,
               jump_theta,
               jump_gamma,
               jump_z,
               jump_w,
               
               pr_mean_beta,
               pr_sd_beta,
               pr_a_th_sigma,
               pr_b_th_sigma,
               pr_mean_theta,
               pr_a_sigma,
               pr_b_sigma,
               pr_mean_gamma,
               pr_sd_gamma,
               
               missing):

        ##### 3_1. 
        
        #phiwz = self.phiwz
        percentage_range = [i for i in range(50 - num_percentage//2, 50 + num_percentage//2 + 1)][::-1]

        dict_per_perc = []
        data_per_perc = []

        for curr_perc in percentage_range:

            nchosen = int(np.percentile(np.argsort(word_maxprob), curr_perc)) #FIX
            argchosen = np.argsort(word_maxprob)[:nchosen]
            
            dict_per_perc.append(dictionary[argchosen])
            data_per_perc.append(phiwz[argchosen, :])

        #logit_x = log(data_m / (1 - data_m))
        #data_np = np.log(data_m / (1 - data_m))

        output_per_perc = []
        #output_new_per_perc = []

        print()
        
        for idata, data in tqdm(enumerate(data_per_perc), total = len(data_per_perc),
                                position=0, leave=True, desc = "LSIRM per perc"):
            
            print()

            # Set 99 as missing
            output2 = onepl_lsrm_cont_missing(data,
                                              
                                              ndim, niter, nburn, nthin, nprint,
                                              
                                              jump_beta, jump_theta, jump_gamma, jump_z, jump_w,
                                              
                                              pr_mean_beta, pr_sd_beta, pr_a_th_sigma, pr_b_th_sigma, 
                                              pr_mean_theta, pr_a_sigma, pr_b_sigma, pr_mean_gamma, 
                                              pr_sd_gamma,
                                              
                                              missing)
              
            output = {}

            output["beta"] = output2[0]
            output["theta"] = output2[1]
            output["w"] = output2[2]
            output["z"] = output2[3]
            output["gamma"] = output2[4]
            output["sigma_theta"] = output2[5]
            output["sigma"] = output2[6]
            output["map"] = output2[7]
            output["accept_beta"] = output2[8]
            output["accept_theta"] = output2[9]
            output["accept_w"] = output2[10]
            output["accept_z"] = output2[11]
            output["accept_gamma"] = output2[12][0]
            output["phiwz"] = data_per_perc[idata]
            output["words"] = dict_per_perc[idata]
            output["percentile"] = percentage_range[idata]
            
            
            output_per_perc.append(output)
        
        return percentage_range, output_per_perc
    
    def _procrustes_mine(self, X, X_star):
        
        n, m = X.shape
        J = np.identity(n)

        C = X_star.transpose() @ J @ X

        svd_out = np.linalg.svd(C)

        R = svd_out[2] @ svd_out[0].transpose()
        s = 1

        tt = np.zeros((m, 1))

        X_new = s * X @ R + np.full((n, m), tt.transpose())
        return X_new
    
    def _proc2(self, niter, nburn, nthin, ndim, outputs):
        
        #proc_within
        
        output_new_per_perc = []
        
        
        
        for ioutput, output in enumerate(outputs):
            
            phiwz = output["phiwz"]
            
            nsample, nitem = phiwz.shape
            nmcmc = int((niter - nburn) / nthin) 
        
            print("\n" + "current Matrix under procrustes within: " + str(ioutput+1) + "/" + str(len(outputs)))
            
            max_address = np.argmax(output['map'])
            
            w_star = output['w'][max_address, :, :]
            z_star = output['z'][max_address, :, :]
            
            w_proc = np.zeros((nmcmc, nsample, ndim), )
            z_proc = np.zeros((nmcmc, nitem, ndim), )
            
            for iter in trange(nmcmc, position=0, leave=True, desc = "Procrustes within"):

                w_iter = output['w'][iter, :, :]

                if iter != max_address:
                    w_proc[iter, :, :] = self._procrustes_mine(w_iter, w_star) 
                else:
                    w_proc[iter, :, :] = w_iter

                z_iter = output['z'][iter, :, :]

                if iter != max_address:
                    z_proc[iter, :, :] = self._procrustes_mine(z_iter, z_star)
                else:
                    z_proc[iter, :, :] = z_iter


            w_est = np.empty((nsample, ndim,), )

            for k in trange(nsample, position=0, leave=True, desc = "derive estimated w"):
                for j in range(ndim):
                    w_est[k, j] = w_proc[:, k, j].mean()


            z_est = np.empty((nitem, ndim), )

            for i in trange(nitem, position=0, leave=True, desc = "derive estimated z"):
                for j in range(ndim):
                    z_est[i, j] = z_proc[:, i, j].mean()

                    
            beta_est = output["beta"].mean(axis = 0)
            theta_est = output["theta"].mean(axis = 0)
            sigma_theta_est = output["sigma_theta"].mean()
            gamma_est = output["gamma"].mean()
            
            output_new = {"beta_estimate": beta_est,
                        "theta_estimate": theta_est,
                        "sigma_theta_estimate": sigma_theta_est,
                        "gamma_estimate": gamma_est,
                        
                        "z_estimate": z_est,
                        "w_estimate": w_est,
                        
                        "beta": output["beta"],
                        "theta": output["theta"],
                        "theta_sd": output["sigma_theta"],
                        "gamma": output["gamma"],
                        
                        "z": z_proc,
                        "w": w_proc,
                        
                        "accept_beta": output["accept_beta"],
                        "accept_theta": output["accept_theta"],
                        "accept_w": output["accept_w"],
                        "accept_z": output["accept_z"],
                        "accept_gamma": output["accept_gamma"],
                        
                        "words": output["words"]
                        }
            
            output_new_per_perc.append(output_new)
        
        #proc_bw
        
        dist_ratio_per_perc = [1]

        dist_old = np.sum(np.sqrt(np.sum(output_new_per_perc[0]["z_estimate"] ** 2, axis=1)))

        for output_new in output_new_per_perc[1:]:

            dist_new = np.sum(np.sqrt(np.sum(output_new["z_estimate"] ** 2, axis=1)))
            dist_ratio_per_perc.append(dist_new/dist_old)
            dist_old = dist_new

        iamax = np.argmax(dist_ratio_per_perc)
        
        proc2_zs = []
        
        

        for index, output in enumerate(output_new_per_perc):
            if index == iamax:
                proc2_zs.append(output["z_estimate"])
            else:
                proc2_zs.append(self._procrustes_mine(output["z_estimate"], 
                                                      output_new_per_perc[iamax]["z_estimate"]))
        
        return {"iamax":iamax, "proc2_zs":proc2_zs, "amax_data": output_new_per_perc[iamax]}



    def _oblimin(self, proc2s):
        oblimin_proc2_zs = []
        
        rotator = Rotator(method = "oblimin")
        for proc2_z in proc2s:
            oblimin_proc2_zs.append(rotator.fit_transform(proc2_z))
        
        return oblimin_proc2_zs

        

    def most_words_per_topic(self, a_i, nchoice = 30):

        a_i_wz = a_i["w_estimate"] @ a_i["z_estimate"].transpose()

        mwpt = []

        for j in range(a_i_wz.shape[1]):
            mwpt.append(a_i["words"][np.argsort(-a_i_wz[:,j])[:nchoice]])
        
        return mwpt
    
    


    def fit(self, 
            
            niter1 = 20,
            #nburn1 = 0,
            #nthin1 = 1
            num_topics1 = 20,
            alpha1 = 1.0,
            beta1 = 0.1,
            
            num_percentage2 = 21,
            
            ndim2 = 2, niter2 = 55000, nburn2 = 5000, nthin2 = 5, nprint2 = 5000,
            
            jump_beta2 = 0.28,
            jump_theta2 = 1.0,
            jump_gamma2 = 0.01,
            jump_z2 = 0.06,
            jump_w2 = 0.06,
            pr_mean_beta2 = 0,
            pr_sd_beta2 = 1,
            pr_a_th_sigma2 = 0.001,
            pr_b_th_sigma2 = 0.001,
            pr_mean_theta2 = 0,
            pr_a_sigma2 = 0.001,
            pr_b_sigma2 = 0.001,
            pr_mean_gamma2 = 0.0,
            pr_sd_gamma2 = 1.0,
            
            missing2 = 99):
        
        start = time.time()
        
        tokenized_docs = self.corpus
        
        btm = self._BTM(tokenized_docs, 
                        niter = niter1, 
                        num_topics = num_topics1, 
                        alpha = alpha1, 
                        beta = beta1)
        
        
        #btm["phiwz"] = np.log(btm["phiwz"] / (1-btm["phiwz"]))
        


        """
        모든 topic의 분포는 theta ~ 디리클레 알파를 따름

        biterm 총체 B에서 biterm b를 뽑으면, 이 biterm이 어느 topic z에 속할지는 z ~ 다항분포 세타

        topic z의 topic-word 분포는 phi_z ~ 디리클레 베타를 따름
        topic = z, word = w. z가 정해졌을 때 이로부터 각 단어가 가지는 확률을 모아서 set으로 한것이 phi_z.

        골라진 topic에 대응하는 topic-word 분포로부터 단어 2개가 골라질 확률은 w_i, w_j ~ 다항(phi_z)를 따름
        """


        
        percentage_range, lsirm = self._LSIRM(phiwz = btm["phiwz"], 
                            dictionary = btm["dictionary"], 
                            word_maxprob = btm["word_maxprob"],
                            
                            num_percentage = num_percentage2,
                            ndim = ndim2, 
                            niter = niter2, 
                            nburn = nburn2, 
                            nthin = nthin2, 
                            nprint = nprint2,
                            
                            jump_beta = jump_beta2,
                            jump_theta = jump_theta2,
                            jump_gamma = jump_gamma2,
                            jump_z = jump_z2,
                            jump_w = jump_w2,            
                            
                            pr_mean_beta = pr_mean_beta2,
                            pr_sd_beta = pr_sd_beta2,
                            pr_a_th_sigma = pr_a_th_sigma2,
                            pr_b_th_sigma = pr_b_th_sigma2,
                            pr_mean_theta = pr_mean_theta2,
                            pr_a_sigma = pr_a_sigma2,
                            pr_b_sigma = pr_b_sigma2,
                            pr_mean_gamma = pr_mean_gamma2,
                            pr_sd_gamma = pr_sd_gamma2,
                            
                            missing = missing2)        
        
        
        temp_proc2_zs = self._proc2(niter = niter2, 
                                    nburn = nburn2, 
                                    nthin = nthin2, 
                                    ndim = ndim2, 
                                    outputs = lsirm)
        
        oblimin_proc2_zs = self._oblimin(proc2s = temp_proc2_zs["proc2_zs"])
        
        self.iamax = temp_proc2_zs["iamax"]
        self.amax = temp_proc2_zs["amax_data"]["z_estimate"]
        self.amax_data = temp_proc2_zs["amax_data"]
        self.oblimin_proc2_zs = oblimin_proc2_zs
        #self.data_topics = self.most_words_per_topic(temp_proc2_zs["amax_data"])[:,0]
        self.percentile_range = percentage_range
        
        
        print("elapsed time: " + str(time.time() - start))
        
        return self



