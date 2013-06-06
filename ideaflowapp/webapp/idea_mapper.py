#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
Pitch-based scrolling - e.g. when you sing middle C, the document jumps to 50% mark. natural tool for voice recognition users/RSI/paralyzed patients

EEG-based Slumping Detector -- detect the pattern of brain activity that correlates with slumping / program that alerts me as is my posture begins to deteriorate so that I could correct it.. Could also just tells you to go to sleep. Helps people recover more quickly from RSI/carpal tunnel. Has interesting neuro/psych implications if it works as well. Would use Emotiv headset ~jcole@mit.edu

WorldThroughYourEyes -- What if you could make an app for Google Glasses or similar that follows a person's eyes and then and tracks where they are focusing. This way, you could  compare how different people focus differently, and analyze what that does to their lives. I also imagine that you could you could put on glasses yourself (or watch a screen), and then see the world through another person's eyes. ~jcole@mit.edu

InstaBoxSite: platform to build: generalized, easy to modify "suggestion box" framework anyone can use to quickly buildp a website off that mold.  All of following sites and countless more are based on fundamentally the same idea of a “comments box: isawyou stackoverflow forums reddit fml formspring ideaoverflow.tk / hackathonprojects.tk suggestion box/politicalprogressbar ifiwereanmitstudent.tk tumblr twitter facebook wall
In parallel, I am able to protoype many of the websites I build these days with what is basically a google doc. Why not build a google doc with slightly more functionality that truly allows me to prototype these tools? Check out http://mitdocs.tk/ to see the potential of this. Relatedly, way for people to make a homepage as easily as they can make a google doc -- consider http://adamchu.tk/, and http://minimalisthomepages.tk/  ~jcole@mit.edu
"""
#from d4d import d4d
#from conceptnet.models import Language
import inspect 
import mock_db 
import math
#Language.get('en')
'''
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def extract_concepts(idea):
	return d4d.en_nl.extract_concepts(idea)

def how_related_are(concept1, concept2):
	#print concept1, concept2
	try:
		return d4d.d4d.c4.how_related_are(concept1, concept2)
	except KeyError: # key does not exist
		return 0

"""def getRelatedIdeas(qidea):
	idea_entries=get_idea_entries()

	qconcept_list = extract_concepts(qidea)

	relatedness = []

	for i,idea_entry in enumerate(idea_entries):
		(id, idea, concept_list) = idea_entry
		relatedness.append((idea, how_related_are_concept_lists(qconcept_list, concept_list)))

	return sorted(relatedness, reverse=True)
"""

def getRelatedIdeas(qidea):
	idea_entries=get_idea_entries()

	qconcept_list = extract_concepts(qidea)

	relatedness = []

	for i,idea_entry in enumerate(idea_entries):
		(id, idea, concept_list) = idea_entry
		relatedness.append((idea, how_related_are_concept_lists(qconcept_list, concept_list)))

	return sorted(relatedness,key=lambda idea_entry:-idea_entry[1])[0:20]


def how_related_are_concept_lists(concept_list1, concept_list2):
	"""returns numerical relationship level 0 and up"""
	"""
	metrics
		sum([(10*max(how_related_are(c1, c2)-.7,0))**3
		sum([(10*max(how_related_are(c1, c2)-.6,0))**3
		sum([(10*max(how_related_are(c1, c2)-.5,0))**3
		
		sum([(10*max(how_related_are(c1, c2)-.6,0))**2
		sum([(10*max(how_related_are(c1, c2)-.5,0))**2

		Todo: machine learning, figure out what are good indicators

		Todo: transitive relations

	"""

	#return sum([3**(10*max(how_related_are(c1, c2)-.8,0)) for c1 in concept_list1 for c2 in concept_list2])

	#idea: try euclidean distance?
	
	#return max([how_related_are(c1, c2) for c1 in concept_list1 for c2 in concept_list2])

#	return sum(sorted(how_related_are(c1, c2) for c1 in concept_list1 for c2 in concept_list2)

	maxVs=[0,0,0,0,0]
	maxCs=[('',''),('',''),('',''),('',''),('','')]
	
	for c1 in concept_list1:
		for c2 in concept_list2:
			r=how_related_are(c1, c2)
			if r>maxVs[0]:
				maxVs.insert(0,r)
				maxCs.insert(0,(c1,c2))
				maxVs.pop()
				maxCs.pop()

	#print maxCs
	return sum(maxVs)
	

	"""
	for c1 in concept_list1:
		for c2 in concept_list2:
			r=how_related_are(c1, c2)
			if r>.95:
				return 1
	return 0
	"""



class MockDB:
	RAW_IDEAS = mock_db.RAW_IDEAS
	MOCK_IDEAS_TBL=[(id, idea,extract_concepts(idea)) for id, idea in enumerate(RAW_IDEAS)]


def get_idea_entries():
	return MockDB.MOCK_IDEAS_TBL

def printRelatedIdeas(qidea):
	for i,s in getRelatedIdeas(qidea):
		print i[0:60],s

if __name__ == '__main__':
	print 'start'
	#print getRelatedIdeas('eeg scrolling')
	printRelatedIdeas('eeg scrolling')










'''