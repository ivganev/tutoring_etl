# Tutoring Business

This is a repository with tools to process the data generated by an individual's tutoring business. Specifically, the code implements an ETL (extract transform load) procedure. Here are the steps for using this code:

## 1. Lesson data

Save the lesson data as a `csv` file: `data/lessons.csv`. The columns must include:

* `student` : the name of the student.
* `rate` : the rate of the lesson. This is the effective rate, after any third-party fees have been subtracted.
* `datetime` : the date and time of the lesson, formatted as `YYYY-MM-DD HH:MM`. 
* `length` : the duration of the lesson.
* `payment` : the payment method for the lesson.
* `level` : the level of the student, e.g. High School, College, Masters, PhD, etc.
* `subject` : the primary subject of the lesson.

Additionally, one may include estimates for the tax rates associated to various payment methods. This is done in a `csv` file: `data/payment.csv` with columns:

* `pay_method` : the name of the payment method.
* `tax_rate` : the estimated tax rate for each payment method. These rates can be used to calculate net earnings. 

The repository includes synthetic example data; one must replace the files in the `data` directory with one's own. 

## 2. Summary tables with pandas

Change the directory to `etl-pandas`. Running 

```python produce_summary.py``` 

creates a `summaries/` directory (if one does not already exist) and a subdirectory with today's date. The script exports `csv` files with several summaries:

* `yearly_summary.csv`: rows are the years appearing in the data and the columns giving the total number of lessons in the corresponding year, the total number of (distinct) students, the total number of hours tutored, the total earnings, and the average rate. If the `payment.csv` file is available, the net earnings and average net earning are also included.

* Similarly, we have `monthly_summary.csv` and `weekly_summary.csv`, which give summaries on a monthly and weekly basis. 

* `subject_summary.csv` and `level_summary.csv` give a similar breakdown as the yearly summary, but now rows are the various subjects and the various levels of the students, respectively. 

* `student_summary.csv`: rows are the students, and the columns giving the total number of lessons completed with that student, the total number of hours of lessons, the total earnings, and the average rate. 

Furthermore, the script `produce_summary.py` creates a `figs/` directory (if one does not already exist) and a subdirectory with today's date, where it exports several figures:

* `hours-subjects.png`: a pie plot of the subjects tutored based on the number of hours dedicated to each.

* `students-level.png`: a pie plot of the proportion of students in each level.

* `students-subjects.png`: a pie plot of the proportion of students in each subject.

In terms of the mechanics, the script imports the data from the `csv` file and converts it to a custom class called `lessons` (defined in `lessons_class.py`). 

## 3. ETL with PostgreSQL

Change to the `etl-postgres` directory. To create the database, run:

```psql -f make_db.sql```

One may get an error message about a connection to a server failing. In this case, see what is running at port 5432 with `sudo lsof -i :5432`. If port 5432 is already in use, to kill it use `sudo pkill -u postgres`. Then make sure PostgreSQL is running.

The file `script-etl.py` contains ETL methods for extracting, transforming, and loading the data from csv files to the PostgreSQL database. It requires the `data/` directory to contain the following files:

* `lessons.csv`. Same as discussed above. 
* `payment.csv`. Same as discussed above. 
* `student.csv`. A file with information about the students. Specifically, the columns are `students_name`, `account`, `timezone`, `rate`, `email`,`source`.

Once the csv files have been updated with the current information, and the database has been created, one can run the etl file:

```python script-etl.py```

This script relies on the package `pygrametl` ([link](https://chrthomsen.github.io/pygrametl/doc/index.html)). A number of queries are available in the `queries/` directory. One can run each individually via, e.g.,

```psql -f ../queries/monthly_summary.sql```

One can also run all of them at once with:

```bash run_queries.sh```

<!-- ## 4. Next steps (work in progress)

* Produce more of the relevant figures (pie plots, histograms, etc.) from the summary data frames. 

* Include methods for processing summaries of the topics in the lessons. E.g. make a word cloud of some sort. -->


