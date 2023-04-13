from parser import Token

class Tokenizer(object):
  #input: input file name
  #output: array of tokens
    def tokenize(self, input_file):
      file = f'input/{input_file}.txt'
      with open(file, 'r') as file:
        query = file.readline()
        
