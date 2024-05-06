\connect tutoring_db;

SELECT 
    level,
    count(lesson) as n_lessons, 
    count(distinct studentid) as n_students,
    sum(duration)/60 as hours, 
    round(cast(sum(effective_rate*duration) as numeric)/60,2) as earned, 
    round(cast(avg ( effective_rate ) as numeric),0) as avg_rate
FROM lesson 
    INNER JOIN student 
        USING(studentid)
GROUP BY level
ORDER BY n_lessons DESC;