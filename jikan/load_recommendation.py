import sys, os
import pandas as pd
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jikan.settings")
import django
django.setup()
from ast import literal_eval
from search.models import Paper, Journal, Author


def load_recommendation(paper_row):
    paper, _ = Paper.objects.get_or_create(aminer_id=paper_row['id'])
    rankings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    for rank in rankings:
        similar_paper, _ = Paper.objects.get_or_create(aminer_id=paper_row[rank])
        paper.recommend.add(similar_paper)
        paper.save()

# the main function for the script, called by the shell
if __name__ == "__main__":

    # Check number of arguments (including the command name)
    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        papers_df = pd.read_csv(sys.argv[1])

        # apply save_review_from_row to each review in the data frame
        papers_df.apply(
            load_recommendation,
            axis=1
        )

        print("There are {} papers in DB".format(Paper.objects.count()))

    else:
        print("Please, provide papers file path")

