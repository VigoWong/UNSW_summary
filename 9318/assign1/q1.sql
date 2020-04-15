drop table q1;
CREATE TABLE if not exists q1(
    location VARCHAR(32) not null,
    time VARCHAR(32),
    item VARCHAR(32) not null,
    quantity int 
);

-- Insert rows into table 'TableName'
INSERT INTO q1
( -- columns to insert data into
 location, time, item, quantity
)
VALUES
( -- first row: values for the columns in the list above
 'Sydney', '2005', 'PS2', 1400
),
( -- second row: values for the columns in the list above
 'Sydney', '2006', 'PS2', 1500
),
( -- first row: values for the columns in the list above
 'Sydney', '2006', 'Will', 500
),
( -- first row: values for the columns in the list above
 'Melbourne', '2005', 'xBox 360', 1700
);

SELECT Location, time, item, SUM(quantity) FROM q1 CUBE Location, time, item HAVING COUNT(*) > 1;
-- question 1 t2:
(SELECT * from q1) UNION 
(SELECT 'ALL' , time, item, sum(quantity) from q1 group by time, item) UNION
(SELECT location, 'ALL', item, sum(quantity) from q1 group by location, item) UNION
(SELECT location, time, 'ALL', sum(quantity) from q1 group by location, time) UNION
(SELECT 'ALL' , 'ALL' , item, sum(quantity) from q1 group by item) UNION
(SELECT 'ALL' , time, 'ALL' , sum(quantity) from q1 group by time) UNION
(SELECT location, 'ALL' , 'ALL', sum(quantity) from q1 group by location) UNION
(SELECT 'ALL' , 'ALL' , 'ALL' , sum(quantity) from q1)
cube by 
ORDER by location, time, item
;