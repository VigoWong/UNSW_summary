select distinct p.unswid,p.name from people p
join course_staff cs on cs.staff = p.id
join 
 (select id from  courses
  join course_enrolments ce on ce.student = p.id
  where p.name = 'Hemma Margareta') o
on o.id = cs.course;