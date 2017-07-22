# Instruction to Run the code

- Clone repository from github in to your homedirectory
- To get the images in the local execute: 
   - docker pull prashantvksingh/team6midterm_part1:part1
   - docker pull prashantvksingh/team6midterm_part2:part2
- Execute  docker run  -e username="prashantvksingh@gmail.com" -e password="V4wlNZow" -e startYear=2005 -e  endYear=2009 prashantvksingh/team6midterm_part1:part1 /usr/src/Midterm_Part1/run.sh
  - Execute docker ps -l (to get the ID of last run container)
  - Execute docker commit 'ID received from above code' prashantvksingh/team6midterm_part1:part1
- Execute docker run -p 8888:8888 prashantvksingh/team6midterm_part1:part1 /bin/bash -c 'jupyter notebook --no-browser --ip=* --allow-root'

- Execute docker run  -e username="prashantvksingh@gmail.com" -e password="V4wlNZow" -e trainQuarter=Q12005 -e  testQuarter=Q22005 prashantvksingh/team6midterm_part2:part2 /usr/src/Midterm_Part2/run.sh
  - Execute docker ps -l (to get the ID of last run container)
  - Execute docker commit 'ID received from above code' prashantvksingh/team6midterm_part2:part2
- Execute docker run -p 8888:8888 prashantvksingh/team6midterm_part2:part2 /bin/bash -c 'jupyter notebook --no-browser --ip=* --allow-root'
   
## To create and run Part 1 docker image manually:
- Navigate to Part1 directory
- Execute docker build -t team6midterm_part1 .
- Execute  docker run  -e username="prashantvksingh@gmail.com" -e password="V4wlNZow" -e startYear=2005 -e  endYear=2009 team6midterm_part1 /usr/src/Midterm_Part1/run.sh
  - Execute docker ps -l (to get the ID of last run container)
  - Execute docker commit 'ID received from above code' team6midterm_part1
- Execute docker run -p 8888:8888 team6midterm_part1 /bin/bash -c 'jupyter notebook --no-browser --ip=* --allow-root'

## To create and run Part 2 docker image manually:
- Navigate to Part2 directory
- Execute docker build -t team6midterm_part2 .
- Execute docker run  -e username="prashantvksingh@gmail.com" -e password="V4wlNZow" -e trainQuarter=Q12005 -e  testQuarter=Q22005 team6midterm_part2 /usr/src/Midterm_Part2/run.sh
  - Execute docker ps -l (to get the ID of last run container)
  - Execute docker commit 'ID received from above code' team6midterm_part2
- Execute docker run -p 8888:8888 team6midterm_part2 /bin/bash -c 'jupyter notebook --no-browser --ip=* --allow-root'

## Fiile contains:
- part 1 
- DataIngestion_Part1.py this file is for data injestion 
- EDA_Part1.ipynb is for EDA

- PART 2
- Prediction_algos is for algo prediction
- Classification_2 is for classification. 

- In python notebook need to run each cell sequentially . also enter the year and quarter for prediction 
