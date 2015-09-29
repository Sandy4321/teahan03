# corpusdir - name of subdir with corpus
# META_FNAME - name of the meta-file.json
# OUT_FNAME - file to write the output in (out.json)
# upath - path of the 'unknown' dir in the corpus (from json)
# candidates - list of candidate author names (from json)
# unknowns - list of unknown filenames (from json)
# trainings - dictionary with lists of filenames of trainingtexts for each author
# 	{"candidate2":["file1.txt", "file2.txt", ...], "candidate2":["file1.txt", ...] ...}

# Usage:
# loadJson(corpusname), with corpusname from commandline
# OPTIONAL: loadTraining()
# OPTIONAL: getTrainingText(jsonhandler.candidate[i], jsonhandler.trainings[jsonhandler.candidates[i]][j]), gets trainingtext j from candidate i as a string
# getUnknownText(jsonhandler.unknowns[i]), gets unknown text i as a string
# storeJson(candidates, texts, scores), with list of candidates as candidates (jsonhandler.candidates can be used), list of texts as texts and list of scores as scores, last argument can be ommitted

'''
EXAMPLE:

import jsonhandler

candidates = jsonhandler.candidates
unknowns = jsonhandler.unknowns
jsonhandler.loadJson("testcorpus")

# If you want to do training:
jsonhandler.loadTraining()
for cand in candidates:
	for file in jsonhandler.trainings[cand]:
		# Get content of training file 'file' of candidate 'cand' as a string with:
		# jsonhandler.getTrainingText(cand, file)

# Create lists for your answers (and scores)
authors = []
scores = []

for file in unknowns:
	# Get content of unknown file 'file' as a string with:
	# jsonhandler.getUnknownText(file)
	# Determine author of the file, and score (optional)
	author = "oneAuthor"
	score = 0.5
	authors.append(author)
	scores.append(score)

# Save results to json-file out.json (passing 'scores' is optional)
jsonhandler.storeJson(unknowns, authors, scores)
'''

import os, json

META_FNAME = "meta-file.json"
OUT_FNAME = "out.json"

def loadJson(corpus):
	global corpusdir, upath, candidates, unknowns
	corpusdir += corpus
	mfile = open(os.path.join(corpusdir, META_FNAME), "r")
	metajson = json.load(mfile)
	mfile.close()

	upath += os.path.join(corpusdir, metajson["folder"])
	candidates += [author["author-name"] for author in metajson["candidate-authors"]]
	unknowns += [text["unknown-text"] for text in metajson["unknown-texts"]]

def getUnknownText(fname):
	dfile = open(os.path.join(upath, fname))
	s = dfile.read()
	dfile.close()
	return s

def loadTraining():
	for cand in candidates:
		trainings[cand] = []
		for subdir, dirs, files in os.walk(os.path.join(corpusdir, cand)):
			for doc in files:
				trainings[cand].append(doc)

def getTrainingText(cand, fname):
	dfile = open(os.path.join(corpusdir, cand, fname))
	s = dfile.read()
	dfile.close()
	return s

def storeJson(texts, cands, scores = None):
	answers = []
	if scores == None:
		scores = [1 for text in texts]
	for i in range(len(texts)):
		answers.append({"unknown_text": texts[i], "author": cands[i], "score": scores[i]})
	f = open(os.path.join(corpusdir, OUT_FNAME), "w")
	json.dump({"answers": answers}, f, indent=2)
	f.close()

corpusdir = ""
upath = ""
candidates = []
unknowns = []
trainings = {}
