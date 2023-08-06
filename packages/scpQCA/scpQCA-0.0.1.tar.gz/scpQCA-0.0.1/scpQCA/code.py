import pandas as pd
import numpy as np
import itertools
import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
from sklearn import tree
from sklearn import linear_model


class scpQCA:
    def __init__(self,data,feature_list,decision_name, caseid):
        self.data=data
        self.feature_list=feature_list
        self.necessity=[]
        self.decision_name=decision_name
        self.decision_label=-1
        self.caseid=caseid
        self.formal_feature=[]
        self.omit=[]
        
    def direct_calibration(self, full_membership, cross_over, full_nonmembership):
        def Ragin_direct(data, full_membership, cross_over, full_nonmembership):
            deviation=[i-cross_over for i in data]
            log_odds=[i*(3/(full_membership-cross_over)) if i>0 else i*(-3/(full_nonmembership-cross_over)) for i in deviation]
            return [round(np.exp(i)/(1+np.exp(i)),3) for i in log_odds]
        self.raw_data=copy.deepcopy(self.data)
        for factor in self.feature_list:
            self.data[factor]=np.array(Ragin_direct(list(self.data[factor]), full_membership, cross_over, full_nonmembership))

    def indirect_calibration(self, class_num, full_membership=None, full_nonmembership=None):
        def Ragin_indirect(data, class_num, full_membership, full_nonmembership):
            if full_membership!=None and full_nonmembership!=None:
                a,b=full_membership, full_nonmembership
            else:
                a,b=max(data),min(data)
            ruler=np.linspace(b,a,class_num+1)
            cali=[]
            for i in range(len(data)):
                for j in range(len(ruler)):
                    if data[i]<=ruler[j+1]:
                        cali.append(round(j/(class_num-1),3))
                        break
            return cali
        self.raw_data=copy.deepcopy(self.data)
        character_list=copy.deepcopy(self.feature_list)
        if self.caseid !=None and self.caseid in character_list:
            character_list.remove(self.caseid)
        for factor in character_list:
            # print(factor)
            self.data[factor]=np.array(Ragin_indirect(list(self.data[factor]),class_num, full_membership, full_nonmembership))
    
    def raw_truth_table(self,decision_label,cutoff=2,consistency_threshold=0.8,sortedby=True):
        character_list=copy.deepcopy(self.feature_list)
        if self.caseid !=None and self.caseid in character_list:
            character_list.remove(self.caseid)
        if self.decision_name in character_list:
            character_list.remove(self.decision_name)
        issues=len(self.data.loc[(self.data[self.decision_name]==decision_label)])
        Cartesian=[]
        for i in range(len(character_list)):
            Cartesian.append(list(self.data[character_list[i]].unique()))
        values=[d for d in itertools.product(*Cartesian)]
        raw=[]
        print(len(values))
        for v in range(len(values)):
            # print(v)
            Q=''
            for i in range(len(character_list)):
                Q+=str(character_list[i])+'=='+str(values[v][i])+' & '
            Q=Q[:-3]
            result=self.data.query(Q)
            if len(result)!=0:
                number=len(result)
                raw_consistency=len(result.loc[(result[self.decision_name]==decision_label)])/len(result) if number>0 else 0
                raw_coverage=len(result.loc[(result[self.decision_name]==decision_label)])/issues if issues>0 else 0
                case_list=list(result[self.caseid]) if self.caseid!=None else []
                if number>=cutoff and raw_consistency>=consistency_threshold:
                    raw.append((values[v]+(number,case_list,raw_consistency,raw_coverage,)))
        print("raw finished")
        if sortedby:
            # ordered by number (coverage)
            raw=sorted(raw, key=lambda raw: raw[len(character_list)+3],reverse=True)
            raw=sorted(raw, key=lambda raw: raw[len(character_list)],reverse=True)
        else:
            # ordered by consistency
            raw=sorted(raw, key=lambda raw: raw[len(character_list)+3],reverse=True)
            raw=sorted(raw, key=lambda raw: raw[len(character_list)+2],reverse=True)
        character_list.append('number')
        character_list.append('caseid')
        character_list.append('consistency')
        character_list.append('coverage')

        truth_table=pd.DataFrame(raw,columns=character_list)
        print(truth_table)

    def scp_truth_table(self,rules,decision_label):
        self.decision_label=decision_label
        issues=len(self.data.loc[(self.data[self.decision_name]==decision_label)])
        rules=sorted(rules,key=lambda raw:raw[0],reverse=True)
        df=[]
        for i in range(len(rules)):
            row=['-']*(len(self.feature_list)+3)
            Q=rules[i][0].split(' & ')
            for j in Q:
                equation=j.split('==')
                factor=equation[0]
                value=equation[1]
                row[self.feature_list.index(factor)]=value
            result=self.data.query(rules[i][0])
            number=len(result)
            raw_consistency=len(result.loc[(result[self.decision_name]==decision_label)])/len(result) if number>0 else 0
            row[-3]=number
            row[-2]=format(raw_consistency, '.4f') 
            row[-1]=format(len(result.loc[(result[self.decision_name]==decision_label)])/issues, '.4f') 
            df.append(row)
        df=sorted(df, key=lambda raw: raw[-2],reverse=True)
        df=sorted(df, key=lambda raw: raw[-1],reverse=True)
        character_list=copy.deepcopy(self.feature_list)
        character_list.append('number')
        character_list.append('consistency')
        character_list.append('coverage')
        truth_table=pd.DataFrame(df,columns=character_list)
        with pd.option_context('display.max_rows', None):  
            print(truth_table)
        return truth_table

    def search_necessity(self,decision_label,consistency_threshold=0.9):
        self.decision_label=decision_label
        self.necessity=[]
        character_list=copy.deepcopy(self.feature_list)
        if self.caseid !=None and self.caseid in character_list:
            character_list.remove(self.caseid)
        if self.decision_name in character_list:
            character_list.remove(self.decision_name)
        issue=len(self.data.loc[(self.data[self.decision_name]==self.decision_label)])
        if issue==0:
            return []
        necessity=dict()
        for character in character_list:
            for value in self.data[character].unique():
                if len(self.data.loc[(self.data[self.decision_name]==self.decision_label) & (self.data[character]==float(value))])/issue>=consistency_threshold:
                    print("{}=={} is a necessity condition".format(character,value))
                    necessity[character]=value
                    self.necessity.append(str(character)+'=='+str(value))
        self.formal_feature=self.feature_list
        self.feature_list=character_list
        return necessity

    def __search_combination(self, items):
        if len(items) == 0:
            return [[]]
        subsets = []
        first_elt = items[0] 
        rest_list = items[1:]
        for partial_sebset in self.__search_combination(rest_list):
            subsets.append(partial_sebset)
            next_subset = partial_sebset[:] +[first_elt]
            subsets.append(next_subset)
        return subsets

    def filter(self):
        self.omit=[]
        print("Please input the filter items, separated with Space and end with Enter.")
        for factor in self.feature_list:
            print("The omitted value of factor \"{}\" is:".format(factor))
            temp=input()
            values=[]
            while values==[]:
                try:
                    values=temp.split(" ")
                except:
                    print("wrong format, please split the multi-value with space")
                    temp=input()
            for value in values:
                if value==''or value=='\n':
                    continue
                else:
                    self.omit.append(str(factor)+'=='+str(value))
        print(self.omit)

    def candidate_rules(self,decision_label,consistency,cutoff,rule_length=5):
        if self.caseid !=None and self.caseid in self.feature_list:
            self.feature_list.remove(self.caseid)
        if self.decision_name in self.feature_list:
            self.feature_list.remove(self.decision_name)
        self.decision_label=decision_label
        issues=len(self.data.loc[(self.data[self.decision_name]==decision_label)])
        candidate=[]
        for i in self.__search_combination(self.feature_list):
            if 1<len(i)<rule_length:
                candidate.append(i)  
        print("Running...please wait. There are {} candidate combinations.".format(len(candidate)))
        rules=[]
        for i in range(len(candidate)):  
            length=len(candidate[i])
            Cartesian=[]                  
            for j in range(length):
                Cartesian.append(list(self.data[candidate[i][j]].unique()))
            values=[d for d in itertools.product(*Cartesian)]   
            for r in range(len(values)):
                Q=''
                for j in range(length):
                    Q+=str(candidate[i][j])+'=='+str(values[r][j])+' & '
                Q=Q[:-3]
                flag=False
                for n in self.necessity+self.omit:
                    if n in Q:
                        flag=True
                result=self.data.query(Q)
                p=result[self.decision_name].value_counts(normalize = True, dropna = False)
                if len(p)==0 or flag:
                    pass
                elif p.idxmax()==self.decision_label and p[p.idxmax()]>=consistency and p[p.idxmax()]*len(result)>=cutoff: 
                    row=[Q,p[p.idxmax()]*len(result)/issues,p[p.idxmax()]] # coverage, consistency
                    rules.append(row)
        print("There are {} candidate rules in total.".format(len(rules)))
        return rules

    def __check_subset(self, new_rule, rules, unique_cover=2):
        final_rules=copy.deepcopy(rules)
        final_rules.append(new_rule)
        rules=[]
        set_A=set()
        for i in range(len(final_rules)):
            set_B=set()
            for j in range(i+1,len(final_rules)):
                temp=self.data.query(final_rules[j])
                index=set(temp[temp[self.decision_name] == self.decision_label].index.tolist())
                set_B=set_B.union(index)
                temp[self.decision_name].value_counts(normalize = False, dropna = True)
            temp=self.data.query(final_rules[i])
            index=set(temp[temp[self.decision_name] == self.decision_label].index.tolist())
            if len(index.difference(set_B.union(set_A)))<unique_cover:
                pass
            else:
                rules.append(final_rules[i])
                set_A=set_A.union(index)      
        return rules, set_A

    def greedy(self,rules,decision_label,rule_length=5,consistency=0.8,cutoff=2,unique_cover=2):
        if rules==[]:
            _=self.search_necessity(decision_label=decision_label)
            rules=self.candidate_rules(decision_label,consistency,cutoff,rule_length)
        rules=sorted(rules, key=lambda raw: raw[2],reverse=True)
        rules=sorted(rules, key=lambda raw: raw[1],reverse=True)
        event_set=set()
        final_rule=[]
        for i in range(len(rules)):
            temp_final_rule, temp_set=self.__check_subset(rules[i][0], final_rule, unique_cover)
            if len(temp_set)>len(event_set):
                final_rule, event_set=temp_final_rule, temp_set
        if len(final_rule)==0:
            return [],set()
        for i in range(len(final_rule)):
            for j in range(len(self.necessity)):
                final_rule[i]=final_rule[i]+' & '+self.necessity[j]
        final_set=set()
        for rule in final_rule:
            cases=self.data.query(rule)
            final_set=final_set.union(set(list(cases[cases[self.decision_name] == self.decision_label][self.caseid])))
        return final_rule, final_set

    def MFMC(self,rules,decision_label,rule_length=5,consistency=0.8,cutoff=2,unique_cover=2):
        G=nx.DiGraph()
        G.add_node('start')
        G.add_node('end')
        cases=set(self.data[self.data[self.decision_name] == decision_label].index.tolist())
        for case in cases:
            G.add_node(case)
            G.add_edge(case,'end',weight=1)
        if rules==[]:
            _=self.search_necessity(decision_label=decision_label)
            rules=self.candidate_rules(decision_label,consistency,cutoff,rule_length)
        rules=sorted(rules, key=lambda raw: raw[2],reverse=True)
        rules=sorted(rules, key=lambda raw: raw[1],reverse=True)
        for i in range(len(rules)):
            result=self.data.query(rules[i][0])
            cases=set(result[result[self.decision_name]==self.decision_label].index.tolist())
            G.add_node(rules[i][0])
            G.add_edge('start',rules[i][0],weight=1)# start-rule
            for j in cases:
                G.add_edge(rules[i][0],j,weight=1)
        A=nx.adjacency_matrix(G)
        A=A.toarray()
        residual = copy.deepcopy(A)
        flow = [0 for i in range(len(A))]
        level = [float('inf') for i in range(len(A))]
        maxflowgraph = [[0 for i in range(len(A))] for j in range(len(A))]
        def build_level(source,sink):
            level[source] = 0
            level_pre = [float('inf') for i in range(len(A))]
            q = Queue()
            q.put(source)
            while(not q.empty()):
                current = q.get()
                for i in range(len(A)):
                    if( (i==source) | (i==current) ):
                        continue
                    if((residual[current][i]>0)&(level_pre[i]==float('inf'))):
                        level_pre[i] = current
                        level[i] = level[current]+1
                        q.put(i)
            if(level_pre[sink]!=float('inf')):
                return True
            else:
                return False
        def get_augment(source,sink):
            temp_augment = [source]
            count = 1
            def recursion(count):
                for i in range(len(A)):
                    if(level[i]==count):
                        temp_augment.append(i)
                        if(i == sink):
                            send_flow(temp_augment,source,sink)
                        recursion(count+1)
                        temp_augment.remove(i)
            recursion(count)
        def send_flow(augment,source,sink):
            flow[sink] = float('inf')
            for i in range(len(augment)-1):
                flow[augment[i+1]] = min(flow[augment[i]],residual[augment[i]][augment[i+1]])
            if(flow[sink] != 0):
                for i in range(len(augment)-1):
                    residual[augment[i]][augment[i+1]] -= flow[sink]
                    residual[augment[i+1]][augment[i]] += flow[sink]
                    maxflowgraph[augment[i]][augment[i+1]] += flow[sink]  
        def dinic(source,sink):
            flow[source] = float('inf')
            while(True):
                temp = build_level(source,sink)
                if(temp is False):
                    break
                else:
                    get_augment(source,sink)

            flow[source] = float('inf')
            while(True):
                temp = build_level(source,sink)
                if(temp is False):
                    break
                else:
                    get_augment(source,sink)
        dinic(0,1)
        first_rule=[]
        node_list=list(G.nodes())
        for i in range(len(maxflowgraph)):
            if maxflowgraph[0][i]!=0:
                first_rule.append(node_list[i])
        cases_set=set()
        final_rule=[]
        for i in range(len(first_rule)):
            temp_final_rule, temp_set=self.__check_subset(first_rule[i], final_rule, unique_cover)
            if len(temp_set)>len(cases_set):
                final_rule, cases_set=temp_final_rule, temp_set
        if len(final_rule)==0:
            final_rule.append('')
            return [],set()
        for i in range(len(final_rule)):
            for j in range(len(self.necessity)):
                final_rule[i]=final_rule[i]+' & '+self.necessity[j]
        final_set=set()
        for rule in final_rule:
            cases=self.data.query(rule)
            final_set=final_set.union(set(list(cases[cases[self.decision_name] == decision_label][self.caseid])))
        return final_rule, final_set

    def _judge_rules(self,temp_rule,temp_rule_new):
        setA=set()
        setB=set()
        consistency1=set()
        consistency2=set()
        for rule in temp_rule:
            temp=self.data.query(rule)
            setA=setA.union(set(temp[temp[self.decision_name]==self.decision_label].index.tolist()))
            consistency1=consistency1.union(set(temp[temp[self.decision_name]==self.decision_label].index.tolist()))
            consistency2=consistency2.union(set(temp[temp[self.decision_name]!=self.decision_label].index.tolist()))
        consistencyA=len(consistency1)/(len(consistency1)+len(consistency2)) if len(consistency1)+len(consistency2)!=0 else 0
        consistency1=set()
        consistency2=set()
        for rule in temp_rule_new:
            temp=self.data.query(rule)
            setB=setB.union(set(temp[temp[self.decision_name]==self.decision_label].index.tolist()))
            consistency1=consistency1.union(set(temp[temp[self.decision_name]==self.decision_label].index.tolist()))
            consistency2=consistency2.union(set(temp[temp[self.decision_name]!=self.decision_label].index.tolist()))
        consistencyB=len(consistency1)/(len(consistency1)+len(consistency2)) if len(consistency1)+len(consistency2)!=0 else 0
        if len(setB)>len(setA):
            return 1
        elif len(setB)==len(setA):
            if len(temp_rule_new)<len(temp_rule):
                return 1
            elif len(temp_rule_new)==len(temp_rule):
                if consistencyB>consistencyA:
                    return 1
                elif consistencyB==consistencyA:
                    return 0
                else:
                    return consistencyB-consistencyA
            else:
                return len(temp_rule)-len(temp_rule_new)
        else:
            return len(setB)-len(setA)

    def simannealing(self,rules,decision_label,rule_length=5,consistency=0.8,cutoff=2):
        if rules==[]:
            _=self.search_necessity(decision_label)
            rules=self.candidate_rules(decision_label,consistency,cutoff,rule_length)
        new_rules=[i[0] for i in rules]
        final_rule=[]
        if len(new_rules)==0:
            return [],set()
        for length in range(1,min(rule_length,len(rules))):
            temp_rule=random.sample(new_rules,length)
            temp_rule_new=random.sample(new_rules,length)
            delta=0.99
            T=10000
            T_min=1
            while T>T_min:
                dE=self._judge_rules(temp_rule,temp_rule_new)
                if dE==1:
                    temp_rule=temp_rule_new
                elif dE==0:
                    pass
                else:
                    if np.exp(dE/T)>random.random():
                        temp_rule=temp_rule_new
                T*=delta
            if self._judge_rules(final_rule,temp_rule)==1 or final_rule==[]:
                final_rule=temp_rule
        for i in range(len(final_rule)):
            for j in range(len(self.necessity)):
                final_rule[i]=final_rule[i]+' & '+self.necessity[j]
        final_set=set()
        for rule in final_rule:
            cases=self.data.query(rule)
            final_set=final_set.union(set(list(cases[cases[self.decision_name] == self.decision_label][self.caseid])))
        return final_rule, final_set

    def _combine(self,m, n):
        a = len(m)
        c = ''
        count = 0
        for i in range(a): 
            if(m[i] == n[i]):
                c += m[i]
            elif(m[i] != n[i]):
                c += '-'
                count += 1
        if(count > 1): 
            return None
        else:            
            return c

    def _find_prime_implicants(self,data):
        newList = list(data)
        size = len(newList)
        IM = []
        im = []
        im2 = []
        mark = [0]*size
        m = 0
        for i in range(size):
            for j in range(i+1, size):
                c = self._combine( str(newList[i]), str(newList[j]) )
                if c != None:
                    im.append(str(c))
                    mark[i] = 1
                    mark[j] = 1
                else:
                    continue
        mark2 = [0]*len(im)
        for p in range(len(im)):
            for n in range(p+1, len(im)):
                if( p != n and mark2[n] == 0):
                    if( im[p] == im[n]):
                        mark2[n] = 1
        for r in range(len(im)):
            if(mark2[r] == 0):
                im2.append(im[r])
        for q in range(size):
            if( mark[q] == 0 ):
                IM.append( str(newList[q]) )
                m = m+1
        if(m == size or size == 1):
            return IM
        else:
            return IM + self._find_prime_implicants(im2)
    
    def QuineMccluskey(self,decision_label,consistency=0.8,cutoff=2):
        self.decision_label=decision_label
        if self.caseid !=None and self.caseid in self.feature_list:
            self.feature_list.remove(self.caseid)
        if self.decision_name in self.feature_list:
            self.feature_list.remove(self.decision_name)  
        features=[]
        mv_features=dict()
        temp_data=copy.deepcopy(self.data[[self.caseid,self.decision_name]])
        for character in self.feature_list:
            if len(self.data[character].unique())>2:
                value=list(self.data[character].unique())
                for v in range(len(value)):
                    name=character+'{}'.format(v)
                    temp_data[name]=[1 if self.data.loc[i,character]==value[v] else 0 for i in range(len(self.data))]
                    features.append(name)
                mv_features[character]=value
            else:
                temp_data[character]=self.data[character]
                features.append(character)
        Cartesian=[]
        # print(temp_data)
        for i in range(len(features)):
            # print(temp_data[features[i]].unique())
            Cartesian.append(list(temp_data[features[i]].unique()))
        values=[d for d in itertools.product(*Cartesian)]
        raw=[]
        for v in range(len(values)):
            Q=''
            for i in range(len(features)):
                Q+=str(features[i])+'=='+str(values[v][i])+' & '
            Q=Q[:-3]
            flag=False
            for n in self.necessity+self.omit:
                if n in Q:
                    flag=True
            result=temp_data.query(Q)
            if len(result)==0 or flag:
                    pass
            else:
                number=len(result)
                raw_consistency=len(result.loc[(result[self.decision_name]==decision_label)])/len(result) if number>0 else 0
                if number>=cutoff and raw_consistency>=consistency:
                    raw.append(list(values[v]))
        data_binary=[]
        for i in range(len(raw)):
            temp=''
            for j in range(len(features)):
                temp+=str(int(raw[i][j]))
            data_binary.append(temp)
        result=self._find_prime_implicants(set(data_binary))
        final_rules=[]
        new_raw=[['-',]*len(self.feature_list) for _ in range(len(result))]
        for i in range(len(new_raw)):
            count=0
            for j in range(len(self.feature_list)):
                if self.feature_list[j] not in mv_features.keys():
                    new_raw[i][j]=result[i][j+count]
                else:
                    start_index=features.index(self.feature_list[j]+str(0))
                    end_index=features.index(self.feature_list[j]+str(len(mv_features[self.feature_list[j]])-1))
                    count+=len(mv_features[self.feature_list[j]])
                    v=mv_features[self.feature_list[j]][result[i].index('1',start_index,end_index+1)-start_index]
                    new_raw[i][j]=str(v)
        for value in new_raw:
            Q=''
            for i in range(len(self.feature_list)):
                Q+=str(self.feature_list[i])+'=='+value[i]+' & ' if value[i]!='-' else ''
            Q=Q[:-3]
            final_rules.append(Q)
        final_set=set()
        for rule in final_rules:
            cases=self.data.query(rule)
            final_set=final_set.union(set(list(cases[cases[self.decision_name] == decision_label][self.caseid])))
        return final_rules, final_set

    def cov_n_con(self,configuration,issue_sets):
        if issue_sets==set():
            print("consistency = {} and coverage = {}".format(0.0,0.0))
        coverage=len(issue_sets)/len(self.data[self.data[self.decision_name] == self.decision_label]) if len(self.data[self.data[self.decision_name] == self.decision_label])!=0 else 0
        consistency1=set()
        consistency2=set()
        for rule in configuration:
            temp=self.data.query(rule)
            consistency1=consistency1.union(set(temp[temp[self.decision_name]==self.decision_label].index.tolist()))
            consistency2=consistency2.union(set(temp[temp[self.decision_name]!=self.decision_label].index.tolist()))
        consistency=len(consistency1)/(len(consistency1)+len(consistency2)) if len(consistency1)+len(consistency2)!=0 else 0
        print("consistency = {} and coverage = {}".format(consistency,coverage))

    def runQCA(self, optimization, decision_label, rule_length=5, consistency=0.8,cutoff=2,unique_cover=2):
        self.decision_label=decision_label
        if self.caseid !=None and self.caseid in self.feature_list:
            self.feature_list.remove(self.caseid)
        if self.decision_name in self.feature_list:
            self.feature_list.remove(self.decision_name)  
        if optimization=="greedy":
            return self.greedy([],decision_label,rule_length=rule_length,consistency=consistency,cutoff=cutoff,unique_cover=unique_cover)
        elif optimization=="MFMC":
            return  self.MFMC([],decision_label,rule_length=rule_length,consistency=consistency,cutoff=cutoff,unique_cover=unique_cover)
        elif optimization=="SimAnnealing":
            return self.simannealing([],decision_label,rule_length=rule_length,consistency=consistency,cutoff=cutoff)
        elif optimization=="qma":
            return self.QuineMccluskey(decision_label,consistency=consistency,cutoff=cutoff)
        else:
            print("Wrong optimization key!")

    def comparison(self, data, feature_list, round, random_num, optimization, caseid, decision_name, rule_length, consistency=0.8,cutoff=2,unique_cover=2, index_list=[]):
        code1,code2,code3,code4=0,0,0,0
        dtr_score=[]
        lr_score=[]
        samply_index=[]
        code_result=[]
        for i in range(round):
            random_index=set()
            if index_list!=[]:
                random_index=set(index_list[i])
            else:
                for _ in range(int(random_num)):
                    random_index.add(random.randint(0,len(data)-1))
            print("The sample cases are:", random_index)
            samply_index.append(len(random_index))
            data_test=data.drop(list(random_index))
            if self.caseid !=None and self.caseid in feature_list:
                feature_list.remove(self.caseid)
            if self.decision_name in feature_list:
                feature_list.remove(self.decision_name)
            model = tree.DecisionTreeClassifier(max_depth=rule_length, min_samples_split=int(1/(1-consistency)), min_samples_leaf=cutoff)#Decision Tree Regression
            model.fit(data_test[feature_list],data_test[decision_name])
            score=model.score(data.loc[random_index,feature_list],data.loc[random_index,decision_name])
            dtr_score.append(score)
            print(model.predict(data.loc[random_index,feature_list]))
            print("Decision Tree's prediction precision is:",score)
            model = linear_model.LogisticRegression()# Linear Regression
            model.fit(data_test[feature_list],data_test[decision_name])
            score=model.score(data.loc[random_index,feature_list],data.loc[random_index,decision_name])
            lr_score.append(score)
            print(model.predict(data.loc[random_index,feature_list]))
            print("Linear Regression's prediction precision is:",score)
            result=list(data[decision_name].unique())
            rules,sets=[],[]
            for i in range(len(result)):
                obj=scpQCA(data_test,feature_list,decision_name,caseid)
                # obj.search_necessity(result[i])
                temp_rules,_=obj.runQCA(optimization,result[i], rule_length, consistency, cutoff, unique_cover)
                rules.append(temp_rules)
                sets.append(set())
                for rule in temp_rules:
                    sets[i]=sets[i].union(set(list(data.query(rule).index)))
            print(rules,sets)
            print("scpQCA's prediction solutions are:")
            for random_i in random_index:
                i=result.index(data.iloc[random_i][decision_name])
                right_set=sets[i]
                wrong_set=set()
                for j in range(len(result)):
                    if j!=i:
                        wrong_set=wrong_set.union(sets[j])
                if random_i in right_set and random_i not in wrong_set:
                    print("perfectly correct!")
                    code1+=1
                elif random_i in right_set and random_i in wrong_set:
                    print("confusion mistake!")
                    code2+=1
                elif random_i not in right_set and random_i in wrong_set:
                    print("totally mistake!")
                    code3+=1
                else:
                    print("not found")
                    code4+=1
            code_result.append([code1,code2,code3,code4])
            print()
        print("Decision Tree's results are:","model score=",dtr_score)
        print("Linear Regression's results are:","model score=",lr_score)
        print("The 4 solution codes are: perfectly correct!, confusion mistake!, totally mistake!, not found")
        print("scpQCA's solution codes are:",code_result)
        return samply_index,dtr_score,lr_score,code_result

    def draw_plt(self, dtr_score, lr_score, code_result, round):
        dtr=dtr_score
        lr=lr_score
        code=code_result
        code1,code2,code3,code4=[code[0][0],],[code[0][1],],[code[0][2],],[code[0][3],]
        for i in range(1,len(code)):
            code1.append(code[i][0]-code[i-1][0])
            code2.append(code[i][1]-code[i-1][1])
            code3.append(code[i][2]-code[i-1][2])
            code4.append(code[i][3]-code[i-1][3])
        print(code1,code2,code3,code4)
        ratio1,ratio2,ratio3,ratio4,ratio5=[],[],[],[],[]
        for i in range(round):
            ratio1.append(code1[i]/(code1[i]+code2[i]+code3[i]+code4[i]))
            ratio2.append(code2[i]/(code1[i]+code2[i]+code3[i]+code4[i]))
            ratio3.append(code3[i]/(code1[i]+code2[i]+code3[i]+code4[i]))
            ratio4.append(code4[i]/(code1[i]+code2[i]+code3[i]+code4[i]))
            ratio5.append(code1[i]/(code1[i]+code2[i]+code3[i]))
        x=range(len(lr))
        plt.figure(figsize=(12,8))
        plt.gcf().set_facecolor(np.ones(3)* 240 / 255)
        plt.grid()
        plt.plot(x, dtr, marker='.', ms=10, label="decision tree regression")
        plt.plot(x, lr, marker='.', ms=10, label="linear regression")
        plt.plot(x, ratio1, marker='.', ms=10, label="perfectly correct")
        plt.plot(x, ratio5, marker='.', ms=10, label="perfectly correct(except not found)")
        plt.xticks(rotation=45)
        plt.ylim(0,1)
        plt.xlabel("case number")
        plt.ylabel("ratio")
        plt.legend(loc="upper left")
        plt.show()
        print("The mean of Linear Regression, Decision Tree, perfect correct and perfectly correct(except not found) are:")
        print(np.mean(lr),np.mean(dtr),np.mean(ratio1),np.mean(ratio5))
        print("The variance of Linear Regression, Decision Tree, perfect correct and perfectly correct(except not found) are:")
        print(np.var(lr),np.var(dtr),np.var(ratio1),np.var(ratio5))
        return

# if __name__=="__main__":
#     data=[[random.randint(0,100) for _ in range(6)] for _ in range(30)]
#     data=pd.DataFrame(data)
#     data.columns=['A','B','C','D','F','cases']
#     obj=scpQCA(data,['A','B','C','D','F'],decision_name='F',caseid='cases')
#     # obj=scpQCA.scpQCA(data,['A','B','C','D','E','F','G','H','I'],decision_name='F',caseid='cases')
#     # obj.direct_calibration(90,50,10)
#     obj.indirect_calibration(2,100,0)
#     print(obj.data)
#     obj.raw_truth_table(1,cutoff=1,sortedby=True)

#     obj.search_necessity(decision_label=1,consistency_threshold=0.9)

#     rules=obj.candidate_rules(1,0.8,1)

#     obj.scp_truth_table(rules,1)

#     configuration,issue_set=obj.QuineMccluskey(decision_label=1,consistency=0.8,cutoff=1)
#     print(configuration)
#     print(issue_set)

#     obj.cov_n_con(configuration,issue_set)
#     sample_index, dtr, lr, code=obj.comparison(data,10,3,"greedy",'cases','F',5,0.8,1,1)
#     obj.draw_plt(dtr, lr, code,10)