# Jikan

An NLP Django webapp that suggests academic papers to read based on citation data.

## Paper Recommendation

The recommendation engine uses citation data to train a Neural Network with the fastai library. A paper can cite other papers and can be cited by others. The matrix consists of all the papers that are in the database. We use a collaborative filtering approach, which means that we look at the similarity between papers by the citation pattern (specifically, how they are cited by other papers) and find other papers that are most similar to these other papers.
