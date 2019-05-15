# Jikan

A NLP Django webapp that suggests academic papers to read based on citation data.

## Paper Recommendation

The recommendation engine uses citation data to decide the next paper the reader should read. A paper can cite other papers and can be cited by others. We use a collaborative filtering approach, which means that we look at the similarity between papers by the citation pattern (specifically, how they are cited by other papers) and find other papers that are most similar to these other papers.

### Data

References: https://aminer.org/citation

[[https://github.com/onyilam/jikan/blob/master/num_paper.png|alt=num_paper]]
