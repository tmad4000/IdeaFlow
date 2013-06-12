#!/usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse
from webapp.models import Idea, Suggestion
from django.core.serializers.json import DjangoJSONEncoder
import simplejson, datetime, re
#import imtesttest
import idea_mapper


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif '__json__' in dir(obj):
            return obj.__json__()
        else:
            return super(CustomJSONEncoder, self).default(obj)
      
# USE this to return a json response.
# Define the method __json__() in the models you're using.
# __json__() should returns a dict.

def to_json(d):
  return HttpResponse(simplejson.dumps(d, cls=CustomJSONEncoder), mimetype='application/json')



def idea(request, id):
	idea = Idea.objects.get(id=int(id))
	suggestions = idea.get_suggestions()
	
	ret = []
	
	for s in suggestions:
	    d = {}
	    d['suggestion'] = s
	    d['comments'] = s.get_comments()
	    ret.append(d)
	
 	return render(request, 'idea.html', {'idea': idea, 'suggestions': ret})

def home(request):
    '''import imtesttest 
    x=imtesttest.run()
    return HttpResponse(x)'''
    args = {
        'ideas': Idea.objects.all().order_by('-id'),
    }
    return render(request, 'main.html', args)
  
def upvote(request):
    if request.method == 'POST':
        if request.POST['type'] == 'idea':
            obj = Idea.objects.get(id=int(request.POST['id']))
        elif request.POST['type'] == 'suggestion':
            obj = Suggestion.objects.get(id=int(request.POST['id']))
        else: return
        
        obj.upvotes += 1
        obj.save()
        
        return to_json({ 'upvotes': obj.upvotes })
        
def addidea(request):
    if request.method == 'POST':
        idea = Idea()
        idea.title = request.POST['title']
        idea.text = request.POST['text']
        idea.tags = request.POST['tags']
        idea.save()
        
        return to_json(idea)
'''
def addideas_from_mockdb(request):
    if request.method == 'POST':
        idea = Idea()
        idea.title = request.POST['title']
        idea.text = request.POST['text']
        idea.tags = request.POST['tags']
        idea.save()
        
        return to_json(idea)
  '''

def addsuggestion(request):
    if request.method == 'POST':
        suggestion = Suggestion()
        suggestion.idea = Idea.objects.get(id=int(request.POST['idea']))
        suggestion.text = request.POST['text']
        suggestion.save()
        
        return to_json(suggestion)    

def getIdeaById(request):

    t='' 
    if 'id' in request.GET:
        t = request.GET['id']
        ideas = Idea.objects.filter(id=t)
    else:
        ideas = Idea.objects.filter(title=request.GET['title'])

    #todo: remove DUMMY IDEA
    if len(ideas)==0 :
        ideas=Idea.objects.filter(id=20)
#    t = request.GET['autocomplete']
    
    #t='5'
    
    idea=ideas[0]
#    rank_list = []
#    if len(ideas)>0:
#    rank_list.append(ideas[0])
#    rank_list.append(ideas[0])
    print ideas[0].title

#    return to_json([{'id':idea.id,'name':idea.title,'text':idea.text,'status':0,'tags':idea.tags,'upvotes':idea.upvotes} for rank, idea in rank_list])
    return to_json([{'id':idea.id,'name':idea.title,'text':idea.text,'status':0,'tags':idea.tags,'upvotes':idea.upvotes}])
    
        
'''def getIdeaById(request):

    def is_word_prefix(prefix, text):
        prefix = prefix.upper()
        text = text.upper()
        
        s = ''
        for c in text:
            if (ord(c) >= ord('A') and ord(c) <= ord('Z')) or (ord(c) >= ord('0') and ord(c) <= ord('9')) or c == '_':
                s += c
            else:
                if s.startswith(prefix): return True
                s = ''
        
        if s.startswith(prefix): return True
        else: return False
    
    t=''
    if('id' in request.POST):
        t = request.POST['relatedideas']
#    t = request.GET['autocomplete']
    words = t.split(' ')

#    targetid=(int)(t['id'])
    ideas = Idea.objects.filter(id=2)
    rank_list = []
    
    for idea in ideas:
        numw = 0
        rank = 0
        for word in words:
            if is_word_prefix(word, idea.text) or is_word_prefix(word, idea.title):
                numw += 1
                rank += 5 * int(is_word_prefix(word, idea.text)) + int(is_word_prefix(word, idea.title))
        
        if numw == len(words):
            rank_list.append((rank, idea))
                
    
    rank_list.sort()
    rank_list.reverse()
    ' id : val.id,
                        name : val.title,
                        status : 'some status',
                        coolness : val.text
                        ''
    return to_json([{'id':idea.id,'name':idea.title,'text':idea.text,'status':0,'tags':idea.tags,'upvotes':idea.upvotes} for rank, idea in rank_list[0:5]])
    
        
'''
        
def autocomplete(request):
    def is_word_prefix(prefix, text):
        prefix = prefix.upper()
        text = text.upper()
        
        s = ''
        for c in text:
            if (ord(c) >= ord('A') and ord(c) <= ord('Z')) or (ord(c) >= ord('0') and ord(c) <= ord('9')) or c == '_':
                s += c
            else:
                if s.startswith(prefix): return True
                s = ''
        
        if s.startswith(prefix): return True
        else: return False
    
    t=''
    if('query' in request.GET):
        t = request.GET['query']
#    t = request.GET['autocomplete']
    words = t.split(' ')
    ideas = Idea.objects.all()
    rank_list = []
    
    for idea in ideas:
        numw = 0
        rank = 0
        for word in words:
            if is_word_prefix(word, idea.text) or is_word_prefix(word, idea.title):
                numw += 1
                rank += 5 * int(is_word_prefix(word, idea.text)) + int(is_word_prefix(word, idea.title))
        
        if numw == len(words):
            rank_list.append((rank, idea))
                
    
    rank_list.sort()
    rank_list.reverse()
    ''' id : val.id,
                        name : val.title,
                        status : 'some status',
                        coolness : val.text
                        '''
#    return to_json([{'id':8,'name':'asdf','text':'a','status':0} for rank, idea in rank_list])
    #return(to_json(idea_mapper.getRelatedIdeas('cook')))

    #return to_json([{'id':idea.id,'name':idea.title,'text':idea.text} for rank, idea in rank_list])
    #return to_json([{'id':idea.id,'name':idea.title,'text':idea.text,'status':0} for rank, idea in rank_list])
    return to_json([{'id':idea.id,'name':idea.title,'text':idea.text,'status':0,'tags':idea.tags,'upvotes':idea.upvotes} for rank, idea in rank_list])
    
        
