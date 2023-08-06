#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Labeled Latent Dirichlet Allocation
# This code is available under the MIT License.
# (c)2010 Nakatani Shuyo / Cybozu Labs Inc.
# refer to Ramage+, Labeled LDA: A supervised topic model for credit attribution in multi-labeled corpora(EMNLP2009)

from optparse import OptionParser
import sys, re, numpy
import nltk

from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()

def load_corpus(filename):
    corpus = []
    labels = []
    labelmap = dict()
    f = open(filename, 'r')
    for line in f:
        mt = re.match(r'\[(.+?)\](.+)', line)
        if mt:
            label = mt.group(1).split(',')
            for x in label: labelmap[x] = 1
            line = mt.group(2)
        else:
            label = None
        doc = re.findall(r'\w+(?:\'\w+)?',line.lower())
        if len(doc)>0:
            corpus.append(doc)
            labels.append(label)
    f.close()
    return labelmap.keys(), corpus, labels

class LLDA:
    def __init__(self, K, alpha, beta, icd11_terms,icd11_terms_codes):
        #self.K = K
        self.alpha = alpha
        self.beta = beta
        self.icd11_terms=icd11_terms
        self.icd11_terms_codes=icd11_terms_codes

    def term_to_id(self, term):
        if term not in self.vocas_id:
            voca_id = len(self.vocas)
            self.vocas_id[term] = voca_id
            self.vocas.append(term)
        else:
            voca_id = self.vocas_id[term]
        return voca_id

    def complement_label(self, label):
        if not label: return numpy.ones(len(self.labelmap))
        vec = numpy.zeros(len(self.labelmap))
        vec[0] = 1.0
        for x in label:
            '''
            ww=self.obtain_tag_word(x)
            if self.icd11_terms.__contains__(ww.lower()):
                vec[self.labelmap[x]]=self.icd11_terms[ww.lower()]
            else:
                vec[self.labelmap[x]] = 1.0
            '''
            vec[self.labelmap[x]] = 1.0

        return vec

    def set_corpus(self, labelset, corpus, labels):
        labelset.insert(0, "common")
        self.inner_labelset=labelset
        self.labelmap = dict(zip(labelset, range(len(labelset))))
        self.K = len(self.labelmap)

        self.vocas = []
        self.vocas_id = dict()
        self.labels = numpy.array([self.complement_label(label) for label in labels])
        self.docs = [[self.term_to_id(term) for term in doc] for doc in corpus]

        M = len(corpus)
        V = len(self.vocas)

        self.z_m_n = []
        self.n_m_z = numpy.zeros((M, self.K), dtype=int)
        self.n_z_t = numpy.zeros((self.K, V), dtype=int)
        self.n_z = numpy.zeros(self.K, dtype=int)

        for m, doc, label in zip(range(M), self.docs, self.labels):
            N_m = len(doc)
            #z_n = [label[x] for x in numpy.random.randint(len(label), size=N_m)]
            z_n = [numpy.random.multinomial(1, label / label.sum()).argmax() for x in range(N_m)]
            self.z_m_n.append(z_n)
            for t, z in zip(doc, z_n):
                self.n_m_z[m, z] += 1
                self.n_z_t[z, t] += 1
                self.n_z[z] += 1

    def inference(self):
        V = len(self.vocas)
        for m, doc, label in zip(range(len(self.docs)), self.docs, self.labels):
            for n in range(len(doc)):
                t = doc[n]
                z = self.z_m_n[m][n]
                self.n_m_z[m, z] -= 1
                self.n_z_t[z, t] -= 1
                self.n_z[z] -= 1

                denom_a = self.n_m_z[m].sum() + self.K * self.alpha
                denom_b = self.n_z_t.sum(axis=1) + V * self.beta
                p_z = label * (self.n_z_t[:, t] + self.beta) / denom_b * (self.n_m_z[m] + self.alpha) / denom_a
                new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()

                self.z_m_n[m][n] = new_z
                self.n_m_z[m, new_z] += 1
                self.n_z_t[new_z, t] += 1
                self.n_z[new_z] += 1

    def phi(self):
        V = len(self.vocas)
        return (self.n_z_t + self.beta) / (self.n_z[:, numpy.newaxis] + V * self.beta)


    def cosine_similarity(self,v1, v2):
        import math
        "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(v1)):
            x = v1[i]
            y = v2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        return sumxy / math.sqrt(sumxx * sumyy)

    def obtain_weight(self,w):
        if self.icd11_terms.__contains__(w):
            return int(self.icd11_terms[w])
        return 1

    def obtain_tags(self,w):
        tokens = nltk.word_tokenize(w)
        pos_tags = nltk.pos_tag(tokens)
        for word, pos in pos_tags:
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                return True
        return False

    def obtain_tag_word(self,w):
        tokens = nltk.word_tokenize(w)
        pos_tags = nltk.pos_tag(tokens)
        for word, pos in pos_tags:
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                return word
        return w

    def predict(self,text,topK):
        print(text)
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english'))
        if ' ' not in text:
            filtered_sentence=[text]
        else:
            # filtered_sentence = [w.lower() for w in text.split(' ') if not w.lower() in stop_words]
            filtered_sentence=[]
            for w in text.split(' '):
                if w.lower() not in stop_words:
                    pos = self.obtain_tags(w.lower())
                    if pos is None:
                        pos = 'n'

                    pos = 'n'
                    new_w = wnl.lemmatize(w.lower(), pos)
                    if new_w is not None:
                        filtered_sentence.append(new_w)

        w_ids=[self.term_to_id(term) for term in filtered_sentence]
        w_vector=[]
        for i in range(len(self.vocas)):
            if i in w_ids:
                current_word=self.vocas[i]

                is_noun=self.obtain_tags(current_word)
                if is_noun:
                    # ww = self.obtain_weight(current_word)
                    w_vector.append(2)
                else:
                    w_vector.append(1)

                # w_vector.append(1)
            else:
                w_vector.append(0)

        phi_data = self.phi()
        max_k=-1
        max_sim=-1
        max_label=''
        label_term=[]
        label_weight=[]
        label_words=[]
        label_word_weights = []
        for k, label in enumerate(self.inner_labelset):
            print("\n-- label %d : %s" % (k, label))
            weight_list=[0]* len(self.vocas)
            for w,value in enumerate(phi_data[k]):
                # print(w)
                # print(value)
                # print("%s: %.4f" % (self.vocas[w], phi_data[k, w]))
                weight_list[w]=phi_data[k, w]
                # word_list.append(self.vocas[w])
                # weight_list.append(phi_data[k, w])
            #print("my sentence: ", w_vector)
            #print("lda weight: ", weight_list)

            cosine_sim=self.cosine_similarity(w_vector,weight_list)

            print("sim:", cosine_sim)
            if(cosine_sim>max_sim):
                max_sim=cosine_sim
                max_k=k
                max_label=label
            label_term.append(label)
            label_weight.append(cosine_sim)
            for w in numpy.argsort(-phi_data[k])[:topK]:
                print("%s: %.4f" % (self.vocas[w], phi_data[k, w]))
                label_words.append(self.vocas[w])
                label_word_weights.append(phi_data[k, w])
        return max_label,label_term,label_weight,label_words,label_word_weights

    def theta(self):
        """document-topic distribution"""
        n_alpha = self.n_m_z + self.labels * self.alpha
        return n_alpha / n_alpha.sum(axis=1)[:, numpy.newaxis]

    def perplexity(self, docs=None):
        if docs == None: docs = self.docs
        phi = self.phi()
        thetas = self.theta()

        log_per = N = 0
        for doc, theta in zip(docs, thetas):
            for w in doc:
                log_per -= numpy.log(numpy.inner(phi[:,w], theta))
            N += len(doc)
        return numpy.exp(log_per / N)

def main():
    parser = OptionParser()
    parser.add_option("-f", dest="filename", help="corpus filename")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.001)
    parser.add_option("--beta", dest="beta", type="float", help="parameter beta", default=0.001)
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
    (options, args) = parser.parse_args()
    if not options.filename: parser.error("need corpus filename(-f)")

    labelset, corpus, labels = load_corpus(options.filename)

    llda = LLDA(options.K, options.alpha, options.beta)
    llda.set_corpus(labelset, corpus, labels)

    for i in range(options.iteration):
        sys.stderr.write("-- %d " % (i + 1))
        llda.inference()
    #print llda.z_m_n

    phi = llda.phi()
    for v, voca in enumerate(llda.vocas):
        #print ','.join([voca]+[str(x) for x in llda.n_z_t[:,v]])
        print(','.join([voca]+[str(x) for x in phi[:,v]]))

if __name__ == "__main__":
    main()