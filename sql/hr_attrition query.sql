1. Attrition rate

 SELECT 
    attrition, 
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM hr_attrition
GROUP BY attrition;   



2.Attrition by department

SELECT 
    department,
    COUNT(*) FILTER (WHERE attrition = 'Yes') AS left_count,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / COUNT(*), 2) AS attrition_rate
FROM hr_attrition
GROUP BY department
ORDER BY attrition_rate DESC;

3. Attrition by overtime

SELECT 
    overtime,
    COUNT(*) FILTER (WHERE attrition = 'Yes') AS left_count,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / COUNT(*), 2) AS attrition_rate
FROM hr_attrition
GROUP BY overtime
ORDER BY attrition_rate DESC;

4. Attrition by income band

SELECT 
    CASE 
        WHEN monthly_income < 3000 THEN '1. Below 3000'
        WHEN monthly_income BETWEEN 3000 AND 6000 THEN '2. 3000-6000'
        WHEN monthly_income BETWEEN 6001 AND 10000 THEN '3. 6001-10000'
        ELSE '4. Above 10000'
    END AS income_band,
    COUNT(*) FILTER (WHERE attrition = 'Yes') AS left_count,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / COUNT(*), 2) AS attrition_rate
FROM hr_attrition
GROUP BY income_band
ORDER BY income_band ;

5.Attrition by tenure

SELECT 
    CASE 
        WHEN years_at_company <= 2 THEN '0-2 yrs'
        WHEN years_at_company BETWEEN 3 AND 5 THEN '3-5 yrs'
        WHEN years_at_company BETWEEN 6 AND 10 THEN '6-10 yrs'
        ELSE '10+ yrs'
    END AS tenure_band,
    COUNT(*) FILTER (WHERE attrition = 'Yes') AS left_count,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / COUNT(*), 2) AS attrition_rate
FROM hr_attrition
GROUP BY tenure_band
ORDER BY tenure_band;

6. Attrition by job role (highest risk roles)
SELECT 
    job_role,
    COUNT(*) FILTER (WHERE attrition = 'Yes') AS left_count,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / COUNT(*), 2) AS attrition_rate
FROM hr_attrition
GROUP BY job_role
ORDER BY attrition_rate DESC;

7. Rank departments by attrition rate (window function)

SELECT 
    department,
    ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / COUNT(*), 2) AS attrition_rate,
    RANK() OVER (ORDER BY ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / COUNT(*), 2) desc) AS rank
FROM hr_attrition
GROUP BY department;

8.Combined high-risk segment

WITH risk_segment AS (
    SELECT *
    FROM hr_attrition
    WHERE overtime = 'Yes' 
      AND job_satisfaction <= 2 
      AND monthly_income < 5000
)
SELECT 
    COUNT(*) AS total_at_risk,
    COUNT(*) FILTER (WHERE attrition = 'Yes') AS actually_left,
    ROUND(100.0 * COUNT(*) FILTER (WHERE attrition = 'Yes') / COUNT(*), 2) AS attrition_rate
FROM risk_segment;



    