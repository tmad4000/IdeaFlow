#translates dustin's common consensus json assertions into d4d assertions
import json
import os
from d4d import d4d
class d4dcc:
  
  @classmethod
  def normalize_relation(clz, rel):
    return {u'action_app':'UsedFor', 
            u'concept_concept':'ConceptuallyRelatedTo',
            u'contenttype_device':'UsedFor2', #2 suffix means arg2 becomes concept1 and arg1 is concept2
            u'device_action':'UsedFor',
            u'device_location':"AtLocation",
            'duration_of_action': "MadeOf",
            u'location_action':"LocatedNear",
            'isa':'IsA',
            'motivation_of': "MotivatedByGoal",
            'part_of': "PartOf",
            'type_of': "IsA"}[rel]
  
  @classmethod 
  def unique_predicates(clz, filename):
    """
    d4dcc.unique_predicates("common_consensus_samsung_predicates.json")
    """
    src = open(filename).read()
    js_array = val = json.loads(src)
    two_arg_preds = []
    for js_obj in js_array:
      if len(js_obj["arguments"]) == 2:
        pred = js_obj["predicate"]
        two_arg_preds.append(pred)
    two_arg_preds = list(set(two_arg_preds))
    two_arg_preds.sort()
    return two_arg_preds
  
  @classmethod 
  def cc_to_assertions(clz, filename):
      """filename is a string representing a file containing json assertions in cc format,
         or a dir name containing files containing json assertions in cc format.
      d4dcc.print_list(d4dcc.cc_to_assertions("assertion_data/cc_samsung_predicates.json"))
      d4dcc.print_list(d4dcc.cc_to_assertions("assertion_data"))
      """
      assertions = []
      if isinstance(filename, str):
        if os.path.isdir(filename):
          for file_str in os.listdir(filename):
            full_name = filename + "/" + file_str
            clz.full_filename_to_assertions(full_name, assertions)
        else:
          clz.full_filename_to_assertions(filename, assertions)
      return assertions
   
  @classmethod         
  def full_filename_to_assertions(clz, full_filename, assertions):
      src = open(full_filename, "r").read()
      js_array = val = json.loads(src) 
      clz.cc_to_assertions_js_obj(js_array, assertions)
      return assertions
   
  @classmethod    
  def cc_to_assertions_js_obj(clz, js_array, assertions):
    for js_obj in js_array:
      if len(js_obj["arguments"]) == 2:
        pred = js_obj["predicate"]
        arg1 = js_obj["arguments"][0]["value"]
        arg2 = js_obj["arguments"][1]["value"]
        rel = clz.normalize_relation(pred)
        ass = None
        if rel[-1] == "2":
          rel = rel[0:-1]
          ass = [arg2, rel, arg1]
        else:
          ass = [arg1, rel, arg2]
        if not(ass in assertions): #remove duplicates
          assertions.append(ass)
    return assertions
  
  @classmethod 
  def print_list(clz, a_list):
    result = ""
    for elt in a_list:
      result += repr(elt) + "\n"
    print str(len(a_list)) + " assertions:\n" + result
  
"""diaognostics and various tests
d4dcc.print_list(d4dcc.cc_to_assertions("assertion_data/cc_samsung_predicates.json"))
d4dcc.print_list(d4dcc.cc_to_assertions("assertion_data"))

d4d.normalize("d2", d4dcc.cc_to_assertions("assertion_data")) 
d4d.d2.how_true_is("tv", "ConceptuallyRelatedTo", "boobtube")
d4d.d2.how_true_is("dvd", "ConceptuallyRelatedTo", "tv")
d4d.blend("b2", [d4d.c4, d4d.d2])
d4d.b2.how_true_is("tv", "ConceptuallyRelatedTo", "boobtube")
d4d.b2.how_true_is("dvd", "ConceptuallyRelatedTo", "tv")

os.getcwd() current working directory
os.getlogin() errors but doced to get logged in user.
os.listdir(path)
os.path.isdir("assertion_data")
"""