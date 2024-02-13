# Réflexion pour la database

## Task
- [ ] task_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] name
- [ ] project
- [ ] description
- [ ] priority(1 to 5)
- [ ] delay
- [ ] state(“On Going” “Done” “Stop”)
- [ ] users
- [ ] comments

## Project
- [ ] project_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] nom
- [ ] description
- [ ] delay
- [ ] completion
- [ ] admin_user

## User
- [ ] user_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] surname
- [ ] name
- [ ] user_type


- FOR <span style="color:green">**Project Manager**</span> 
- [ ] my_projects 


- FOR <span style="color:green">**Developper**</span> 
- [ ] tasks
- [ ] skills

## Comment
- [ ] comment_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] creation_date
- [ ] user
- [ ] content



