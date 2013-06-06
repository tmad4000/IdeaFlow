#translates dustin's common consensus json assertions into d4d assertions
import json
import os
from cStringIO import StringIO
from ../../d4d import d4d
class d4dcc:
  
  @classmethod
  def normalize_relation(clz, rel):
    return {'action_app':        'UsedFor', 
            'concept_concept':   'ConceptuallyRelatedTo',
            'contenttype_device':'UsedFor2', #2 suffix means arg2 becomes concept1 and arg1 is concept2
            'device_action':     'UsedFor',
            'device_location':   'AtLocation',
            'duration_of_action':'MadeOf',
            'location_action':   'LocatedNear',
            'isa':               'IsA',
            'motivation_of':     'MotivatedByGoal',
            'part_of':           'PartOf',
            'type_of':           'IsA'}[rel]
  
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
        if not(arg1 == arg2): # we want to filter out things like 'phone Usedfor phone' because it causes a bug deep in the graph code when making the matrixes
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
    
  # This code originally came from write_packed in the file packed_matrix.py
  @classmethod 
  def write_svdview_files(clz, d4d_instance_or_matrix, labels=None, out_basename=None, cutoff=40):
      """
      svdview is the pretty, 3D view of concepts. The display software needs
      2 data files in a special format.
      This method produces those 2 files in the same folder as this source file.
      Those 2 files have extensions of .coords and .names
      The .coords file is a binary file.
      The .names file is just a list of the concept names.
      If files by those names already exist, they will be overwritten.
      See the file svdview_doc.txt for how to display that data.
      Example use:
      d4d.normalize("Samsung_CC_Without_CN4", d4dcc.cc_to_assertions("assertion_data"), principal_component_count=10) 
      d4dcc.write_svdview_files(d4d.Samsung_CC_Without_CN4)
      Warning: the above call may take several minutes. 
      You will see a statement in your python console telling you when its done.
      """
      matrix = None
      if isinstance(d4d_instance_or_matrix, d4d):
        matrix = d4d_instance_or_matrix.predict_matrix
        if out_basename == None:
          out_basename = d4d_instance_or_matrix.name        
      else:
        matrix = d4d_instance_or_matrix
        if out_basename == None:
          out_basename = "svd_data"
      if labels == None:
        labels = d4d_instance_or_matrix.get_concepts()
      
      import struct
      
      num_vecs, num_dims = matrix.shape
      if num_dims > cutoff: num_dims = cutoff
      
      coords_str_io = StringIO()  
      names_str_io  = StringIO()         
      coords_str_io.write(struct.pack('>ii', num_dims, num_vecs))
  
      # Write the whole file.
      format_str = '>' + 'f'*num_dims  
      for row in xrange(len(labels)):
          concept = labels[row]
          vec = matrix[row, :]
          cutoff_vec = vec[:cutoff]
          payload = struct.pack(format_str, *cutoff_vec)
          coords_str_io.write(payload)
          names_str_io.write(concept)
          names_str_io.write('\n')
      coords_file_name = out_basename + '.coords'
      names_file_name  = out_basename + '.names'
      coords = open(coords_file_name, 'wb') #open empties any existing file by that name.
      coords.write(coords_str_io.getvalue())
      coords.close()
      names  = open(names_file_name,'wb')
      names.write(names_str_io.getvalue())  
      names.close()
      print("The files: " + coords_file_name + " and " +  names_file_name + " have been made.")
      

print "d4dcc.py loaded"  


"""diaognostics and various tests
d4dcc.print_list(d4dcc.cc_to_assertions("assertion_data/cc_samsung_predicates.json"))
d4dcc.print_list(d4dcc.cc_to_assertions("assertion_data"))

d4d.normalize("Samsung_CC_Without_CN4", d4dcc.cc_to_assertions("assertion_data/cc_samsung_predicates.json"), principal_component_count=10) 
d4d.normalize("Samsung_CC_Without_CN4", d4dcc.cc_to_assertions("assertion_data"), principal_component_count=10) 

d4dcc.write_svdview_files(d4d.Samsung_CC_Without_CN4)
#see the file in this folder "svd_view_doc.txt" for how to visualize these files.



d4d.d2.how_true_is("tv", "ConceptuallyRelatedTo", "boobtube")
d4d.d2.how_true_is("dvd", "ConceptuallyRelatedTo", "tv")
d4d.blend("b2", [d4d.c4, d4d.d2])
d4d.b2.how_true_is("tv", "ConceptuallyRelatedTo", "boobtube")
d4d.b2.how_true_is("dvd", "ConceptuallyRelatedTo", "tv")

os.getcwd() current working directory
os.getlogin() errors but doced to get logged in user.
os.listdir(path)
os.path.isdir("assertion_data")


# Create a blend from Samsung Common Consensus, blended with ConceptNet 4
d4d.normalize("Samsung_CC_Without_CN4", d4dcc.cc_to_assertions("assertion_data"), principal_component_count=10) 
d4dcc.write_svdview_files(d4d.Samsung_CC_Without_CN4.predict_matrix, d4d.Samsung_CC_Without_CN4.get_concepts(), "Samsung_CC")

d4d.blend("Samsung_CC", [d4d.c4, d4d.Samsung_CC_Without_CN4])

d4dcc.write_svdview_files(d4d.Samsung_CC) 
  #warning: takes a couple minutes, and sometimes does't work as too large. Quit python and start fresh if that happens.
"""