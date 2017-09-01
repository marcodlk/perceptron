'''
@author: Marco de Lannoy Kobayashi
'''

from optparse import OptionParser
from datagen import generate_random_linear_separable
from plotanimation import animate

#-- OPTIONS --------------------------------------------------------------------
def _parse_opts():
    parser = OptionParser()
    parser.add_option('-d','--datafile',dest='datafile',
                      help='get data from file',
                      metavar='FILE')
    parser.add_option('-l','--logfile',dest='logfile',
                      help='log weights and bias updates to file',
                      metavar='FILE')
    parser.add_option('-c','--learning_rate',dest='learn_rate',
                      help='set learning rate parameter [default = 0.1]',
                      metavar='<float>',
                      default=0.1)
    parser.add_option('-i','--maximum_iterations',dest='max_iters',
                      help='set max iterations [default = 1000]',
                      metavar='<integer>',
                      default=1000)
    parser.add_option('-r','--random_data',dest='randomset',
                      help='use randomly generated data with size X',
                      metavar='X')
    parser.add_option('-0','--binop',dest='operation',
                      help='use binary operation dataset [default = AND]',
                      default='AND')
    parser.add_option('-a','--animation',dest='animation',
                      help='generate animated plot of perceptron converging',
                      metavar='FILE')

    return parser.parse_args()

#-- CLASSES --------------------------------------------------------------------
''' single layer perceptron '''
class SLP:
    def __init__(self,train_set,lrp=0.1,mi=1000,name='perc'):
        self.name = name
        self.__max_iters = mi
        self.__learn_rate = lrp 
        self.__samples = [[col for col in row[:-1]] for row in train_set]
        self.__labels = [row[-1] for row in train_set]

        self.__weights = [0.0 for col in range(len(self.__samples[0]))]
        self.__bias = 0.0
        self.logs = []

    def __predict(self,sample):
        activation = self.__bias + sum(weight*feat
                                  for weight,feat in zip(self.__weights,sample))
        return 1 if (activation > 0.0) else -1

    def train(self):
        for i in range(self.__max_iters):
            updated = False
            for sample,label in zip(self.__samples,self.__labels):
                prediction = self.__predict(sample)
                if (label*prediction) > 0.0:
                    continue
                    
                error = label - prediction
                self.__bias += self.__learn_rate * error
                self.__weights = [weight + self.__learn_rate*error*feat
                                  for weight,feat in zip(self.__weights,sample)]
                updated = True
                log = [self.__bias]
                log.extend([weight for weight in self.__weights])
                self.logs.append(log)
                
            if not updated: 
                return i,self.__bias,self.__weights

        return None,None,None 

    def update_training_set(self,train_set):
        self.__samples = [[col for col in row[:-1]] for row in train_set]
        self.__labels = [row[-1] for row in train_set]

    def reset(self):
        self.__weights = [0.0 for col in range(len(__samples[0]))]
        self.__bias = 0.0
        self.__logger = []

    def logs(self):
        return self.__logger

''' multi layer perceptron '''
class MLP: #TODO
    def __init__(self,dataset,name='P'):
        self.__name = name
        self.__data = dataset

    

#-- HELPER FUNCTIONS -----------------------------------------------------------
def _collect(filename):
    print('-- Collecting data from %s' % filename)
    collected = []
    with open(filename) as datafile:
        data = datafile.read().strip().split('\n')
        collected = [[float(col) for col in row.strip().split(',')] 
                                 for row in data]

    return collected

def _dump(logs,filename):
    print('-- Dumping data to %s' % filename)
    with open(filename,'w') as outfile:
        for log in logs:
            outfile.write(str(log[0]) + ",")
            outfile.write(str(log[1]) + ",")
            outfile.write(str(log[2]) + "\n")

    return

#-- MAIN -----------------------------------------------------------------------
def _main():
    # parse options and arguments
    opts,args = _parse_opts()

    # max iterations, in case solution is unfeasible
    max_iters = int(opts.max_iters)
    assert max_iters > 0

    # preset datasets, binary operations
    AND  = [[0,0,-1], [1,0,-1], [0,1,-1], [1,1, 1]]
    NAND = [[0,0, 1], [1,0, 1], [0,1, 1], [1,1,-1]]
    OR   = [[0,0,-1], [1,0, 1], [0,1, 1], [1,1, 1]]
    XOR  = [[0,0,-1], [1,0, 1], [0,1, 1], [1,1,-1]]

    d = dict()
    d.update( {'AND':AND,'NAND':NAND,'OR':OR,'XOR':XOR} )
    dataset = d[opts.operation.upper()]

    # data input
    if opts.datafile:
        dataset = _collect(opts.datafile)
    elif opts.randomset:
        dataset = generate_random_linear_separable(int(opts.randomset))
        _dump(dataset,'random.csv')

    # learning rate parameter
    learn_rate = float(opts.learn_rate)
    assert learn_rate < 1. and learn_rate > 0.

    # setup
    perceptron = SLP(dataset,name='and',lrp=learn_rate,mi=max_iters)

    # train
    print('-- Running perceptron algorithm')
    iters,bias,weights = perceptron.train()

    # results
    if (iters,bias,weights) == (None,None,None):
        print('-- [!!!] Unable to converge within %d iterations' % max_iters)
    else:
        print( '-- Success')
        print( '+%s' % ('='*79) )
        print(('| Weight function = %f + (%f * x0) + (%f * x1)') 
                                                            % (bias, weights[0], weights[1]))
        print( '| Converged in %d iterations' % (iters-1))
        print( '+%s' % ('='*79) )
        if opts.animation:
            print('-- Generating %s' % opts.animation)
            animate(perceptron.logs,dataset,opts.animation)

    if opts.logfile:
        _dump(perceptron.logs,opts.logfile)

if __name__ == '__main__':
    _main()
    print('-- Done')
