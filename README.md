# Jikan

An NLP Django webapp that suggests academic papers to read based on citation data.

## Paper Recommendation

The recommendation engine uses citation data to train a Neural Network with the fastai library. A paper can cite other papers and can be cited by others. The matrix consists of all the papers that are in the database.
