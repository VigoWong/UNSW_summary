-- comp9311 19T3 Project 1
--
-- MyMyUNSW Solutions


-- Q1:
create or replace view Q1(unswid, longname)
as select distinct r.unswid, r.longname from rooms r 
join room_facilities rf on rf.room = r.id 
join facilities f on rf.facility = f.id
where f.description = 'Air-conditioned';

-- Q2:
create or replace view Q2(unswid,name)
as select distinct p.unswid,  p.name from people p 
join course_staff cs on cs.staff = p.id
join 
    (select course from course_enrolments ce
    join people p on ce.student = p.id
    where p.name = 'Hemma Margareta') t2 
on cs.course =  t2.course;

-- Q3:
-- student take 'COMP9311'
create or replace view Q3_1 as
select ce.student,c.semester from subjects s 
join courses c on s.id = c.subject
join course_enrolments ce on ce.course = c.id
where s.code = 'COMP9311' and ce.grade = 'HD';

-- student take 'COMP9024'
create or replace view Q3_2 as
select ce.student,c.semester from subjects s 
join courses c on s.id = c.subject
join course_enrolments ce on ce.course = c.id
where s.code = 'COMP9024' and ce.grade = 'HD';

-- finish
create or replace view Q3(unswid,name) as
select distinct p.unswid, p.name from people p
join students s on s.id = p.id
join Q3_1 q1 on s.id = q1.student
join Q3_2 q2 on q1.student = q2.student and q1.semester = q2.semester
where s.stype = 'intl';

-- Q4:
-- the number of HD gotten by all student
create or replace view student_HD_num as
select count(*) as HD from course_enrolments 
where grade = 'HD';

-- the number of student who have at least one valid mark
create or replace view student_num(student_num) as
SELECT count(*) from students s where s.id in 
(select student from course_enrolments where mark is not null);

-- the avg number of hd of all students
create or replace view avg_HD_num as
SELECT shn.HD/sn.student_num as avg_HD_num 
from student_HD_num shn,student_num sn;


-- the enrolment_record of student who get more HD than average
create or replace view Q4(num_student) as
select count(*) from 
(SELECT distinct student,count(*) as HD from course_enrolments ce 
where grade = 'HD' group by student) a 
join avg_HD_num ahn on a.HD > ahn.avg_HD_num;

--Q5:
-- each course id match one subject and one semester
-- select valid courses of all terms
create or replace view valid_course as
select * from 
(select course, count(*) as valid_num from course_enrolments where mark is not null group by course) a 
where a.valid_num >= 20 order by valid_num asc;

-- select the max score of each course 
create or replace view course_max_mark as
select max(mark), vc.course from course_enrolments ce 
join valid_course vc on vc.course = ce.course
group by vc.course;

-- select the semester of course with max_mark of each course 
create or replace view course_max_mark_semester as
select cm.max as max_mark,cm.course, sem.id as semester from course_max_mark cm
join courses c on c.id = cm.course
join semesters sem on sem.id = c.semester;

-- select the min(max_mark) of course groupby semester, then select the courses with max_mark equals to this
create or replace view Q5_match_course as
select a.course,a.max_mark,a.semester from course_max_mark_semester a join 
(select min(max_mark), semester as max_mark,semester from course_max_mark_semester group by semester) b
on a.semester = b.semester and a.max_mark = b.min;

-- finish
create or replace view Q5(code, name, semester)
as select  subj.code, subj.name,sem.name from 
    (select course from Q5_match_course) a
    join courses c on c.id = a.course
    join semesters sem on sem.id = c.semester
    join subjects subj on subj.id = c.subject;

-- Q6:
-- local student who take  Management stream in 10s1
CREATE or replace VIEW S1_management_stu as 
SELECT distinct peo.unswid
from program_enrolments pe 
join people peo on peo.id = pe.student
JOIN students stu on stu.id = pe.student
join stream_enrolments se on se.partof = pe.id
join streams s on se.stream = s.id
join semesters sem on pe.semester = sem.id
WHERE sem.year = '2010' and sem.term = 'S1' and 
s.name = 'Management' and stu.stype = 'local';

-- student who has enrolled in course offered by Faculty of Engineering.
CREATE or replace VIEW engine_stu as 
SELECT distinct peo.unswid 
from people peo 
join course_enrolments ce on ce.student = peo.id
join courses c on c.id = ce.course
join subjects sbj on sbj.id = c.subject 
join OrgUnits org on sbj.offeredby = org.id
WHERE org.name = 'Faculty of Engineering';


-- difference set of above two table
create or replace view Q6(num) as 
select count(*) from 
((SELECT * from S1_management_stu) 
EXCEPT (select * from engine_stu)) a ;


-- Q7:
-- avg mark of each course
create or replace view Q7(year, term, average_mark)as
SELECT distinct s.year, s.term,round(avg(mark),2) as avg_mark from 
(select * from course_enrolments
where mark is not null) a
join courses c on c.id = a.course
join semesters s on s.id = c.semester
join subjects subj on subj.id = c.subject
where subj.name = 'Database Systems'
group by s.year, s.term
order by year, term;

-- Q8:
-- major semester
create or replace view major_sem as
select a.id, a.year, a.term from semesters a 
join (SELECT b.id,b.year,b.term from semesters b where term = 'S1' or term = 'S2') b
on a.id = b.id
where a.year between 2004 and 2013;

-- course start and its term with “COMP93”
create or replace view comp93 as 
SELECT sbj.id as subject, sem.id as semester from courses c
join subjects sbj on sbj.id =c.subject 
join semesters sem on c.semester = sem.id
where sbj.code like 'COMP93%';

-- fix the year 2007 
create or replace view major_sem_fixed as 
select distinct a.id from major_sem a left join comp93 b 
on a.id = b.semester where b.subject is not null order by a.id;

-- cse subject 
create or replace view cse_subject as 
SELECT distinct a.subject from comp93 a WHERE not EXISTS
(select * from major_sem_fixed b 
except (select c.semester from comp93 c
where c.subject = a.subject));

-- student of CSE subject and has failed a course
create or replace view fail_cse_student_ls as 
SELECT ce.student,cse.subject as sbj_id from course_enrolments ce 
join courses c on c.id = ce.course
join cse_subject cse on cse.subject = c.subject
where ce.mark is not null and mark<50;

-- finish
create or replace view Q8(zid, name) as
select distinct concat('z',peo.unswid), peo.name from (
SELECT a.student from fail_cse_student_ls a
where not EXISTS (SELECT b.subject from cse_subject b except 
(select c.sbj_id from fail_cse_student_ls c where c.student = a.student))
)d join people peo on peo.id = d.student;


-- Q9:
-- student pass at least one course in the program in 2010 S2
create or replace view Q9_1_0 as
select * from course_enrolments ce where mark is not null and mark >= 50;

create or replace view Q9_1_1 as
SELECT id as semester from semesters where year = 2010 and term = 'S2';

create or replace view Q9_1 as
select distinct ce.student,pro_enrol.program from Q9_1_0 ce  
join courses c on c.id = ce.course
join Q9_1_1 sem on sem.semester = c.semester
join program_enrolments pro_enrol 
on pro_enrol.student = ce.student and pro_enrol.semester = sem.semester;

-- student enrolled in bsc
create or replace view Q9_2 as
select distinct student from program_enrolments pro_enrol
join program_degrees pro_de on pro_de.program = pro_enrol.program
WHERE pro_de.abbrev ='BSc';

-- students with average mark over 80 before 2011 
create or replace view Q9_3_0 as
select * from course_enrolments where mark is not null and mark >= 50;

create or replace view Q9_3_1 as
select ce.student, pro_enrol.program, avg(ce.mark) as avg_mark from Q9_3_0 ce 
join courses c on ce.course = c.id 
join semesters sem on c.semester = sem.id 
join program_enrolments pro_enrol on pro_enrol.student = ce.student
where sem.year < 2011
group by ce.student, pro_enrol.program;

create or replace view Q9_3 as
select distinct * from Q9_3_1
where avg_mark >= 80;


-- the total uoc acquired by each student
create or replace view uoc_each_student as
select distinct ce.student, pro_enrol.program, sum(sbj.uoc) as uoc from Q9_3_0 ce
join courses c on ce.course = c.id
join subjects sbj on c.subject = sbj.id
join semesters sem on c.semester = sem.id
join program_enrolments pro_enrol on pro_enrol.student = ce.student
     and pro_enrol.semester = c.semester
where sem.year < 2011
group by ce.student, pro_enrol.program;


-- the list of student who satisfy the uoc requirement
create or replace view Q9_4 as
select distinct pe.student from uoc_each_student a
join program_enrolments pe on pe.student = a.student
join programs p on pe.program = p.id
WHERE a.uoc >= p.uoc;


-- finish
create or replace view Q9(unswid, name) as
select distinct peo.unswid,peo.name from people peo
join Q9_1 a on peo.id = a.student
join Q9_2 b on a.student = b.student
join Q9_3 c on b.student = c.student
join Q9_4 d on c.student = d.student;


-- Q10
-- the class of 2011 S1 
create or replace view class_S1_2011 as
select cls.room, COUNT(*) as num from courses cur join
(select * from semesters where year =2011 and term = 'S1') sem 
on cur.semester = sem.id
join classes cls on cls.course = cur.id
group by cls.room
order by num DESC;

-- the room of lecture theatre
create or replace view room_lecture_theatre as
select r.id from rooms r JOIN
(select * from room_types where description = 'Lecture Theatre') rt 
on r.rtype = rt.id;

-- finish
create or replace view Q10(unswid, longname, num, rank) as
SELECT *, rank() over(order by num DESC) from (
    select unswid, longname, 
        coalesce(num,0) as num
        from (
        SELECT r.unswid,r.longname, a.num from room_lecture_theatre b 
        left join class_S1_2011 a on a.room = b.id
        join rooms r on r.id = b.id) a) a;
