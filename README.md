# Jikan

A web platform that allows user to upload their papers to seek comments and allow them to track paper progress. Also built in features such as similar papers recommendation, and other user engagement features. Django + Ajax + Bootstrap.

## Paper Recommendation

The algorithm uses the abstract of the paper to decide the next paper the reader should read. The algorithm first filters the set of papers to papers that belong to the same discipline. We consider 8 arbitrary disciplines and classify papers into them based on the name of the journals that they appear on.

After that, we conduct the standard preprocessing on the abstract (removing punctuation etc), and calculate the tf-idf and subsequently the cosine similarity of the abstract with the other papers in the same set.

### Data

References: https://aminer.org/citation

![num_paper](https://github.com/onyilam/jikan/blob/master/jikan/num_paper.png)
