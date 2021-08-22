# PowerFusionMedia-Project
A mini project to populate and update database and authenticate users.

## BB Product Task - 
### http://pfmproduct-env-1.eba-pvj3mxhy.us-east-2.elasticbeanstalk.com/

## Population 5 Mile Radius - 
### http://pfmpopulation-env.eba-wfgfjc6e.us-east-2.elasticbeanstalk.com/

### Credentials to login
Email - root1@gmail.com or root2@gmail.com
Password - 123456

### Tech stack and steps done to achieve the project

* Create a cloud formation stack to populate the database into Dynamo DB when the csv file is uploaded into S3 bucket in the click of a button.
* Implement the backend in Flask, HTML5 and Bootstrap for frontend.
* Application deployed on AWS Elastic Bean Stalk
* Dynamo Db used to store user credentials and csv data to utilize optimized reads.

## Some screenshots to prove the robustness and correctness of the project.

***

#### Login and Register Pages

![login](https://user-images.githubusercontent.com/55814855/130348901-2021a25d-441c-4485-a756-09d33488d2d6.JPG)
![register](https://user-images.githubusercontent.com/55814855/130348902-42371122-6f22-4180-b909-6f85a8a81c74.JPG)

***

### Handling empty values in csv file

![na_vales](https://user-images.githubusercontent.com/55814855/130349116-d0d7a149-9124-45cd-b245-7fd240a0facd.JPG)
![na_values_error](https://user-images.githubusercontent.com/55814855/130349121-bdb3f2f5-1ed7-44ce-9acd-01c3ddc0d539.JPG)

***

### Handling no file upload

![no_file_error](https://user-images.githubusercontent.com/55814855/130349147-97160239-8058-4e32-bfbf-0c99cc6028e6.JPG)

***

### Handling empty data
![empty_mod_user](https://user-images.githubusercontent.com/55814855/130349157-7a05b4c1-5478-4fd4-80f0-ae014eb3fbd1.JPG)
![empty_mod_error](https://user-images.githubusercontent.com/55814855/130349159-1506b49c-1b14-4acb-a009-8a4d7470f499.JPG)

***

### Handling corrupt data
![bad_data](https://user-images.githubusercontent.com/55814855/130349169-7651c00e-41cc-4f09-9d70-92cf7c92edb1.JPG)
![date_error](https://user-images.githubusercontent.com/55814855/130349174-13fb44c7-d4c5-4bfc-bd97-13984951901e.JPG)

***

### Displaying all N/A values for empty entries

![na_vales](https://user-images.githubusercontent.com/55814855/130349199-edaa7254-4d2e-43b0-9ce3-8dc23dae5fa4.JPG)

***

### Clean data and updated records

![clean_data](https://user-images.githubusercontent.com/55814855/130349256-f2d1cd6b-ca4b-4ce8-93e1-13419720282f.JPG)
![records_success](https://user-images.githubusercontent.com/55814855/130349297-0084077d-b3b1-446c-8a5c-b114a7d2054e.JPG)

