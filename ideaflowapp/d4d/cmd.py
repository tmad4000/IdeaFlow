"""
Documentation: "cmd" is the name of an add-on to d4d.
               It facilitat4es reasoning about natural language commands
               by parsing them into scored data structures containing an 'action'
               and an 'arg' to that action, with scores as to their likelyhood.
               
               The highest level things to pay attention to are:
               Creating an instance of cmd
               Method: sentence_to_cmd
               Method: prioritize_sentences
              
               All are documented below.
               
Release Notes:
  Jan 25, 2013
             Added more doc.
             Added method: prioritize_sentences
             Added methods pretty_print_cmd, pretty_print_cmds
             Added 'threshold' arguments
             Made cmd instances that hold an instance of d4d along with the 'actions' and threshold
"""
import logging
#Low level language tools
from conceptnet.models import Language
en = Language.get('en')
en_nl = en.nl

import os, sys
sys.path.append(os.path.abspath("../"))
from d4d import d4d

class cmd:
  """An instance of the 'cmd' class has the properties:
     name:  A string. After its made, the instance can be accessed via cmd.name_of_instance.
            For example: d4d.c4  is the "default" instance that is automatically 
            created when you load 'cmd'. It uses d4d.c4 (Conceptnet4) for its d4d instance.
     d4di:  The instance of d4d used by this instance, or "any_format_assertions" accepted
             by d4d. In this case, an instance of d4d is made with the above 'name',
             and the provided assertions. If you want to use the other arguments to making
             an instance of d4d, create the instance of d4d normally and use it for
             this argument.
     actions: The dict of actions. For each element of the dict, the key is the command name,
              and the value is a list of possible args. Neither the args nor the actions
              should have synonyms in them. the d4di is used to find the mapping
              of an input 'synonym' to its canonical command or arg name,
              specficifed by 'actions'.
     threshold: A float between 1 and 0. sentences that recieve a score below this threshold
                are filtered out. Methods that take a threshold argument have a default value
                of None, meaning that the threshold is derived from this value of 'threshold',
                ie the value in 'self'.
    EXAMPLES:
    cmd(name="c4", 
        d4di=d4d.c4,
        actions={"watch":    ["tv", "dvd", "movie", "comedy", "sports", "house", "pride and prejudice"],
                  "channel": ["weather", "espn", "nbc", "sports"],
                  "volume":  ["loud", "soft", "up", "down"]
                },
        threshold=1)
    cmd.c4.sentence_to_cmd("I want to see football")
    cmd(name="cmd1", 
        d4di='''Football is a sport
                tv used for football
                tv used for watch
              ''',          
        actions={"watch":  ["tv", "dvd", "movie", "comedy", "sports", "house", "pride and prejudice"],
                 "channel":["weather", "espn", "nbc", "sports"],
                 "volume": ["loud", "soft", "up", "down"]
                },
        threshold=1)
    cmd.cmd1.sentence_to_cmd("I want to watch football")
        
        You may call all the d4d methods using an instance of cmd, 
        where below, 'c4' is the name of your cmd instance. Example:
        cmd.c4.d4di.how_true_is("dog is a pet")      
  """
  d4di=None
  actions=None
  concept_actions=None #a filtered set from actions in which all terms normalized and IN d4di.
                       #we must do this because how_similar_are breaks if passed a concept
                       #that is not in the matrix
  threshold=1
  
  def __init__(self, name, d4di, actions, threshold=1):
    setattr(self.__class__, name, self)
    self.name    = name
    self.d4di    = d4di
    self.actions = actions
    threshold    = threshold
    if not(isinstance(self.actions, d4d)):
       d4d(name=name, any_format_assertions=d4di)
       self.d4di = getattr(d4d, name)
    #below inits concept_actions, which is a dict that is a normalized version of actions, with concepts not in d4di filterned out.
    self.concept_actions = {}
    for action in self.actions:
      if self.d4di.is_concept(action):
        result_args = []
        for arg in self.actions[action]:
          if not(arg in ["dvd"]): #don't normalize words in this exception list because it screws up. ie dvd normalizes to "d"
            arg = d4d.normalize_concept(arg)
          if self.d4di.is_concept(arg):
            result_args.append(arg)
        if len(result_args) > 0:
          self.concept_actions[action] = result_args
  
  @classmethod        
  def init(clz):
    clz("c4", 
        d4d.c4,
        {"watch":  ["tv", "dvd", "movie", "comedy", "sports", "house", "pride and prejudice"],
                   "channel":["weather", "espn", "nbc", "sports"],
                   "volume": ["loud", "soft", "up", "down"]
        },
        threshold=1
       )    
                    
  def sentence_to_cmd(self, sentence, threshold=None):
    """Always returns a "cmd_dict".
       When full, a cmd_dict has the field of the orignal sentence, the action found in it,
       the arg to the action in the sentence, and scores for the action and arg.
       When 'empty' the 'action' will have a value of None.
       If threshold is passed in, it over-rides self.threshold.
    Examples:
    cmd.c4.sentence_to_cmd("I want to watch a movie") #=>{'action': 'watch', 'arg': 'movie'}
    cmd.c4.sentence_to_cmd("I want to see a movie") 
    cmd.c4.sentence_to_cmd("I want to see football")
    cmd.c4.sentence_to_cmd("baseball")
    cmd.c4.sentence_to_cmd("is basketball on")
    cmd.c4.sentence_to_cmd("make the volume louder")
    cmd.c4.sentence_to_cmd("make the volume less")
    cmd.c4.sentence_to_cmd("the sound isn't loud enough")
    cmd.c4.sentence_to_cmd("show me something good")
    """
    if threshold == None:
      threshold = self.threshold
    cmd_dict = {"sentence":sentence}
    cmd_dict = self.sentence_to_action(sentence, cmd_dict, float(threshold)/2)
    if not(cmd_dict["action"]):
      return cmd_dict
    cmd_dict    = self.sentence_to_arg(sentence, cmd_dict, float(threshold)/2)
    if self.cmd_filled(cmd_dict) and self.cmd_score(cmd_dict) >= threshold:
        return cmd_dict
    else:
      cmd_dict["action"] = None
      return cmd_dict
  
  def sentence_to_action(self, sentence, cmd_dict, threshold=None):
    """ If threshold is passed in, it over-rides the default of self.threshold / 2.
    """
    if threshold == None:
      threshold = float(self.threshold ) / 2   
    result_action = None
    for action in self.actions:
      if action in sentence:
        result_action = action
        break
    if result_action:
      cmd_dict["action"] = result_action
      cmd_dict["action_score"] = 1      
      return cmd_dict
    else:
      concepts = self.sentence_to_concepts(sentence)
      if not(concepts):
        result_action = None
        result_score  = 0
        return result_score
      result_score = 0
      for action in self.concept_actions:
        for concept in concepts:
          score = self.d4di.how_similar_are(action, concept)
          if score > result_score:
            result_action = action
            result_score = score
      if result_score >= threshold:
        cmd_dict["action"] = result_action
        cmd_dict["action_score"] = result_score
      else:
        cmd_dict["action"] = None
      return cmd_dict
      
  
  def sentence_to_arg(self, sentence, cmd_dict, threshold=None):
      """ If threshold is passed in, it over-rides the default of self.threshold / 2.
      """      
      if threshold == None:
        threshold = float(self.threshold ) / 2        
      result_arg = None
      action = cmd_dict["action"]
      args = self.actions[action] #dont' use concept-actions here but do use it below
      for arg in args:
        if arg in sentence:
          result_arg = arg
          break
      if result_arg:
        cmd_dict["arg"] = result_arg
        cmd_dict["arg_score"] = 1        
        return cmd_dict 
      else:
        concepts = self.sentence_to_concepts(sentence)
        if not(concepts):
          cmd_dict["arg"] = None
          cmd_dict["arg_score"] = 0       
          return cmd_dict 
        result_arg = None
        result_score = 0
        args = self.concept_actions[action] #not the same as setting args above on purpose, as above,
                                            #we bypass normalization and in-d4di as criteria.
        for arg in args:
          for concept in concepts:
            score = self.d4di.how_similar_are(arg, concept)
            if score > result_score:
              result_arg = arg
              result_score = score
        if result_score >= threshold:
                cmd_dict["arg"] = result_arg
                cmd_dict["arg_score"] = result_score
        else:
           cmd_dict["arg"] = None        
           cmd_dict["arg_score"] = 0
        return cmd_dict       
        
  
  def sentence_to_concepts(self, sentence):
    """
    cmd.c4.sentence_to_concepts("I want to see a movie")
    """
    concepts = en_nl.extract_concepts(sentence, max_words=2, check_conceptnet=False)
      #as far as I can tell, check_conceptnet=True does nothing and
      #if I try to use how_similar_are on a string that isn't in d4di, I lose.
    result = []
    for concept in concepts:
      if self.d4di.is_concept(concept):
        result.append(concept)
    return result
  
  def cmd_score(self, cmd_dict):
    return cmd_dict["action_score"] + cmd_dict["arg_score"]
  
  def cmd_filled(self, cmd_dict):
      return cmd_dict["action"] and cmd_dict["arg"] 
  
  def prioritize_sentences(self, sentences, threshold=1):
    """ Returns a list of cmd dicts sorted by highest_scored dict first.
        cmd_dicts that have a score of less than 'treshold' are not in the returned list.
    
        cmd.c4.pretty_print_cmds(cmd.c4.prioritize_sentences(["I want to see foot", 
                                                              "I want to see football", 
                                                              "I want to see foosball"]))
    """
    cmd_dicts = []
    for sentence in sentences:
      cmd_dict = self.sentence_to_cmd(sentence, threshold)
      if self.cmd_filled(cmd_dict):
        cmd_dicts.append(cmd_dict)
    cmd_dicts.sort(key=lambda cmd_dict: 1000 - self.cmd_score(cmd_dict)) #use 1000 - score so that the higher score returns the lower number and thus will be sorted first
    return cmd_dicts
  
  def pretty_print_cmd(self, cmd):
    """
    cmd.c4.pretty_print_cmd(cmd.c4.sentence_to_cmd("I want to see football"))
    """
    return '"' + cmd["sentence"] + '" ' + cmd["action"] + "->" + cmd["arg"] + " " + \
           str(cmd["action_score"])[0:3] + " + " + str(cmd["arg_score"])[0:3] + " = " + \
           str(self.cmd_score(cmd))[0:3]
  
  def pretty_print_cmds(self, cmds):
    for cmd in cmds:
      print(self.pretty_print_cmd(cmd))

cmd.init()

# cmd.c4.prioritize_sentences(["I want to see football", "I want to see foosball"])
print("cmd loaded")
