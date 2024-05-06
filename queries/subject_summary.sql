\connect tutoring_db;

SELECT 
    subject,
    count(lesson) as n_lessons, 
    count(distinct studentid) as n_students,
    sum(duration)/60 as hours, 
    round(cast(sum(effective_rate*duration/60) as numeric),2) as earned, 
    round(cast(avg ( effective_rate ) as numeric),0) as avg_rate
FROM lesson 
    INNER JOIN subject 
        USING(subjectid)
GROUP BY subject
ORDER BY n_lessons DESC;