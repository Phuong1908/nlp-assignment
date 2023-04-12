from enum import Enum
import pdb
import re

class Category(Enum):
    ROOT = 0
    NOUN = 1
    VERB = 2
    PRO_LOC = 3
    QDET = 4
    PREP_TIME = 5
    PRO_TIME = 6
    DET = 7
    PREP_LOC = 8
    PRO_BUS = 9

    def __str__(self):
        return self.name

class RelationName(Enum):

    ROOT = 0
    SUBJ = 1
    NOBJ = 2
    POBJ = 3
    DET_WH = 4
    NMOD = 5
    DET = 6
    PMOD_TIME = 7
    PMOD_LOC = 8

    def __str__(self):
        return self.name

class Tense(Enum):
    PAST  = 0
    PRES = 1
    FUT = 2


class Prep_SEM(Enum):

    FROM = 0
    TO = 1

    def __str__(self):
        return self.name

class Verb_SEM(Enum):

    DEPART = 0
    ARRIVE = 1

    def __str__(self):
        return self.name

class Token(object):

    def __init__(self, word, cat, sem,index):
        self.word = word
        self.category = cat
        self.sem = sem
        self.index = index
        self.head_index = None

    def __str__(self):
        return f"{self.word}"

    def is_head_of_relation(self, relation_set, relation_name):
        relation_set_with_name = Relation.retrieve_relation(relation_set=relation_set, name=relation_name)
        for rel in relation_set_with_name:
            if rel.head == self:
                return True 
        return False
    
    def is_dept_of_relation(self, relation_set, relation_name):
        relation_set_with_name = Relation.retrieve_relation(relation_set=relation_set, name=relation_name)
        for rel in relation_set_with_name:
            if rel.dept == self:
                return True 
        return False

    def is_main(self, token_set ,relation_set):
        index = token_set.index(self)
        window = token_set[index:index+WINDOW_SIZE]
        for token in window:
            rel = Relation.get_relation(head=token, dept=self,relation_set=relation_set )
            if rel and rel.name != RelationName.SUBJ and rel.name != RelationName.NOBJ: 
                return False
        return True

ROOT = Token('s', Category.ROOT ,None, 0)
WINDOW_SIZE = 1

class Relation(object):
    #return relation object
    # Attribute: _name, _head, _dependent 
    def __init__(self, name, head, dependent):
        self.name = name
        self.head = head
        self.dependent = dependent

    def __str__(self):
        return f"({self.name},{self.head},{self.dependent})"

    @staticmethod
    def has_relation(relation_set, name):
        if len(Relation.retrieve_relation(relation_set=relation_set, name=name)) == 0:
            return False
        return True
    
    @staticmethod
    def retrieve_relation(relation_set, name):
        if len(relation_set) == 0:
            return []
        res = []
        for rel in relation_set:
            if rel.name == name:
                res.append(rel) 
        return res

    @staticmethod
    def is_nmod(head, dept):
        if dept.category == Category.NOUN:
            if head.category == Category.PRO_LOC or head.category == Category.NOUN or head.category == Category.PRO_BUS:
                return True
        return False

    @staticmethod
    def is_det_wh(head, dept, relation_set):
        if dept.category == Category.QDET:
            if head.category == Category.NOUN or head.category == Category.PRO_LOC or head.category == Category.PRO_BUS  or head.category == Category.PRO_TIME:
                if not Relation.has_relation(relation_set=relation_set, name=RelationName.DET_WH):
                    return True
        return False

    @staticmethod
    def is_root(head, dept):
        if head is ROOT and dept.category == Category.VERB:  #chống chỉ định nếu khuyết động từ  :)))
            return True
        return False

    @staticmethod
    def is_pmod_time(head, dept, relation_set):
        if dept.category == Category.PREP_TIME:
            if head.category == Category.PRO_TIME:
                if not head.is_head_of_relation(relation_set=relation_set, relation_name=RelationName.PMOD_TIME):
                    return True
        return False
    
    @staticmethod
    def is_pmod_loc(head, dept, relation_set):
        if dept.category == Category.PREP_LOC:
            if head.category == Category.PRO_LOC:
                if not head.is_head_of_relation(relation_set=relation_set, relation_name=RelationName.PMOD_LOC):
                    return True
        return False

    @staticmethod 
    def is_det(head, dept):
        if dept.category == Category.DET and head.category == Category.NOUN:
            return True
        return False

    @staticmethod 
    def is_subj(head, dept, relation_set): 
        if head.category == Category.VERB:
            if dept.category == Category.NOUN or dept.category == Category.PRO_LOC or dept.category == Category.PRO_BUS or dept.category == Category.PRO_TIME:
                if not Relation.has_relation(relation_set=relation_set, name=RelationName.SUBJ):
                    return True
        return False
    
    @staticmethod
    def is_nobj(head, dept):
        if head.category == Category.VERB:
            if dept.category == Category.NOUN or dept.category == Category.PRO_TIME or dept.category == Category.PRO_LOC or dept.category == Category.PRO_BUS:
                return True
        return False
    
    @staticmethod
    def is_pobj(head, dept):
        if head.category == Category.VERB and dept.category == Category.PRO_TIME :
            return True
        return False 

    @staticmethod
    def get_relation(head, dept, relation_set):
        if Relation.is_root(head, dept):
            return Relation(name=RelationName.ROOT,head=head,dependent=dept)
        elif Relation.is_subj(head, dept, relation_set):
            return Relation(name=RelationName.SUBJ,head=head,dependent=dept)
        elif Relation.is_det(head, dept):
            return Relation(name=RelationName.DET,head=head,dependent=dept)
        elif Relation.is_det_wh(head,dept,relation_set):
            return Relation(name=RelationName.DET_WH,head=head,dependent=dept)
        elif Relation.is_nmod(head, dept):
            return Relation(name=RelationName.NMOD,head=head,dependent=dept)
        elif Relation.is_nobj(head,dept):
            return Relation(name=RelationName.NOBJ,head=head,dependent=dept)
        elif Relation.is_pmod_time(head, dept,relation_set):
            return Relation(name=RelationName.PMOD_TIME,head=head,dependent=dept)
        elif Relation.is_pmod_loc(head, dept, relation_set):
            return Relation(name=RelationName.PMOD_LOC,head=head,dependent=dept)
        elif Relation.is_pobj(head,dept):
            return Relation(name=RelationName.POBJ,head=head,dependent=dept)
        return None
        

    #return Relation object

class GrammarRelation(object):

    def __init__(self, name, relation,left, right):
        self.name = name
        self.relation = relation
        self.left = left #s word
        self.right = right # 

    def __str__(self):
        return f'({self.left} {self.name} {self.right})'

    @staticmethod
    def to_WH(relation):
        #return GrammarRelation obj
        return GrammarRelation(name="WH-Q", relation=relation ,left=ROOT.word,right="")

    @staticmethod
    def to_PRED(relation):
        return GrammarRelation(name="PRED", left=ROOT.word, relation=relation,right=relation.dependent.word)
    
    @staticmethod
    def to_LSUBJ(relation):
        return GrammarRelation(name="LSUBJ", left=ROOT.word, relation=relation ,right= f"<{relation.dependent.word}>")
    
    @staticmethod
    def to_OBJ(relation,right):
        return GrammarRelation(name=relation.head.word, left=ROOT.word, relation=relation ,right=right )

    @staticmethod
    def to_NAME(token):
        right = "d1"
        if (token.category == Category.PRO_TIME):
            right = "t1" 
        elif (token.category == Category.PRO_LOC):
            if token.word == "Huế":
                right = "h1"
            elif token.word == "Hồ Chí Minh":
                right = "hc1"
        elif (token.category == Category.PRO_BUS):
            right = token.word.lower()
        return  GrammarRelation(name="NAME", left="" , relation=None ,right= f"{right} <{token.word}>")

class LogicalForm(object):

    def __init__(self, name, relation,left, right):
        self.name = name
        self.relation = relation
        self.left = left #s word
        self.right = right # 

    def __str__(self):
        return f'({self.left} {self.name} {self.right})'

    @staticmethod
    def handle_position(token):
        if token.category == Category.PREP_TIME:
            return "AT-TIME"
        else:
            if token.sem == Prep_SEM.TO:
                return "TO-LOC"
            elif token.sem == Prep_SEM.FROM:
                return "FROM-LOC"
        return "TO-LOC"

class Bus(object):
    def __init__(self):
        self.name = "BUS"
        self.var = "?b"

    def __str__(self):
        return f"({self.name} {self.var})"

class ADtime(object):
    def __init__(self,name="ATIME"):
        self.name = name
        self.b_var = "?b"
        self.s_var = "?s"
        self.t_var = "?t"

    def __str__(self):
        return f"({self.name} {self.b_var} {self.s_var} {self.t_var})"

    def get_loc(self,string):
        if re.search(".*h1.*", string):
            self.s_var = "HUE"
        elif re.search(".*d1.*", string):
            self.s_var = "DANANG"
        elif re.search(".*hc1.*", string):
            self.s_var = "HCMC"

class SematicProcedure(object):

    def __init__(self):
        self.procedure = "PRINT-ALL"
        self.var = "?b"
        self.query_list = [Bus()]

    

    def __str__(self):
        queries =f"{self.procedure} {self.var} " 
        for query in self.query_list:
            queries = queries + str(query)
        return queries

#########################################################################################
##### PARSER ############################################################################
#########################################################################################


class Parser(object):
    # return List of relation 
    #alpha: List: init with ROOT element
    #beta: List: init with tokenized input sentence
    #Relation: List: list of Relation object
    def __init__(self, input):
        self.alpha = [ROOT]
        self.beta = input
        self.relation = []
        self.cache = []

    def check(self, rel): #prun những case sai, vd như { r(a,b) r'(c,b) r"(a,c) } xảy ra vì if-else ko handle hết được :))))))
        same = Relation.retrieve_relation(relation_set=self.relation, name=rel.name)
        if len(same) == 0:
            return
        else:
            for relation in same:
                if relation.head == rel.head:
                    if Relation.get_relation(rel.dependent,relation.dependent,self.relation):
                        self.relation.remove(relation)
        return

    def __str__(self):
        string = ""
        for rel in self.relation:
            string += str(rel)
        return string

    def shift(self):
        #pop beta, insert vào alpha tại index 0
        item = self.beta.pop(0)
        self.cache.append(item)
        self.alpha.insert(0,item)
        print('shift ' + str(item))
        return True

    def left_arc(self):
        #pop alpha, ko đổi beta , chèn quan hệ mới vào 
        dept = self.alpha[0]
        head = self.beta[0]
        rel = Relation.get_relation(head=head,dept=dept,relation_set=self.relation)
        if rel is not None:
            print('left')
            print(rel)
            self.check(rel)
            self.relation.append(rel)
            dept.head_index = head.index
            self.alpha.pop(0)
            return True
        return False
        

    def right_arc(self):
        #pop beta, chèn vào index 0 cua alpha 
        dept = self.beta[0]
        head = self.alpha[0]
        
        # if not dept.is_main(token_set=self.beta, relation_set=self.relation):
        #     return False
        rel = Relation.get_relation(head=head,dept=dept,relation_set=self.relation)
        if rel is not None:
            print('right')
            print(rel)
            self.check(rel)
            self.relation.append(rel)
            dept.head_index = head.index
            self.beta.pop(0)
            self.cache.append(dept)
            self.alpha.insert(0,dept)
            return True
        return False

    def p_reduce(self): # ko dat ten reduce() duoc :v
        item = self.alpha[0]
        if item.category == Category.VERB or item is ROOT:
            return False 
        for token in self.beta:
            right = Relation.get_relation(item,token,self.relation)
            left = Relation.get_relation(token,item,self.relation)
            if left or right:
                return False
        self.alpha.pop(0)
        print('reduce' + str(item))
        return True 
    
    def produce(self):
        while len(self.beta) != 0:
            if self.left_arc():
                continue
            elif self.right_arc():
                continue
            elif self.p_reduce():
                continue
            else:
                self.shift()
    
    def map_to_GR(self):
        relations = []
        wh_rel = Relation.retrieve_relation(self.relation, RelationName.DET_WH)
        relations.append(GrammarRelation.to_WH(wh_rel[0]))
        root = Relation.retrieve_relation(self.relation, RelationName.ROOT)
        relations.append(GrammarRelation.to_PRED(root[0]))
        lsubj = Relation.retrieve_relation(self.relation, RelationName.SUBJ)
        relations.append(GrammarRelation.to_LSUBJ(lsubj[0]))
        nobjs = Relation.retrieve_relation(self.relation, RelationName.NOBJ)
        for obj in nobjs:
            token = obj.dependent
            name = GrammarRelation.to_NAME(token)
            relations.append(GrammarRelation.to_OBJ(obj,str(name)))
        self.g_relation = relations
        result = ''.join(map(str, self.g_relation)) 
        return result

    def map_to_LF(self):
        g_relations = self.g_relation.copy()
        f_form = []
        for g_relation in g_relations:
            if g_relation.name == "WH-Q":
                f_form.append(LogicalForm(name="WH-QUERY",relation=g_relation.relation,left=g_relation.left,right=g_relation.right))
            elif g_relation.name == "LSUBJ":
                f_form.append(LogicalForm(name="AGENT",relation=g_relation.relation,left=g_relation.left,right=g_relation.right))
            elif g_relation.name == "PRED":
                f_form.append(LogicalForm(name="PRED",relation=g_relation.relation,left= g_relation.left ,right=g_relation.right)) 
            elif g_relation.name == g_relation.relation.head.word:
                token = g_relation.relation.dependent
                if token.is_head_of_relation(self.relation, RelationName.PMOD_TIME):
                    prep = Relation.retrieve_relation(self.relation,RelationName.PMOD_TIME)[0].dependent #hard code
                    f_form.append(LogicalForm(name=LogicalForm.handle_position(prep),relation=g_relation.relation,left= g_relation.left ,right=g_relation.right)) 
                elif token.is_head_of_relation(self.relation, RelationName.PMOD_LOC):
                    rels = Relation.retrieve_relation(self.relation,RelationName.PMOD_LOC)
                    for rel in rels:
                        if rel.head == token:
                            f_form.append(LogicalForm(name=LogicalForm.handle_position(rel.dependent),relation=g_relation.relation,left= g_relation.left ,right=g_relation.right)) 
                else:
                    f_form.append(LogicalForm(name="TO-LOC",relation=g_relation.relation,left= g_relation.left ,right=g_relation.right)) 
        self.l_form = f_form
        result = ''.join(map(str, self.l_form)) 
        return result

    def map_to_SP(self):
        sem_procedure = SematicProcedure()

        isDepart = True
        for sem in self.l_form:
            if sem.name == "WH-QUERY":
                continue #still hard-code. 
            elif sem.name == "AGENT":
                continue #still hard-code. 
            elif sem.name == "PRED":
                verb = Relation.retrieve_relation(self.relation,RelationName.ROOT)[0].dependent
                if verb.sem == Verb_SEM.ARRIVE:
                    isDepart = False
            elif sem.name == "TO-LOC":
                atime = ADtime("ATIME")
                atime.get_loc (string=sem.right)
                sem_procedure.query_list.append(atime)
            elif sem.name == "FROM-LOC":
                dtime = ADtime("DTIME")
                dtime.get_loc (string=sem.right)
                sem_procedure.query_list.append(dtime)
            elif sem.name == "AT-TIME":
                time = ADtime()
                if isDepart:
                    time.name = "DTIME"
                t_var = Relation.retrieve_relation(self.relation,RelationName.PMOD_TIME)[0].head.word
                time.t_var = t_var
                sem_procedure.query_list.append(time)
        self.sem_procedure = sem_procedure
        return str(self.sem_procedure)