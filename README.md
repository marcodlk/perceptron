# -- perceptron -- 
Perceptron algorithm module

#### Setup
```
# clone
git clone https://github.com/marcodlk/perceptron

cd perceptron/
# see options
python perceptron.py -h
```

#### Usage examples
```
# use randomly generated dataset size 10
# set learning rate parameter to 0.01
# set max iterations to 500
# generate animated plot from results
python perceptron.py -r 10 -c 0.01 -i 1000 -a plot.mp4

# use preset AND binary op data
#  + available binops: and,or,xor,nand
# default parameters are used if not specified
python perceptron.py -0 and
```

