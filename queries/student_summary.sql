\connect tutoring_db;

SELECT 
    student_name,
    count(lesson) as n_lessons, 
    sum(duration)/60 as hours, 
    round(cast(sum(effective_rate*duration/60) as numeric),2) as earned, 
    round(cast(avg ( effective_rate ) as numeric),0) as avg_rate
FROM lesson 
    INNER JOIN student 
        USING(studentid)
GROUP BY student_name
ORDER BY n_lessons DESC;