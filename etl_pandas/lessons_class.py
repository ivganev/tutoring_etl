import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class lessons():
    '''
    Class for the tutoring dataframe. Contains summary methods.
    '''

    def __init__(self, df: pd.DataFrame) -> None:
        ''' Check that the input dataframe has the appropriate columns.
        This list will grow as more methods are added.'''
        # assert 'start_timestamp' in df.columns
        # assert 'earned' in df.columns 
        # assert 'student_name' in df.columns
        # assert 'duration' in df.columns
        # assert 'pay_method' in df.columns
        assert {'start_timestamp', 'earned',
            'duration', 'level', 'pay_method',
            'student_name', 'subject'}.issubset(set(df.columns))
        self.df = df


    def set_net_earning(self, tax_rates: dict) -> None:
        '''Sets the net earning percentage for different payment methods'''
        
        # Dictionary for the net rates
        net_rates = {}

        # Set the net rate equal to one for methods not in the input dictionary
        for method in set(self.df['pay_method']):
            if method not in tax_rates:
                net_rates[method] = 1
            else:
                net_rates[method] = 1 - tax_rates[method]

        # Define the net earned column
        self.df['net_earned'] = (self.df['pay_method'].map(net_rates))*self.df['earned']
        self.df['net_earned'] = self.df['net_earned'].round(2)
        return
    
    def summary_student(self) -> pd.DataFrame:
        '''Summarizes the number lessons, hours tutored, and earnings per student'''

        # Filter by students
        student_df = self.df[['student_name', 'duration', "earned"]].groupby('student_name').sum().round(2)

        # Process the columns
        student_df['n_lessons'] = self.df['student_name'].value_counts()
        student_df['av_rate'] = (60*student_df['earned']/student_df['duration']).round(2)
        student_df['duration'] = (student_df['duration']/60).round(2)
        student_df = student_df.rename(columns={'duration' : 'hours'})
        student_df = student_df[['n_lessons', 'hours', 'earned', 'av_rate']]

        # Sort in decreasing order of number of lessons
        student_df = student_df.sort_values(by=['n_lessons','hours'], ascending=False)

        return student_df
    
    def summary_att(self, attribute: str) -> pd.DataFrame:
        '''Filters by an attribute and returns the number of lessons, number of students, 
        number of hours, earnings, and average rate, as well as the net earnings, and 
        net average rate, if available'''

        assert attribute in {'total', 'level', 'subject', 'pay_method', 'year', 'month', 'week', 'day'}, "Invalid attribute"

        # Add an extra column for totals if necessary
        if attribute == 'total':
            self.df['total'] = 1
            column = 'total'
            per = 'total'

        # Special procedure for time period summaries
        elif attribute in {'year', 'month', 'week', 'day'}:
            column = 'start_timestamp'
            pd.DatetimeIndex(self.df['start_timestamp']).to_period(attribute[0])
            per = self.df['start_timestamp'].dt.to_period(attribute[0])
        
        # Otherwise, just group by the attribute
        else:
            column = attribute
            per = attribute

        # Aggregating dictionary and columns
        agg_dict = {'earned': 'sum', 'duration': 'sum', 'student_name': 'nunique', column : 'count'}
        agg_columns = ['earned', 'duration', column, 'student_name']

        # Include a net earned column if it exists
        if 'net_earned' in self.df.columns:
            agg_dict['net_earned'] = 'sum'
            agg_columns.append('net_earned')

        # Aggregate and process the data
        g = self.df[agg_columns].groupby(per)
        att_df = g.agg(agg_dict)
        att_df['av_rate'] = (60*att_df['earned']/att_df['duration']).round(2)
        att_df['earned'] = att_df['earned'].round(2)
        att_df['hours'] = (att_df['duration']/60).round(2)
        att_df= att_df.rename(columns ={'student_name': 'n_students', column:'n_lessons'})

        # Output columns and extra column for average net rate
        out_columns = ['n_lessons', 'n_students', 'hours', 'earned', 'av_rate']
        if 'net_earned' in self.df.columns:
            att_df['av_net_rate'] = (60*att_df['net_earned']/att_df['duration']).round(2)
            out_columns += ['net_earned', 'av_net_rate']
        att_df = att_df[out_columns]

        # Remove the extra column, if necessary
        if column == 'total':
            self.df.drop(columns=['total'])
        
        # Sort the columns and return. Keep chronological order for datetime
        if column != 'start_timestamp':
            att_df = att_df.sort_values(by=['n_lessons','hours'], ascending=False)

        return att_df
    
    
    def summary_totals(self):
        '''Produce a grand total summary table'''
        totals_df = self.summary_att(attribute='total')
        return totals_df
        
    def summary_time_period(self, time_period):
        '''Produce a summary table for a time increment'''
        assert time_period in {'year', 'month', 'week', 'day'}
        period_df = self.summary_att(attribute=time_period)
        return period_df
    
    def summary_levels(self):
        '''Produce a summary table for the different levels'''
        level_df = self.summary_att('level')
        return level_df

    def summary_subjects(self):
        '''Produce a summary table for the different subjects'''
        subject_df = self.summary_att('subject')
        return subject_df
    
    def summary_pay_method(self):
         '''Produce a summary table for the different payment methods'''
         pay_df = self.summary_att('pay_method')
         return pay_df
    
    def export_summaries_to_csv(self, overwrite=True):
        '''Exports summary tables to csv files.
        Written to subdirectory of summaries directory for today's date.
        With overwrite=True, replaces any existing data for today's date'''
        
        # Make directory for today's date
        date_dir_name = datetime.datetime.today().strftime('%Y-%m-%d/')
        try:
            os.mkdir('summaries/' + date_dir_name)
        except FileExistsError:
            if not overwrite:
                print('Summary already exists for this date. Run again with overwrite=True to overwrite it.')
                return
            else:
                pass

        # Run the summary methods and export the dataframes
        yearly_summary = self.summary_time_period('year')
        yearly_summary.to_csv('summaries/' + date_dir_name + 'yearly_summary.csv')

        monthly_summary = self.summary_time_period('month')
        monthly_summary.to_csv('summaries/' + date_dir_name + 'monthly_summary.csv')

        weekly_summary = self.summary_time_period('week')
        weekly_summary.to_csv('summaries/' + date_dir_name + 'weekly_summary.csv')

        subject_summary = self.summary_subjects()
        subject_summary.to_csv('summaries/' + date_dir_name + 'subject_summary.csv')

        level_summary = self.summary_levels()
        level_summary.to_csv('summaries/' + date_dir_name + 'level_summary.csv')

        student_summary = self.summary_student()
        student_summary.to_csv('summaries/' + date_dir_name + 'student_summary.csv')

        pay_method_summary = self.summary_pay_method()
        pay_method_summary.to_csv('summaries/' + date_dir_name + 'pay_method_summary.csv')


    def make_summary_figures(self, overwrite=True, save=True):
        '''Exports summary figures to png files.
        Written to subdirectory of summaries directory for today's date.
        With overwrite=True, replaces any existing data for today's date'''

        if save:        
            date_dir_name = datetime.datetime.today().strftime('%Y-%m-%d/')
            try:
                os.mkdir('figs/' + date_dir_name)
            except FileExistsError:
                if not overwrite:
                    print('Figures already exist for this date. Run again with overwrite=True to overwrite it.')
                    return
                else:
                    pass

        subject_summary = self.summary_subjects().sort_values(by='hours', ascending=False)
        subject_summary['percent_hours'] = subject_summary['hours']/subject_summary['hours'].sum()
        keep_df = subject_summary[['hours', 'percent_hours']][subject_summary['percent_hours'] >= 0.01]
        other_df = subject_summary[['hours', 'percent_hours']][subject_summary['percent_hours'] < 0.01]
        other_row = pd.DataFrame(data = {
            'subject' : ['Other'],
            'hours' : [other_df['hours'].sum()]
        })
        other_row = other_row.set_index('subject')
        subject_summary_processed = pd.concat([keep_df['hours'], other_row['hours']])        
        colors = sns.color_palette('pastel')[0:12]
        plt.pie(
            subject_summary_processed, 
            labels = subject_summary_processed.index, 
            colors=colors, 
            autopct='%.0f%%', 
            radius =1)
        plt.title("Subjects by hours tutored")
        if save:
            plt.savefig("figs/" + date_dir_name + "hours-subjects.png")
        plt.show()
        plt.close()
    
        subject_n_students = subject_summary['n_students'].sort_values(ascending=False)
        plt.pie(
            subject_n_students, 
            labels = subject_n_students.index, 
            colors=colors, 
            autopct='%.0f%%', 
            radius =1)
        plt.title('Subjects by number of students')
        if save:
            plt.savefig("figs/" + date_dir_name + "students-subjects.png")
        plt.show()
        plt.close()

        level_summary = self.summary_levels()
        level_n_students = level_summary['n_students'].sort_values(ascending=False)
        plt.pie(
            level_n_students, 
            labels = level_n_students.index,
            colors=colors, 
            autopct='%.0f%%', 
            radius =1)
        plt.title('Levels by number of students')
        if save:
            plt.savefig("figs/" + date_dir_name + "students-level.png")
        plt.show()
        plt.close()




