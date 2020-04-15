-- comp9311 19T3 Project 1
--
-- MyMyUNSW Solutions


-- Q1:
create or replace view Q1(unswid, longname)
as select distinct r.unswid, r.longname from rooms r 
join room_facilities rf on rf.room = r.id 
join facilities f on rf.facility = f.id
where f.description = 'Air-conditioned';


--... SQL statements, possibly using other views/functions defined by you ...


-- Q2:
create or replace view Q2(unswid,name)
as select distinct p.unswid,  p.name from people p 
join course_staff cs on cs.staff = p.id
join 
    (select course from course_enrolments ce
    join people p on ce.student = p.id
    where p.name = 'Hemma Margareta') t2 
on cs.course =  t2.course;
--... SQL statements, possibly using other views/functions defined by you ...

-- Q3:
create or replace view Q3(unswid, name)
as
select distinct p.unswid, p.name from people p
join students s on s.id = p.id
join 
-- student take both 'COMP9024' and 'COMP9311'
(
    select a.student from
        (select ce.student,c.semester from subjects s 
        join courses c on s.id = c.subject
        join course_enrolments ce on ce.course = c.id
        where s.code = 'COMP9311' and ce.grade = 'HD') a
    join
        (select ce.student,c.semester from subjects s 
        join courses c on s.id = c.subject
        join course_enrolments ce on ce.course = c.id
        where s.code = 'COMP9024' and ce.grade = 'HD') b
    on a.student = b.student and a.semester = b.semester
)stu on stu.student = s.id

where s.stype = 'intl';


-- 后面类似