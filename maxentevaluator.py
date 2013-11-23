

import cPickle as pickle
import os

from evaluator import Evaluator
from maxentclassifier import MaximumEntropyClassifier

class MaxEntEvaluator(Evaluator):

    def __init__(self, trainfile, testfile, maxent_args = {}, **kargs):
        Evaluator.__init__(self, trainfile, testfile, **kargs)
        # TODO add dictionary for arguments to pass to MaximumEntropyClassifier
        self.maxent_args = maxent_args

    def run(self):
        ent = MaximumEntropyClassifier(self.rawfname, **self.maxent_args)
        print 'Initialized classifier, about to train...'
        ent.trainClassifier()

        self.evaluate(ent)

    def runFromPickle(self, picklefile):
      f = open(picklefile, "rb")
      ent = pickle.load(f)
      f.close()

      print 'Loaded classifier from', picklefile

      self.evaluate(ent)

    def testAllPickles(self, pickledir='maxentpickles/'):
      pickle_files = os.listdir(pickledir)

      for pick in pickle_files:
        self.runFromPickle(pickledir + pick)

    def buildManyModels(self):
      '''

      '''
      all_filesubsets = [2000, 4000, 6000]

      all_min_occurences = [1, 3, 5]
      max_iter = 4
      all_grams = [[1], [1,2]]

      for filesubset in all_filesubsets:
        for min_occurence in all_min_occurences:
          for grams in all_grams:
            self.maxent_args = {
              'filesubset' : filesubset,
              'min_occurences' : min_occurence,
              'max_iter' : max_iter,
              'grams' : grams
            }
            ent = MaximumEntropyClassifier(self.rawfname, **self.maxent_args)
            print 'About to train with', self.maxent_args
            ent.trainClassifier()
            self.evaluate(ent)



def main():
    trainfile = "trainingandtestdata/training.csv"
    testfile = "trainingandtestdata/testing.csv"

    maxent_args = {
      'filesubset' : 3000,
      'min_occurences' : 3,
      'max_iter' : 4,
      'grams' : [1]
    }
    maxent_evaluator = MaxEntEvaluator(trainfile, 
                                       testfile,
                                       maxent_args,
                                       stdout = True
                                       )
    maxent_evaluator.buildManyModels()
    #maxent_evaluator.run()
    #maxent_evaluator.runFromPickle('maxentpickles/maxent_100_1_2.dat')
    #maxent_evaluator.testAllPickles()

if __name__ == '__main__':
  main()