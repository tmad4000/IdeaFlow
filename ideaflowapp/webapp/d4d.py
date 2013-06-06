# d4d stands for Divisi for Dummies. It is a library of software tools for processing
# natural langauge and common sense reasoning based on ConceptNet4 and the divisi library.
# Installation: Before using this software, install Python2.7, conceptnet4 and divisi as detailed in:
# http://csc.media.mit.edu/docs/install.html and the embedded links to installing conceptnet and divisi
# please send bug reports and suggestions to cfry@media.mit.edu

#d4d Data Structures in 4 sentences: 
#1. Concepts and relations are represented by strings, possibly including more than one word.
#2. Only the pre-defined set of 24 relations are valid relations.
#3. An assertion is a concept, a relation, and another concept.
#4. An instance of d4d is a set of assertions configured to make reasoning easy.

#Tips for getting the most out of this file quickly:
#Scroll down to the calls to en_nl.normalize. These are little utilities that can help with data input.
#Next examine the list of relations. Each assertion must have one of these relations as its relation.
#Skip over most of the utilites, but find 'is_concept" and "is_relation", two utilties that will come in handy.
#From there on down, the methods are relatively high level and interesting. 
#Read their doc and try out the examples in their doc strings.

#if_bad: some methods, esp 'normalize' methods, take an optional argument named 'if_bad'.
#  The default value is 'warn' meaning print out a waring in the python console and return None,
#  which is generally ignored by the callers.
#  To supress the printout, pass in 'ignore'.
#  To error at the first problem encountered, pass in 'error'.
#Additional documentation on Divisi: http://csc.media.mit.edu/docs/divisi2/intro.html
#d4dcc.py has code for turning output from Common Concensus into d4d assertions,
#and d4dcc.write_svdview_files makes files that can be viewed in the "processing" svdview.
#see svd_view.doc.txt for details.


"""
version history
  Freb 19, 2013
            - Minor doc improvement
            - make_assoc now working
            - separated out functionality of assoc_to_spread in its own method
            - make_assoc now "adds in" assertion weights so that 2 assertions that
              have the same 2 concepts will get the weight of the sum of both weights
              from the 2 assertions
  Jan 18, 2013
            - make_assoc method is placeholder for code to create an assoc matrix. 
            - d4dcc.cc_to_assertions_js_obj, Fixed circularity bug by filtering out assertions
               that have concept1 and concept2 equal.
            - d4dcc fixed bug in write_svdview_files that caused it to not use
              the d4d instance passed in to generate the coords and names files.
            - d4dcc massaged example code, improved svd_view_doc.txt
  Jan 2, 2013
            - cut_up_assertions now smarter about separator chars. So now
              normalize_assertions("car isa vehicle. boat isa vehcle.", separator = ".")
              ie separator just a single dot, no space, and this does what you usually want.
            - d4d overview written.
            - removed "is a part of"  and "is a symbol of" from the relations table because "is a" could
              be misinterpreted as "IsA".
            - respelled principle to principal
            - in initing the spread matrix, now use the value of principal_component_count
              rather than a constant of 100 that was way too big for custom data sets.
            - Now principal_component_count defaults to the value of
              self.compute_default_for_principal_component_count()
              which uses number of features and density of input assertions to make
              a reasonable value for principal_component_count.
              You can see the value of principal_component_count used by, for example:
              d4d.c4.principle_component_count
            - Now the examples books.py and dogs.py can be loaded from scatch, they
              will automatically load d4d.
  Dec 18, 2012
            - Now when how_true_is is passed a string as its first argument, the
              string is initially trimmed of whitespace, and if after that it ends in a period,
              the period is removed. 
            - When normalize_assertions is passed a separator of ". ", ie period followed by space,
              and a first argument of "dog isa pet. cat isa pet.", note that the
              last assertion ends with a period, not a space so the last concept was taken as
              "pet." not "pet". But this is probably not what most people want so I've 
              specialized the code to mame that last concept be "pet" in this situation.
            - removed some test cases at the end of the file.
            - how_related_are, concepts_most_related_to, related_concepts_in_category now error
              when called with a subject of other than d4d.c4. They use to just
              use d4d.c4 regardless of the subject you passed.
 Dec 15. 2012
            - d4dcc.py has new method write_svdview_files and
              a new file: svdview_doc.txt to explain how to use it.
 Dec 13.5, 2012
            - New misc_examples folder now contains books and dogs  assertions
 Dec 13, 2012
            - well_formatted_assertions_to_matrix added as an internal method: for modularization only.
            - added method: get_concepts  which returns a list of the concepts in a d4d instance.
            - added method: get_features  which returns a list of the concepts in a d4d instance.
            - added method: get_relations which returns a list of the concepts in a d4d instance.
            - renamed "is_relation" to is_valid_relation to separate out its semantics from is_concept.
            - is_relation now has the semantics of, if the passed in relation is a relation within
              the d4d instance, True is returned.
            - alphabetized the relations list to make finding things in it easier.
            - d4d.relations now returns a pure lists of relations
            - d44.relations_map now holds the map a relation synonyms.
            - added utility print_list to make display of results appear 1 per line.
            - how_true_is now doesn't error when it doesn't know a feature but instead returns 0.0
            - print(d4d_inst) now shows 2D table of the predict matrix
            - d4dcc.py has code for turning common consensus json files into d4d assertions
            - Folder assertion_data  contains 6 files of "home electronics' json assertions from common consensus
            - new file d4dbooks.py contains assertions for the book/magazine/newspaper 
               reasoning by analogy example and an example call showing inference.
Nov 21, 2012
            - fixed bug in normalize_assertions with a file input.
            - extended normalize_relation to work with any case and to strip whitespace from either end of the string
            - new function: normalize_assertions_from_csv
            - normalize_assertions when passed a csv file behaves like normalize_assertions_from_csv
Nov 16, 2012
             - added doc: d4d Data Structures in 4 sentences
             - added doc: Tips for getting the most out of this file quickly 
             - cleaned up doc strings throughout, putting each example on separate line
             - fixed normalize_assertions to work with a file as its first arg.
             - for the Desires relation, added synonyms "like", "love" and made all the
               Desires synonyms have singular and plural forms. 
             - now works for d4d instances a la: print(d4d.c4) 
             
Nov 9, 2012  - Extended error system: see doc on "if_bad" below.
             - Extended how_true_is to be able to take an abnormal assertion as its first arg. 
               See how_true_is extended doc string
             - Fixed normalize_assertions to pass normalize_concept on down, plus removed redundant computation
             - Added relation synonyms for the "plural verbs": 
                   "desire", "cause", "cause desire", "receive action", "inherit from"
             - Added a couple missing commas in the relations table.
             - d4d.normalize now passing all the args it should to d4d._init which fixed a showstopper matrix bug.
             - made arg order of normalize_concepts, separator, if_bad consistent accross functions.
             - Now using Karthik's algorithm to create a sparse matrix: but doesn't appear to have
                any different effect.
             - d4d.relations_map is now what d4d.relations use to be.
             - d4d.relations now returns a simple list of relations.
                   
Nov 6, 2012 - fixed typos in relation synonyms
            - added d4d.normalize that's a synonym for making a d4d instance, but follows the pattern of normalize functions.

Oct 26, 2012: -removed print statements and debugging test call at end.
               -added show_weights param to abnormalize_matrix and d4d instance abnormalize methods
                 to allow the turning off of weights which makes a more "enlgish like" display of assertions.

Oct 25, 2012: -fixed cutting off of last number of concept2 when normalizing a sentence.
               - fixed having weight at end of a sentence string a la: 
                     d4d.normalize_assertion("A Television is created by Acme 0.9") 
               - normalize_assertion now takes if_bad_assertion param.
               - new methods d4d.number_of_assertions_in_matrix(sparse_matrix) and 
                     on d4d instance: d4d.c4.number_of_assertions()
               - new methods: abnormalize_matrix and d4d-instance.abnormalize for getting English-like print outs.
"""
import logging
import inspect # use case to find args: inspect.getargspec(divisi2.blend)
import math
import divisi2
import conceptnet
import networkx as nx

#Low level language tools
from conceptnet.models import Language
en = Language.get('en') #requires django 1.3
en_nl = en.nl
#if the above 2 lines error, try: 
#from simplenlp import get_nl
#en_nl = get_nl('en')

"""
http://csc.media.mit.edu/docs/conceptnet/nl.html
en_nl.is_stopword("the") => True
en_nl.tokenize("Now's the time.") => u"Now 's the time ."
en_nl.normalize("Fishes") => "fish"
en_nl.normalize("Big Cars.") => u'big car '  #note the annoying space on end. Output of normalize needs to be trimmed.
en_nl.normalize("are a") => "be a"
en_nl.normalize("Glimxlings") => "glimxling"  #note word doesn't have to be in conceptnet
en_nl.normalize("Now's the time.") => 'now s time ' # removes "the", replaces ' and . with space
en_nl.normalize("There are movies, etc. and music.") => 'movie  etc  music '

en_nl.lemma_split("Car is a vehicle") => (u'car vehicle', u'1 is a 2')
en_nl.lemma_split("Cars are a vehicle") => (u'car vehicle', u'1s are a 2')

'car vehicle'.split() => ['car', 'vehicle']

en_nl.extract_concepts('People can be eating glimlings.', max_words=1, check_conceptnet=False)
  =>  [u'person', u'eat', u'glimling']
en_nl.extract_concepts('People can be eating glimlings.', max_words=1, check_conceptnet=True)
  => [u'person', u'eat']
en_nl.extract_concepts('People can be eating rice.', max_words=2, check_conceptnet=True)
  => [u'person eat', u'person', u'eat rice', u'eat', u'rice']

"""

"""
The "frequency" of an assertion declares how often it is supposedly true ie
'always'=10, usually=8 unspecified=5 never=-10.
"score" means confidence in the assertion, ie how many users beielve it to be true minus the
number of users that believe its false.
In an analogy space matrix, the "value" ie the cell refered to by a concept and a feature,
is a floating point number than combines the fequencey and score into a number generally
between -1 and 1.
"""

"""examples from: http://csc.media.mit.edu/docs/conceptnet/nl.html?highlight=nltools#simplenlp.NLTools
en_nl.tokenize("dogs are located at houses -2.3").split(" ") # vector of strings.
en_nl.normalize("the Running dogs") => "run dog"  ie remove "the", lowercase and stem "Running", depluralize "dogs"
"""
class d4d:
  """d4d means divisi for dummies.
     Example: d4d.relations  returns a list of the string names of the conceptnet4 relations
              d4d() creates an instance of d4d contaning various matricies useful for computation.
  """ 
  """in the list for each relation, the first item is the official c4 spelling, the last is the most english-like, use it for generating sentences.
     There is no relation for "is" but there is "is a".
     Note that a relation within a sentence is looked for in the order of the relation synonyms within its list.
     Thus if one synonym starts with the same thing as the whole of another synonym, the longer one should be first
     as in "IsA", "isa", "is a kind of", "is a")  for the last two synonyms.
  """
  relations_map = (
    ("AtLocation", "atlocation", "at location", "are at location", "is at location"),      #Where would you find it?
    ("CapableOf",  "capableof", "capable of", "are capable of", "is capable of"),      #What can it do?
    ("ConceptuallyRelatedTo", "conceptuallyrelatedto", "conceptually related to", "is conceptually related to", "are related to", "is related to"), #What is related to it in an unknown way? 
    ("CreatedBy", "createdby", "created by", "are created by", "is created by"),       #How do you bring it into existence?
    ("Causes", "cause",  "causes"),       #What does it make happen?
    ("CausesDesire", "causesdesire", "cause desire", "causes desire"),    #What does it make you want to do?
    ("DefinedAs", "definedas", "defined as", "are defined as", "is defined as"),       #How do you define it?  
    ("Desires",  "desires", "desire", "likes", "like", "loves", "love", "needs", "need", "want", "wants"),       #What does it want?             
    ("HasA", "hasa", "has a", "have", "have a", "has a property of"),          #What does it possess?
    ("HasProperty",  "hasproperty", "has property", "has the property of"),   #What properties does it have? 
    ("HasSubevent", "hassubevent", "has subevent"),    #What do you do to accomplish it?
    ("HasFirstSubevent", "hasfirstsubevent" "has first subevent"), #What do you do first to accomplish it?
    ("HasLastSubevent",  "haslastsubevent", "has last subevent"), #What do you do last to accomplish it?
    ("HasPrerequisite",  "hasprerequisite", "has prerequisite"), #What do you need to do first?           
    ("IsA", "isa", "is a kind of", "is a"),           #What kind of thing is it?
    ("InheritsFrom", "inheritsfrom", "inherit from", "inherits from"),     #(not stored, but used in some applications)    
    ("LocatedNear", "loctednear", "located near", "are located near", "is located near", "is near"),     #What is it typically near?
    ("MadeOf",  "madeof", "made of", "are made of", "is made of"),         #What is it made of?
    ("MotivatedByGoal",  "motivatedbygoal", "motivated by goal", "is motivated by goal"), #Why would you do it?
    ("ObstructedBy", "obstructedby", "obstructed by", "are obstructed by", "is obstructed by"),   #What would prevent it from happening?           
    ("PartOf", "partof", "part of", "are part of", "is part of"),        #What is it part of?
    ("ReceivesAction", "receivesaction", "receives action", "receive action", "receives the action of"),  #What can you do to it?
    ("SymbolOf", "symbolof", "synmbol of", "are symbol of", "is symbol of"),        #What does it represent?                     
    ("UsedFor", "usedfor", "used for", "are used for", "is used for")         #What do you use it for?
    )
  name              = None
  sparse_matrix     = None
  principal_component_count = None
  concept_axes      = None
  axis_weights      = None
  feature_axes      = None
  sim_matrix        = None
  sim_matrix_normalized = None
  predict_matrix    = None
  assoc             = None
  spread            = None
  
  def __str__(self):
    """enables printing of the predict matrix of a d4d instance to  work.
       Example:
       print(d4d.c4)
    """
    return self.predict_matrix.to_dense().__str__()
  
  
  @classmethod 
  def error(clz, a_string):
    raise Exception(a_string)  

  @classmethod
  def warn(clz, a_string):
    logging.warning(a_string)
   
  @classmethod
  def error_or_warn(clz, a_string, if_bad="warn"):
    if if_bad == "error":
      d4d.error(a_string)
    elif if_bad == "warn":
      d4d.warn(a_string)
      return None
  
  #Initializing d4d instances____________________
  def __init__(self, 
               name="d1", 
               any_format_assertions=None, 
               normalize_concepts=True,
               separator="\n",
               principal_component_count = None,
               if_bad="warn",                   
               ):
    """Example call: 
       d4d("my_mat", d4d.make_sparse_matrix(), principal_component_count=2)
       
    """
    setattr(d4d, name, self)
    self.name = name
    if any_format_assertions == None:
      self.sparse_matrix = d4d.normalize_matrix()
    else:
      self.sparse_matrix = d4d.normalize_matrix(any_format_assertions=any_format_assertions, 
                                                normalize_concepts=normalize_concepts,
                                                separator=separator,
                                                if_bad=if_bad
                                                )
    if principal_component_count == None:
      principal_component_count = self.compute_default_for_principal_component_count()    
    self.principal_component_count = principal_component_count
    print "principal_component_count=" + str(principal_component_count)
    self.concept_axes, self.axis_weights, self.feature_axes = \
        self.sparse_matrix.svd(k=principal_component_count) #k means "number_of_principal_components"
              #concept_axes is refered to by more of the tutorial as U and
              #axis_weights is refered to as upper case greek sigma char. 
    self.sim_matrix = divisi2.reconstruct_similarity(self.concept_axes, self.axis_weights, post_normalize=False)# set to false for getting the most similar items.
    self.sim_matrix_normalized = divisi2.reconstruct_similarity(self.concept_axes, self.axis_weights, post_normalize=True)    
    self.predict_matrix = divisi2.reconstruct(self.concept_axes, self.axis_weights, self.feature_axes)
    # for the below see: http://csc.media.mit.edu/docs/divisi2/tutorial_aspace.html?highlight=reconstruct_activation
    self.assoc = d4d.make_assoc(name, any_format_assertions, normalize_concepts, separator, if_bad='ignore')
            #was: divisi2.network.conceptnet_assoc('en')
            #use if_bad='ignore because if we had warn or error, that would already have happend
            #when doing the above call to normalize_matrix so we don't want to get those messages twice.
    if self.assoc: 
      self.spread = d4d.assoc_to_spread(self.assoc, principal_component_count)   
    return None
  
  """
  @classmethod
  def make_assoc(clz, name, any_format_assertions, normalize_concepts=True, separator="\n", if_bad="warn"):
    if name == "c4":
      return divisi2.network.conceptnet_assoc('en')
    else: #assume we've got real assertions, and we have to roll our own assco matrix.
      #return None #"make_assoc not working"   
      assertions = clz.normalize_assertions(any_format_assertions, normalize_concepts=normalize_concepts, separator=separator, if_bad=if_bad)    
      the_graph = nx.MultiDiGraph()
      the_graph.clear()      
      for an_assertion in assertions:
        weight = 1
        if len(an_assertion) == 4:
          weight = an_assertion[3]
        c1  = an_assertion[0] #concept1, a string
        rel = an_assertion[1] #one of conceptnet4's relations, a string   
        c2  = an_assertion[2] #concept2, a string
        the_graph.add_edge(c1, c2, attr_dict={"rel": rel, "score": weight, "freq":5}) #weight) #attr_dict={"rel": rel, "weight": weight}) #instead of weight could have "score" and "freq"
        the_graph.add_edge(c2, c1, attr_dict={"rel": rel, "score": weight, "freq":5}) #weight) #attr_dict={"rel": rel, "weight": weight})
      #see network.py  conceptnet_assoc() for an example
      mat = divisi2.network.sparse_matrix(the_graph, 'concepts', 'concepts', 3)
      #mat = divisi2.network.sparse_matrix(the_graph, row_labeler='nodes', col_labeler='features',  cutoff=1)  
      return mat 
  """
  
  @classmethod 
  def make_assoc(clz, name, any_format_assertions, normalize_concepts=True, separator="\n", if_bad="warn"):
      """An assoc matrix is square meaning row_labels==col_labels. 
         The weight, ie the value at x and y pos is a float.
      """
      if name == "c4":
        return divisi2.network.conceptnet_assoc('en')
      else: #assume we've got real assertions, and we have to roll our own assco matrix.
        #return None #"make_assoc not working"   
        assertions = clz.normalize_assertions(any_format_assertions, normalize_concepts=normalize_concepts, separator=separator, if_bad=if_bad)          
        named_entries = []
        for an_assertion in assertions:
          weight = 1
          if len(an_assertion) == 4:
            weight = an_assertion[3]
          c1  = an_assertion[0] #concept1, a string
          c2  = an_assertion[2] #concept2, a string
          if c1 < c2: #sort these so that looking thru the list will be faster.
            x = c1
            c1 = c2
            c2 = x
          #see network.py  conceptnet_assoc() for an example
          already_in = False
          for entry in named_entries:
            if (entry[1] == c1) and (entry[2] == c2):
              entry[0] = entry[0] + weight
              already_in = True
              break
          if already_in == False:  #got a unique c1 and c2 pair
            named_entries.append([weight, c1, c2])
        other_entries = []
        for entry in named_entries: 
          other_entries.append([entry[0], entry[2], entry[1]]) #put in the "other" representation 
        named_entries.extend(other_entries)
        mat = divisi2.SparseMatrix.square_from_named_entries(named_entries)          
        return mat 
      
  @classmethod
  def assoc_to_spread(clz, assoc, principal_component_count=2):
    """# see http://csc.media.mit.edu/docs/divisi2/tutorial_aspace.html?highlight=assoc """
    U, S, _ = assoc.svd(k=principal_component_count)
    return divisi2.reconstruct_activation(U, S)      
  
  @classmethod
  def init(clz, principal_component_count = 100):
    d4d.relations = []
    for rel_syn_set in d4d.relations_map:
      d4d.relations.append(rel_syn_set[0])
    d4d("c4", divisi2.network.conceptnet_matrix('en'), principal_component_count)
    
  #UTILS (low level)___________________
  @classmethod
  def is_list_or_tuple(clz, obj, length=None):
    if isinstance(obj, list) or isinstance(obj, tuple):
      if length == None:
        return obj
      else:
        return len(obj) == length
      
  @classmethod   
  def is_string(clz, obj, length=None):
    if isinstance(obj, str) or isinstance(obj, unicode):
      if length == None:
        return obj
      else:
        return len(obj) == length 
      
  @classmethod   
  def is_int_or_float(clz, obj):
    return isinstance(obj, int) or isinstance(obj, float)
  
  @classmethod 
  def string_to_number(clz, a_string):
    """return a number (int or float) or False."""
    try:
      num = int(a_string)
      return num
    except:
      try:
        num = float(a_string)
        return num
      except:
        return False 
      
  @classmethod 
  def print_list(clz, a_list):
    """Prints out the elements of a_list one per line.
       d4d.print_list(["a", "b", "c"])
    """
    result = ""
    for elt in a_list:
      result += repr(elt) + "\n"
    print str(len(a_list)) + " items:\n" + result  
     
  @classmethod
  def cut_up_assertions(clz, any_format_assertions, separator="\n"):
    """any_format_assertions can be a a list, a tuple, a string or a file file, typically made with open("a-file.txt").
       If its a list or tuple, just return it.
       If its a str or unicode, split it with 'separator' and return that.
       If its a file, grab the contents and treat it as a string.
    """
    if isinstance(any_format_assertions, file):
      any_format_assertions = any_format_assertions.read() #just get the file contents as one big string
    if clz.is_list_or_tuple(any_format_assertions):
      return any_format_assertions
    elif clz.is_string(any_format_assertions):
      result = any_format_assertions.split(separator)
      stripped_result = []
      for i in range(0, len(result)): # necesary for "foo isa bar. baz isa frotz." separator="." ,ie no space after final period.
        new_result = result[i].strip()
        if new_result != "": #often get empty string as an assertion on the end.
          stripped_result.append(new_result) 
      if separator.startswith(".") and stripped_result[-1].endswith("."):
        stripped_result[-1] = stripped_result[-1][:-1]
      return stripped_result
    
  @classmethod     
  def find_relation_in_string(clz, a_string):
    """returns a list of normalized_rel, rel_item, start_pos (of the rel_item) within a_string.
       If no relation is found in a_string, [None, None, None] is returned.
       Examples: d4d.find_relation_in_string("boat is a vehicle") == ["IsA", "is a", 5]
       d4d.find_relation_in_string("boat couldn't possibly be a vehicle") == [None, None, None]
    """
    for rel_syn_set in clz.relations_map:
      for rel_item in rel_syn_set:
        start_pos = a_string.find(rel_item)
        if start_pos > 0: #a_string can't BEGIN the relation
          normalized_rel = rel_syn_set[0]
          return [normalized_rel, rel_item, start_pos]
    return [None, None, None]
  
  #classmethod
  def number_of_assertions_in_matrix(self, sparse_matrix):
    return sparse_matrix.nnz / 2
  
  def number_of_assertions(self):
    """Returns an integer of the number of assertions in the sparse_matrix of self.
       d4d.c4.number_of_assertions() == 450404
    """
    return self.sparse_matrix.nnz / 2 #each assertion is represented by 2 entries in the matrix, one with a 'right' feature and one with a 'left' feature

  def is_concept(self, a_string="dog"):
    """a_string is expected to be a normalized string. If the concept is in the d4d instance,
       True is returned, otherwise False.
       d4d.c4.is_concept("dog")  == True
       d4d.c4.is_concept("dogs") == False
       d4d.c4.is_concept("boysenberry") == False
    """
    return a_string in self.sparse_matrix.row_labels
  
  def get_concepts(self):
    """returns a list of the concepts (strings).
       d4d.c4.get_concepts()
    """
    return self.sparse_matrix.__dict__["row_labels"].items 
  
  def get_features(self):
      """returns a list of the features. 
         Each features is a list of: the string 'left' or 'right',
         the string of its relation, and the string of its concept.
         d4d.c4.get_features()
         """
      return self.sparse_matrix.__dict__["col_labels"].items 
    
  def density(self):
      """returns a float between 0 and 1 inclusive indicating
         the number of assertions we actually have as opposed to the number that are possible.
      """
      concept_count = len(self.get_concepts())
      feature_count = len(self.get_features()) 
      total = concept_count * feature_count # consider dividing feature_count by 2 since each concept/relation pair can be configured in 2 ways  
      ass_count = self.number_of_assertions()     
      return ass_count / float(total) # so I don't get integer divide truncation.
    
  def compute_default_for_principal_component_count(self):
    """returns an integer between 1 and 100 inclusive.
       Number of columns increases the number, as does density
    """
    feature_count = len(self.get_features())
    raw_score     = feature_count * self.density()
    if raw_score <= 1:
      return 1
    elif raw_score >= 100:
      return 100
    else:
      return int(math.ceil(raw_score))
    
  def get_relations(self):
    """returns a list of the relations used in the matrix. There are no duplicates.
       d4d.c4.get_relations()
    """
    result = set()
    for feat in self.get_features():
      result.add(feat[1])
    return list(result) 
  
  def is_relation(self, relation_string):
      """returns True if the relaition in relation_string is in the matrix.
         relation_string is expected to be normalized.
      """
      for feat in self.get_features():
        if feat[1] == relation_string:
          return True
      return False  
  
  @classmethod 
  def is_valid_relation(clz, a_string='IsA', strict=True):
    """ Returns True if a_string is a valid relation, independent of any instance of d4d.
        If 'strict' is True (the default) then a_string must be an exact spelling of a relation.
        Otherwise, a_string can be a synonym.
        d4d.is_valid_relation("IsA",  strict=True)  == True
        d4d.is_valid_relation("is a", strict=True)  == False
        d4d.is_valid_elation("is a",  strict=False) == True
        d4d.is_valid_relation("X",    strict=False) == False
    """
    if strict:
      for rel_syn_set in clz.relations_map:
        if a_string == rel_syn_set[0]:
          return True
    else:
      for rel_syn_set in clz.relations_map:
        if a_string in rel_syn_set:
          return True      
    return False
  
  #Normalize_____________________________________
  @classmethod 
  def normalize_relation(clz, a_string='is a', if_bad="warn"):
    """ Return the conceptnet4 correct spelling for the relation indicated by 'a_string' or False if none.
         d4d.normalize_relation("is used for") == "UsedFor"
         d4d.normalize_relation("no way") == None
    """
    a_string = a_string.strip().lower()
    for rel_syn_set in clz.relations_map:
      if a_string in rel_syn_set:
        return rel_syn_set[0]    
    return d4d.error_or_warn("d4d could not normalize relation: " + a_string, if_bad)
  
  @classmethod
  def abnormalize_relation(clz, a_string="is a", if_bad="warn"):
    """ Return the conceptnet4 correct spelling for the relation indicated by 'a_string' or False if none.
        d4d.abnormalize_relation("UsedFor") == "is used for"
        d4d.abnormalize_relation("NoWay") == None
    """
    for rel_syn_set in clz.relations_map:
      if a_string in rel_syn_set:
        return rel_syn_set[-1] 
    return d4d.error_or_warn("d4d could not abnormalize relation: " + a_string, if_bad)
  
  @classmethod
  def normalize_concept(clz, a_string="Books"):
    """returns a string that has been normalized, but not looked up in conceptnet4 to see if the concept actually exist.
       d4d.normalize_concept("The Boysenberries") == "boysenberry"
    """
    return en_nl.normalize(a_string)
  
  @classmethod
  def abnormalize_concept(clz, a_string="class", capitalize=False, pluralize=False):
    """ Examples:
        d4d.abnormalize_concept("class") == "class"
        d4d.abnormalize_concept("class", capitalize=True, pluralize=True) == "Classes"
    """
    if capitalize:
      a_string = a_string.capitalize()
    if pluralize:
      last_char = a_string[-1]
      if last_char == "s":
        a_string = a_string + "es"
      elif last_char == "y":
        a_string = a_string[0:-1] + "ies"
      else:
        a_string = a_string + "s"    
    return a_string
  
  @classmethod
  def concept_and_feature_to_assertion(clz, concept="teach", feature=('left', u'CapableOf', u'person')):
    """This function not normally useful.
       Example:  
       d4d.concept_and_feature_to_assertion("dog", ('right', u'Desires', u'dogfood'))  
    """
    if feature[0] == 'right':
      return (concept, feature[1], feature[2])
    else:
      return (feature[2], feature[1], concept)
  # [(('right', u'IsA', u'instrument'), 1.0953420256266928), (('right', u'UsedFor', u'make music'), 1.065034405329375), (('right', u'IsA', u'musical instrument'), 1.0037759881111907), (('right', u'UsedFor', u'play music'), 0.97773039626061509), (('right', u'AtLocation', u'band'), 0.77881846884819117), (('right', u'AtLocation', u'orchestra'), 0.72398351131428718), (('right', u'UsedFor', u'music'), 0.64599245793345172), (('right', u'AtLocation', u'music store'), 0.56730362308006144), (('right', u'UsedFor', u'create music'), 0.43499642238639497), (('right', u'UsedFor', u'play'), 0.42812609356753906)]
  
  
  @classmethod
  def normalize_assertion(clz, any_format_assertion, normalize_concepts=True, if_bad="warn"):
    """Returns a normalized assertion is a list of concept1 string, relation string, concept2 string, and optionally a weight int or float.
       OR returns None if any_format_assertion is not a handled assertion format or its relation is not a Conceptnet4 relation.
       d4d.normalize_assertion("A Television CreatedBy Acme")         == [u'television', 'CreatedBy', u'acme', 1]
       d4d.normalize_assertion("A Television is created by Acme 0.9") == [u'television', 'CreatedBy', u'acme', 0.9]
       d4d.normalize_assertion("A Television is screwed up by Acme")  == None
       d4d.normalize_assertion(["dogs", "desire", "dogfood"])   weight defaults to 1.0
       d4d.normalize_assertion(["dogs", "desire", "dogfood", 0.5])
       
    """  
    afa = any_format_assertion
    result_list = None
    if clz.is_list_or_tuple(afa, 2): #weighted triples
      if clz.is_list_or_tuple(afa[0], 3) and clz.is_int_or_float(afa[1]):
        result_list = [afa[0][0], afa[0][1], afa[0][2], afa[1]]
      else: 
        return d4d.error_or_warn("normalize_assertion was passed: " + str(any_format_assertion) + \
                                 " but 2 element lists must have a first element that's of length 3 and a 2nd element that's a number.",
                                 if_bad=if_bad)
    elif clz.is_list_or_tuple(afa, 3):
      result_list = afa
    elif clz.is_list_or_tuple(afa, 4):
      result_list = afa    
    elif clz.is_string(afa):
      afa = afa.strip()
      words = afa.split(" ")
      last_word = words[-1]
      weight = clz.string_to_number(last_word)
      crc = afa #concept,relation, concept
      if weight:
        crc = afa[0: -len(str(weight))].strip() #cut off the weight
      else:
        weight = 1
      normalized_rel, orig_rel, start_pos = clz.find_relation_in_string(crc)
      if normalized_rel == None:
        result_list =  None
      else:
        concept1 = crc[0: start_pos].strip()
        concept2 = crc[start_pos + len(orig_rel) + 1:].strip()
        if normalize_concepts:
          concept1 = clz.normalize_concept(concept1)
          concept2 = clz.normalize_concept(concept2)
        result_list = [concept1, normalized_rel, concept2, weight] 
    if result_list == None:     
      return d4d.error_or_warn("d4d could not normalize assertion: " + any_format_assertion, if_bad)
    else:
      return result_list 
  
  @classmethod
  def abnormalize_assertion(clz, an_assertion=["boat", "IsA", "vehicle", 1]):
    """ Returns a string that approximates English representing an_assertion.
        If the weight is not equal to 1, the weight is included on the end of the string.
        d4d.abnormalize_assertion(["boat", "IsA", "vehicle", 1])    == "Boat is a kind of vehicle"
        d4d.abnormalize_assertion(["boat", "IsA", "vehicle", 0.77]) == "Boat is a kind of vehicle 0.77"
    """
    result = clz.abnormalize_concept(an_assertion[0], capitalize=True) + " " + \
             clz.abnormalize_relation(an_assertion[1]) + " " + \
             an_assertion[2]
    if len(an_assertion) == 4 and an_assertion[3] != 1:
      result = result + " " + str(an_assertion[3])
    return result
  
  @classmethod
  def normalize_assertions(clz, 
                           any_format_assertions="Cat is a mammal\nCats are capable of climbing", 
                           normalize_concepts=True, 
                           separator="\n",
                           concept_separator=",",
                           concept1_column=1,
                           relation_column=2,
                           concept2_column=3,
                           weight_column = None,
                           first_row=1,
                           last_row="end",                           
                           if_bad="warn" #can be "ignore", "error" or "warn" 
                          ):
    """Returns a list of normalized assertions.
       If an assertion is bad, then the value of 'if_bad' determines the behavior.
       A value of 'error' (the default) causes normalize_assertions to error on the first bad assertion.
       A value of 'ignore' ignores the bad assertion and it will not be in the returned list.
       any_format)_assertions can be a file containing assertions.
       Examples: 
       d4d.normalize_assertions('Television is used for entertainment.   Entertainment   is a kind of   fun.', separator='.') 
       d4d.normalize_assertions(open("asserts.txt"))  #foo.txt is a file in the same folder as this file
                                                      #that has any format assertions
                                                      
       If any_format_assertions is a file who's name ends in '.csv', then the parameters
       concept_separator, concept1_column, relation_column, concept2_column, weight_column, first_row, last_row
       are used in a call to normalize_assertions_from_csv (see its doc for details) otherwise they are ignored.
       """
    if isinstance(any_format_assertions, file) and any_format_assertions.name.endswith(".csv"):
      return d4d.normalize_assertions_from_csv(any_format_assertions, normalize_concepts=normalize_concepts, separator=separator, 
                                               concept_separator=concept_separator,
                                               concept1_column=concept1_column,
                                               relation_column=relation_column,
                                               concept2_column=concept2_column,
                                               weight_column = weight_column,
                                               first_row=first_row,
                                               last_row=last_row,                                      
                                               if_bad=if_bad)
    assertions = clz.cut_up_assertions(any_format_assertions, separator)
    result = [] 
    for a in assertions:
      if a != "": #could happen due to the split
        norm_assertion = clz.normalize_assertion(a, normalize_concepts=normalize_concepts, if_bad=if_bad)
        if norm_assertion != None:
          result.append(norm_assertion)
    return result  
  
  @classmethod
  def normalize_assertions_from_csv(clz, 
                             file_or_csv_string="Cat, isa, mammal\nCats, are capable of, climbing", 
                             normalize_concepts=True, 
                             separator="\n",
                             concept_separator=",",
                             concept1_column=1,
                             relation_column=2,
                             concept2_column=3,
                             weight_column = None,
                             first_row=1,
                             last_row="end",
                             if_bad="warn" #can be "ignore", "error" or "warn" 
                            ):
      """Returns a list of normalized assertions.
         If an assertion is bad, then the value of 'if_bad' determines the behavior.
         A value of 'error' (the default) causes normalize_assertions to error on the first bad assertion.
         A value of 'ignore' ignores the bad assertion and it will not be in the returned list.
         any_format)_assertions can be a file containing assertions.
         Examples: 
         d4d.normalize_assertions_from_csv("Cat, isa, mammal\nCats, are capable of, climbing") 
         d4d.normalize_assertions_from_csv(open("android_assertions.csv"), first_row=2, concept1_column=2, relation_column=3, concept2_column=4)
        android_assertions.csv is a file in the same folder as this file
        
        csv files can be viewed in a spreadsheet like Excel, and you can save files in csv format from Excel.
        
        This function has a bunch of flexibility with such files.
        Each row in the spreadsheet indicates an assertion.
        Columns specify concept1, relation, concept2 and, optionally, weight for the assertion.
        Often there is a header row or two. You can ignore them by setting first_row to the number of the first row.
        This is ONE based (not zero based) and corresponds to the numbering of rows in Excel.
        last_row lets you ignore rows below the mentioned row (one based).
        concept1_column, relation_column and concept2_column let you designate where those parts of an assertion will
        be found. These are also "one based". In Excel, Column A is refered to by 1, Column B by 2, etc.
        
        csv uses a comma between elements in a row and newline between rows, which are the defaults for this function,
        but you can customize that with concept_separator and separation (used between rows).
        If weight_column is None, then weight will default to 1, otherwise, it will pull the wieght
        for each assertion from that column.
        
        relations are always normalized. concepts are only normalized if normalize_concepts=True, which is the default.    
      """
      assertions = clz.cut_up_assertions(file_or_csv_string, separator)
      result = [] 
      min_row_elt_length = None
      if weight_column == None:
         min_row_elt_length = max(concept1_column, relation_column, concept2_column)
      else:
         min_row_elt_length = max(concept1_column, relation_column, concept2_column)
      for row_index in range(0, len(assertions)):
        row_index += 1 #row index is 1 based
        if row_index < first_row:
          pass
        elif (last_row != "end") and (row_index > last_row):
          break
        else: #could happen due to the split
          row_string = assertions[row_index - 1].strip()      
          row_elts = row_string.split(concept_separator)
          if len(row_elts) < min_row_elt_length:
            d4d.error_or_warn("d4d could not normalize relation from csv: " + row_string, if_bad)
          else:
            c1  = row_elts[concept1_column - 1]
            rel = row_elts[relation_column - 1]
            c2  = row_elts[concept2_column - 1]
            weight = 1.0
            if isinstance(weight_column, int):
              weight = row_elts[weight_column - 1]
            rel = d4d.normalize_relation(rel, if_bad=if_bad)
            if rel == None:
              pass 
            else:
              if normalize_concepts:
                c1 = d4d.normalize_concept(c1)
                c2 = d4d.normalize_concept(c2)
              result.append([c1, rel, c2, weight])
      return result   
  
  @classmethod
  def abnormalize_assertions(clz, 
                             assertions=[("cat", "IsA", "mammal", 1.0), ("cat" "CapablOf", "climbing", 0.9)], 
                             separator="\n"
                             ):
    """ Returns a string representing the assertions approximately in English.
        d4d.abnormalize_assertions(assertions=[("cat", "IsA", "mammal", 1.0), ("cat", "CapableOf", "climbing", 0.9)], separator=". ")
    """
    result = ""
    for a in assertions:
      result += clz.abnormalize_assertion(a) + separator
    return result
  
  @classmethod
  def normalize_matrix(clz, 
                       any_format_assertions="Television is a product\nTelevision is created by Acme",
                       normalize_concepts=True,
                       separator="\n",
                       if_bad="warn"):  
    """Returns a concept by feature sparse matrix.
       This is not a top level function."""
    #the_graph = G=nx.MultiDiGraph()
    #the_graph.clear()
    mat = None;
    if isinstance(any_format_assertions, divisi2.sparse.SparseMatrix):
      return any_format_assertions
    elif isinstance(any_format_assertions, d4d):
      return any_format_assertions.sparse_matrix
    else:
      assertions = clz.normalize_assertions(any_format_assertions, normalize_concepts=normalize_concepts, separator=separator, if_bad=if_bad)    
      if assertions == None:
        return None
      else:
        return clz.well_formatted_assertions_to_matrix(assertions)
  
  @classmethod  
  def well_formatted_assertions_to_matrix(clz, assertions):
    """Internal method. Does no normalization. If you don't have the proper spelling of a relation,
       it will not error immediately, but sooner or later, you'll get an error using the d4d methods
       on a matrix built with a misspelled relation.
       Example:
      d4d.well_formatted_assertions_to_matrix([["joe", "Desires", "mary"],["mary", "Desires", "sam"]])
    """
    formatted_asses = []      
    for an_assertion in assertions:
      weight = 1
      if len(an_assertion) == 4:
        weight = an_assertion[3]
      c1  = an_assertion[0]
      rel = an_assertion[1]    
      c2  = an_assertion[2] 
      #the_graph.add_edge(c1, c2, attr_dict={"rel": rel, "weight": weight}) #instead of weight could have "score" and "freq"
      formatted_asses.append([weight,c1, ('right', rel, c2)])
      formatted_asses.append([weight,c2, ('left',  rel, c1)])
    #mat = divisi2.network.sparse_matrix(the_graph, row_labeler='nodes', col_labeler='features',  cutoff=1)  
    mat = divisi2.make_sparse(formatted_asses)
    return mat 
  
  @classmethod
  def abnormalize_matrix(clz, sparse_matrix, assertion_count=10, separator="\n", show_weights=True):
    """Returns a string of assertion_count number of assertions in sparse_matrix.
       If matrix doesn't have that many asssertions, it returns all the asssertions in sparse_matrix.
       If assertion_count is "all", return all the assertions in the sparse_matrix.
       This is not advisable for large a matrix like d4d.c4.sparse_matrix.
       Within the returned string will be abnormalized versions of the assertions.
       If show_weights is True, the default, then the weight of each asssertion is shown between concept2
       and the separator. However, if the weight == 1, then its never shown as that's the default weight.
       This is not a top level function.
    """
    result = ""
    result_count = 0
    entries = sparse_matrix.named_entries()
    for assertion_entry_index in range(0, len(entries)): #looping over the entries directly doesn't work, either python bug or just too slow
      assertion_entry = entries[assertion_entry_index]
      feature = assertion_entry[2]
      if feature[0] == "right":  # the 'left' features are redundant entries
        weight = assertion_entry[0]        
        concept1 = assertion_entry[1]
        rel = feature[1]
        concept2 = feature[2]
        if weight == 1 or show_weights == False:
          ab_assertion = clz.abnormalize_concept(concept1, capitalize=True) + " " + \
                         clz.abnormalize_relation(rel) + " " + \
                         concept2 + separator
        else:
          ab_assertion = clz.abnormalize_concept(concept1, capitalize=True) + " " + \
                         clz.abnormalize_relation(rel) + " " + \
                         concept2 + " " + str(weight) + separator          
        result += ab_assertion
        result_count += 1
        if isinstance(assertion_count, int) and result_count >= assertion_count:
          break 
    return result
  
  @classmethod
  def normalize(clz,
                name="d1", 
                any_format_assertions=None,  
                normalize_concepts=True,
                separator="\n",
                principal_component_count=None,
                if_bad="warn"):
    """ This method is just a simple wrapper for making an instance of d4d that conforms to
        the "normalize" pattern of method calls.
        Examples:
        d4d.normalize("my_mat", "Television is a product\nTelevision is created by Acme")
        d4d.my_mat.similar_concepts_to("television")     
    """
    return d4d(name=name, 
               any_format_assertions=any_format_assertions,
               normalize_concepts=normalize_concepts,
               separator=separator,
               principal_component_count=principal_component_count,  
               if_bad=if_bad)
    
  def abnormalize(self, assertion_count=10, separator="\n", show_weights=True):
    """Returns a string of assertion_count assertions.
       d4d.c4.abnormalize(assertion_count=4, separator=". ", show_weights=False)
    """
    return self.abnormalize_matrix(self.sparse_matrix, assertion_count=assertion_count, separator=separator, show_weights=show_weights)
    
  #Common Sense methods__________________________
  def similar_concepts_to(self, concept='teach', result_count=10):
    """Example calls: 
        d4d.c4.similar_concepts_to() 
        d4d.c4.similar_concepts_to(concept='teach')
        Return example: [(u'teach', 1.0000000000000004), (u'research', 0.76193856500095036), (u'pass information', 0.68245192755785722), (u'teach child', 0.67728091668145329), (u'gain knowledge', 0.66468104212733714), (u'teach student', 0.66417014045814737), (u'take beach', 0.66001488082134274), (u'goof off', 0.65920319922769444), (u'learn new', 0.65764429870918806), (u'acquire knowledge', 0.65712316977028984)]
        The numbers vary from +1 to -1 (except note occassionally just over or under those limits.)
    """
    return self.sim_matrix.row_named(concept).top_items(result_count)
   
  
  def assertions_about(self, concept='teach', concept_position='both', result_count=10):
    """Example calls: 
       d4d.c4.assertions_about(concept='teach', concept_position='left')
       d4d.c4.assertions_about(concept='teach', concept_position='right')
    """
    feats = self.predict_matrix.row_named(concept).top_items(result_count) 
    result = []
    for feat_score in feats:
      feat = feat_score[0]
      feat_pos = feat[0]
      if concept_position == 'both' or concept_position != feat_pos:
        result.append(d4d.concept_and_feature_to_assertion(concept, feat)) 
    return result
  
  def how_true_is(self, concept1_or_any_format_assertion='person', relation='CapableOf', concept2='teach'):
    """returns a number beteen -1 and 1 with -1 indicating false and 1 indicating true.
       Note that most of the time, a returned value of 0, ie "no information" can be considered false.
       Examples: 
       d4d.c4.how_true_is("dog is a pet") 
       d4d.c4.how_true_is('dog', 'IsA', 'pet') 
       Warning: If the first arg cannot be interpreted as an asssertion, it will be used as a concept.
       If the first arg IS interpreted as an assertion, the other args will be ignored.
    """
    concept1 = None
    if d4d.is_string(concept1_or_any_format_assertion):
      concept1_or_any_format_assertion.strip()
      if concept1_or_any_format_assertion.endswith("."):
        concept1_or_any_format_assertion = concept1_or_any_format_assertion[0:-1]
      ass = d4d.normalize_assertion(concept1_or_any_format_assertion, if_bad='ignore')
      if ass == None:
        concept1 = concept1_or_any_format_assertion
      else:
        concept1 = ass[0] 
        relation = ass[1] 
        concept2 = ass[2]        
    else:
      concept1 = concept1_or_any_format_assertion[0] 
      relation = concept1_or_any_format_assertion[1] 
      concept2 = concept1_or_any_format_assertion[2]  
    try:
      return self.predict_matrix.entry_named(concept1, ('right', relation, concept2))
    except:
      return 0.0

#http://csc.media.mit.edu/docs/divisi2/tutorial_aspace.html
#how to load a bunch of assertions: But what is the format of the assertion file?

  def how_similar_are(self, concept1="dog", concept2="cat"):
    """Returns a number between 0 and 1.
       Examples: 
       d4d.c4.how_similar_are("cat", "dog")  
       d4d.c4.how_similar_are("cow", "bell")
    """
    return self.sim_matrix_normalized.entry_named(concept1, concept2) 

  def how_related_are(self, concept1="dog", concept2="cat"):
    """Relatedness is not the same as concept similarity. Rather, 
      it tells you how close are two concepts in the network.
      For example, "mother" could be closely related to milk but mother and milk are not similar.
      d4d.c4.how_related_are("cow", "bell")
      d4d("d1", [('television', 'IsA',       'product', 1.0), 
                 ('television', 'CreatedBy', 'Acme',    0.6)
                ])
      d4d.d1.how_related_are("television", "product")
    """
    return self.spread.entry_named(concept1, concept2) #bug


  #bug: seems to know about c4 even when we have another matrix built from scatch with no c4 blended in
  #as in d4d.d1.concepts_most_related_to("television")
  def concepts_most_related_to(self, concept="dog", result_count=10):
    """Returns a list of the concepts most related to the given concept.
       Examples: 
       d4d.c4.concepts_most_related_to() 
       d4d.c4.concepts_most_related_to("television") 
    """
    return self.spread.row_named(concept).top_items(result_count) 
  
  
  
  # CATEGORIES http://csc.media.mit.edu/docs/divisi2/tutorial_category.html
  # Making a category of concepts with keyword + weight or just a list of concepts:
  # happy = divisi2.category(happy=1, sad=-1)
  # transport = divisi2.category('car', 'bus', 'train', 'bicycle') 
  def concepts_in_category(self, category, get_opposites=False, count=10):
    """ returns a list of tuples, each has a concept name as string and a weight of that concept within the category.
        The returned list will likely have SOME of the concepts in the input category but will have others
        if count is high enough.
        The input category can be in 5 formats, examples of each:
        Note the first 2 allow you to specify weights for each concept,
        but the later 3 treat each concept equally.
        1. divisi2.category(happy=1, sad=-1)
        2. {"happy":1, "sad":-1}
        3. divisi2.category('car', 'bus', 'train', 'bicycle') 
        4  ("car", "bus", "train")
        5. [car", "bus", "train"]
        Full Examples: 
        d4d.c4.concepts_in_category({"happy":1, "sad":-1}, count=5)
        d4d.c4.concepts_in_category({"happy":1, "sad":-1}, get_opposites=True, count=5)
        d4d.c4.concepts_in_category(("bus", "train", "car"), count=15)
                       
    """
    if isinstance(category, list) or isinstance(category, tuple):
      if get_opposites:
        category = -divisi2.category(*category)
      else:
        category = divisi2.category(*category)
    elif isinstance(category, dict):
      if get_opposites:
        category = -divisi2.category(**category)
      else:
        category = divisi2.category(**category)
    elif get_opposites:
      category = -category    
    return self.sim_matrix_normalized.left_category(category).top_items(count)
  
  def related_concepts_in_category(self, category, get_opposites=False, count=10):
      """ returns a list of tuples, each has a concept name as string and a weight of that concept within the category.
          The returned list will likely have SOME of the concepts in the input category but will have others
          if count is high enough.
          The input category can be in 5 formats, examples of each:
          Note the first 2 allow you to specify weights for each concept,
          but the later 3 treat each concept equally.
          1. divisi2.category(happy=1, sad=-1)
          2. {"happy":1, "sad":-1}
          3. divisi2.category('car', 'bus', 'train', 'bicycle') 
          4  ("car", "bus", "train")
          5. [car", "bus", "train"]
          Full Examples: 
          d4d.c4.related_concepts_in_category({"happy":1, "sad":-1}, count=5)
          d4d.c4.related_concepts_in_category({"happy":1, "sad":-1}, get_opposites=True, count=5)
          d4d.c4.related_concepts_in_category(("bus", "train", "car"), count=15)
                         
      """
      if isinstance(category, list) or isinstance(category, tuple):
        if get_opposites:
          category = -divisi2.category(*category)
        else:
          category = divisi2.category(*category)
      elif isinstance(category, dict):
        if get_opposites:
          category = -divisi2.category(**category)
        else:
          category = divisi2.category(**category)
      elif get_opposites:
        category = -category
      return self.spread.left_category(category).top_items(count)  
   
  def discover_assertions(self, concept, max_weight=0.98, min_weight=0.5):
    rels = self.get_relations()
    concepts = self.get_concepts()
    concepts.remove(concept)
    results = []
    for rel in rels:
      for con in concepts:
        weight = self.how_true_is(concept, rel, con)
        if max_weight >= weight >= min_weight:
          results = [concept, rel, con, weight]
        weight = self.how_true_is(con, rel, concept)
        if max_weight >= weight >= min_weight:
          results = [con, rel, concept, weight]      
    return results
      


d4d.init()
# blending http://csc.media.mit.edu/docs/divisi1/tutorial_blending.html?highlight=blending
@classmethod
def blend(clz, 
          name="b1",
          list_of_matrix=[d4d.c4, 
                          [('television', 'IsA',       'product', 1.0), 
                           ('television', 'CreatedBy', 'Acme',    0.6)]
                          ],   
          normalize_concepts=True,
          separator="\n",
          factors=None,
          post_weights=None,          
          ):
      """Blend a list of custom matrix, usually only 2 long.
        Returns an instance of d4d containing a blend of the matricies in list_of_matrix.
        name: The name of the returned d4d instance. 
        Defaults to "b1".
        list_of_matrix: a list of sparse matricies to blend.
        Items in this list can also be instances of d4d, or any_format_assertions, in which case we convert it into a sparse matrix.
        Defaults to: d4d.c4 (conceptnet 4) and a simple 2 assertion matrix.
        factors: List of scaling factor for each matrix.
        Defaults to: None which is used to mean the reciprocal of the first singular value is used.
        post_weights: List of weights to apply to each scaled matrix.
        You can use this to, for example, say that one matrix is twice as
        important as another. 
        Defaults to: None, meaning no post-weighting is performed.
         Example: 
         d4d.blend("b2", [d4d.c4, 
                         [('television', 'IsA',       'product', 1.0), 
                          ('television', 'CreatedBy', 'Acme',    0.6)]
                        ])  
      """
      mats = []
      for mat in list_of_matrix:
        mat = d4d.normalize_matrix(mat, separator=separator, normalize_concepts=normalize_concepts)
        mats.append(mat)
      return d4d(name, divisi2.blend(mats, factors=factors, post_weights=post_weights)) #Blend(ms).svd()
    
d4d.blend = blend #not put inside of class def since I wanted the default value for list_of_matrix to
                  #use d4d.c4
                  


print "d4d.py loaded"
# Diagnostics  
# self.get_col_labels().items self.get_row_labels().items

# d4d.d1.number_of_assertions()
# d4d.d1.concepts_most_related_to("dog")
# d4d.d1.similar_concepts_to("dog")
# d4d.d1.similar_concepts_to("fish")
# d4d.d1.how_related_are("cat", "dog")
#d4d.normalize_assertions_from_csv(open("android_assertions.csv"), first_row=2, concept1_column=2, relation_column=3, concept2_column=4)

"""
d4d("d1", [('television', 'IsA',       'product', 0.8), 
           ('television', 'IsA',       'product', 1.0),
           ('product', 'CreatedBy', 'Acme',    0.6),
           ('Acme', 'IsA', 'company',    0.4)
           ])
print d4d.assoc_to_spread(d4d.d1.assoc, 3).to_dense() #any other princ component count than 3 gives bad results
"""
