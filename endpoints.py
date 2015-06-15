#!/usr/bin/python
from __future__ import division
import web, re, json, numpy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist  


urls = (
	
	'/words/findphones/(.*)', 'find_phones',
	'/words/avgwordlen/(.*)', 'find_word_len',
	'/sentences/avglen/(.*)', 'find_sent_len',
	'/words/mostfreqi/(.*)', 'find_most_freq',
	'/words/findmedian/(.*)', 'find_median_word'
)

app = web.application(urls, globals())

class find_median_word:
	def GET(self, jsoninput):
		mediandict = {}
		wordlist= word_tokenize(get_input(jsoninput))
		for w in wordlist:
			mediandict[w] = len(w)
		median = numpy.median(numpy.array(mediandict.values()))
		
		key =  [k for k, v in mediandict.iteritems() if v == median][0]
		return jsonify('mediankey', key)
	

class find_most_freq:
	def GET(self, jsoninput):
		wordlist = word_tokenize(jsoninput)
		wordlist = filter(lambda a: a != '.' and a != ','  and a != '?' and a !='!', wordlist)
		fd = FreqDist(wordlist)
		mostcom = fd.most_common(10)
		return jsonify('mostfreq', mostcom)
		

class find_sent_len:
	def GET(self, jsoninput):
		sents=sent_tokenize(jsoninput)
		avglen= sum(len(sent) for sent in sents) /len(sents)
		return jsonify('avgsentlen', avglen) 
		
		

class find_phones:
	def GET(self, inputjson):
			
		regex =(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
		phones = re.findall(regex, get_input(inputjson))
		return jsonify('phones', phones)
	
		

class find_word_len:
	def GET(self, jsoninput):
		words = word_tokenize(jsoninput)
		avglen=sum(len(word) for word in words) /len(words)
			
		return jsonify('avgwordlen', avglen)

def jsonify(dictname, values):
	retdict = {dictname:values}
	return json.dumps(retdict)

def get_input(jsoninput):
	textinput = json.loads(jsoninput)
	return textinput['text'] 
	

if __name__ == "__main__":
    app.run()
