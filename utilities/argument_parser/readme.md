# module `utilities.argument_parser`

this module provides the class `ArgumentParser` which inherits from `argparse.ArgumentParser`, and its function `add_argument` is overrided. the usage of the function `add_argument` is same, but, the type and default value of the argument can be printed automatically.

for example:

	$ python3 scripts/train_word_vector.py -h
	usage: train_word_vector.py [-h] -d CORPUS_DIRECTORY -o OUTPUT [-t TITLE]
								[-f FLOW] [-u WORD_DICTIONARY] [-a ALGORITHM]
								[-l VECTOR_SIZE] [-r ALPHA] [-s SEED]
								[-w WINDOW_SIZE] [-c MINIMUM_COUNT]
								[-v MAXIMUM_VOCABULARY_SIZE] [-p SAMPLE]
								[-j WORKERS] [-x HIERARCHICAL_SOFTMAX]
								[-m CBOW_MEAN] [-i ITERATIONS] [-b BATCH_WORDS]
								[-k PLACEHOLDER]

	optional arguments:
	  -h, --help            show this help message and exit
	  -d CORPUS_DIRECTORY, --corpus_directory CORPUS_DIRECTORY
							specify the corpus directory
							# parameter type: <class 'str'>
	  -o OUTPUT, --output OUTPUT
							output of the word vector model
							# parameter type: <class 'str'>
	  -t TITLE, --title TITLE
							set the title of the log file
							# parameter type: <class 'str'>
							# default value: micro_service
	  -f FLOW, --flow FLOW  set the flow type of the log file
							# parameter type: <class 'str'>
							# default value: word_vector_training
	  -u WORD_DICTIONARY, --word_dictionary WORD_DICTIONARY
							specify the directory of the word splitter
							# parameter type: <class 'str'>
							# default value: None
	  -a ALGORITHM, --algorithm ALGORITHM
							training algorithm: skip-gram or cbow
							# parameter type: <class 'str'>
							# default value: cbow
	  -l VECTOR_SIZE, --vector_size VECTOR_SIZE
							dimensionality of the word vectors
							# parameter type: <class 'int'>
							# default value: 128
	  -r ALPHA, --alpha ALPHA
							the initial learning rate
							# parameter type: <class 'float'>
							# default value: 0.025
	  -s SEED, --seed SEED  seed for the random number generator, which is used to generate the
							initial value
							# parameter type: <class 'int'>
							# default value: 1
	  -w WINDOW_SIZE, --window_size WINDOW_SIZE
							maximum distance between the current and predicted word within a
							sentence
							# parameter type: <class 'int'>
							# default value: 5
	  -c MINIMUM_COUNT, --minimum_count MINIMUM_COUNT
							ignores all words with total frequency lower than this
							# parameter type: <class 'int'>
							# default value: 5
	  -v MAXIMUM_VOCABULARY_SIZE, --maximum_vocabulary_size MAXIMUM_VOCABULARY_SIZE
							limits the RAM during vocabulary building. if there are more unique
							words than this, then prune the infrequent ones. every 10 million word
							types need about 1GB of RAM. set to -1 for no limit
							# parameter type: <class 'int'>
							# default value: None
	  -p SAMPLE, --sample SAMPLE
							the threshold for configuring which higher-frequency words are
							randomly downsampled, useful range is (0, 1e-5)
							# parameter type: <class 'float'>
							# default value: 0.001
	  -j WORKERS, --workers WORKERS
							use these many worker threads to train the model
							# parameter type: <class 'int'>
							# default value: 4
	  -x HIERARCHICAL_SOFTMAX, --hierarchical_softmax HIERARCHICAL_SOFTMAX
							if True, hierarchical softmax will be used for model training.
							if False, and negative is non-zero, negative sampling will be used
							# parameter type: <class 'bool'>
							# default value: True
	  -m CBOW_MEAN, --cbow_mean CBOW_MEAN
							if 0, use the sum of the context word vectors.
							if 1, use the mean, only applies when cbow is used
							# parameter type: <class 'int'>
							# default value: 1
	  -i ITERATIONS, --iterations ITERATIONS
							number of iterations (epochs) over the corpus
							# parameter type: <class 'int'>
							# default value: 20
	  -b BATCH_WORDS, --batch_words BATCH_WORDS
							target size (in words) for batches of examples passed to worker
							threads (and thus cython routines). larger batches will be passed if
							individual texts are longer than 10,000 words, but the standard cython
							code truncates to that maximum
							# parameter type: <class 'int'>
							# default value: 10000
	  -k PLACEHOLDER, --placeholder PLACEHOLDER
							the placeholder for the unknown words
							# parameter type: <class 'str'>
							# default value: UNK
