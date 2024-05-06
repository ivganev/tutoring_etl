import psycopg2
import pygrametl
import pandas as pd
from transform import process_rating, process_timestamp

from pygrametl.datasources import CSVSource
from pygrametl.tables import CachedDimension, FactTable

if __name__ == "__main__":
    # Set path to the data
    data_path = "../data/"

    # Connection to the data warehouse (get data from the file `business.sql`)
    dw_string = "host='localhost' dbname='tutoring_db' user='tutor' password='tutorpass'"
    dw_conn = psycopg2.connect(dw_string)
    dw_conn_wrapper = pygrametl.ConnectionWrapper(connection=dw_conn)

    # Define the dimension tables and the fact table
    lesson_fact_table = FactTable(
        name = 'lesson',
        keyrefs=['studentid', 'timeid'],
        measures = ['duration', 'effective_rate', 'paymethodid', 'rating', 'subjectid']
    )

    student_dimension = CachedDimension(
        name='student',
        key='studentid',
        attributes=['student_name', 'level', 'timezone', 'account', 'source', 'email'],
        lookupatts=['student_name']
    )

    time_dimension = CachedDimension(
        name='time',
        key='timeid',
        attributes=['start_timestamp', 'day', 'month', 'week', 'year']
    )

    subject_dimension = CachedDimension(
        name='subject',
        key='subjectid',
        attributes=['subject'],
        lookupatts=['subject']
    )

    payment_dimension = CachedDimension(
        name='pay_method',
        key='paymethodid',
        attributes=['pay_method', 'tax_rate'],
        lookupatts=['pay_method']
    )

    # Add information about students
    student_file_handle = open(data_path + 'student.csv', 'r', 16384, "utf-8")
    student_source = CSVSource(f=student_file_handle, delimiter=',')
    [student_dimension.ensure(row) for row in student_source]

    # Add information about payment methods
    paymethod_file_handle = open(data_path + 'payment.csv', 'r', 16384, "utf-8")
    paymethod_source = CSVSource(f=paymethod_file_handle, delimiter=',')
    [payment_dimension.ensure(row) for row in paymethod_source]

    # Read the data from the lessons csv file and add it to the appropriate tables
    lesson_file_handle = open(data_path + 'lessons.csv', 'r', 16384, "utf-8")
    lesson_source = CSVSource(f=lesson_file_handle, delimiter=",")
    for row in lesson_source:
        process_timestamp(row)
        process_rating(row)
        row['studentid'] = student_dimension.lookup(row)
        row['timeid'] = time_dimension.ensure(row)
        row['paymethodid'] = payment_dimension.ensure(row)
        row['subjectid'] = subject_dimension.ensure(row)
        lesson_fact_table.ensure(row)

    # Commit and close
    dw_conn_wrapper.commit()
    dw_conn_wrapper.close()