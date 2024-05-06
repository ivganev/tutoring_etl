import pandas as pd
from lessons_class import lessons
import os


if __name__ == "__main__":
    # Set path to the data
    data_path = "../data/"

    # import lessons csv file as a pandas dataframe
    lessons_df = pd.read_csv(data_path + "lessons.csv")

    # preprocessing
    lessons_df['start_timestamp'] = pd.to_datetime(lessons_df['start_timestamp'])
    lessons_df['earned'] = lessons_df['effective_rate']*lessons_df['duration']/60

    # convert the dataframe to a lessons object
    my_lessons = lessons(lessons_df)

    # add tax rates
    tax_file_path = data_path + "payment.csv"
    if os.path.isfile(tax_file_path):
        tax_rate_df = pd.read_csv(tax_file_path, index_col='pay_method')
        tax_rate_dict = tax_rate_df.to_dict()['tax_rate']
        my_lessons.set_net_earning(tax_rate_dict)

    # make a directory for the summaries
    try:
        os.mkdir('summaries')
    except FileExistsError:
        pass

    # make a directory for the figures
    try:
        os.mkdir('figs')
    except FileExistsError:
        pass

    # make summary tables and export as csv files
    # written to subdirectory of summaries directory for today's date
    my_lessons.export_summaries_to_csv()

    # make summary figures and export as png files
    # written to subdirectory of figures directory for today's date
    my_lessons.make_summary_figures()

    