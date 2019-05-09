import sys, os
import pandas as pd
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jikan.settings")
import django
django.setup()
from ast import literal_eval
from search.models import Paper, Journal, Author


def save_paper_from_row(paper_row):
    paper = Paper()
    paper.aminer_id = paper_row['id']
    paper.title = paper_row['title']
    paper.abstract = paper_row['abstract']
    journal, _ = Journal.objects.get_or_create(name=paper_row['venue'])
    paper.journal = journal
    paper.year = paper_row['year']
    paper.n_citation = paper_row['n_citation']
    paper.references = paper_row['references']
    paper.save()

    for author in literal_eval(paper_row['authors']):
        fname = author.split(" ")[0]
        lname = author.split(" ")[-1]
        author, _ = Author.objects.get_or_create(first_name=fname, last_name=lname)
        paper.authors.add(author)

    paper.save()


# the main function for the script, called by the shell
if __name__ == "__main__":

    # Check number of arguments (including the command name)
    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        papers_df = pd.read_csv(sys.argv[1])

        # apply save_review_from_row to each review in the data frame
        papers_df.apply(
            save_paper_from_row,
            axis=1
        )

        print("There are {} papers in DB".format(Paper.objects.count()))

    else:
        print("Please, provide papers file path")

