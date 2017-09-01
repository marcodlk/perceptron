# -- perceptron -- 
Perceptron algorithm module

#### Setup
```
# required modules
pip3 install matplotlib numpy optparse

# clone
git clone https://github.com/marcodlk/perceptron.git

cd perceptron/
# see options
python3 perceptron.py -h
```

#### Usage examples
```
# use randomly generated dataset size 10
# set learning rate parameter to 0.01
# set max iterations to 500
# generate animated plot from results
python3 perceptron.py -r 10 -c 0.01 -i 500 -a plot.mp4

# use preset AND binary op data
#  + available binops: and,or,xor,nand
# default parameters are used if not specified
python3 perceptron.py -0 and
```

