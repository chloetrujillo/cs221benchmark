Hello!!! This program is our benchmark function for CS221. :)

Most of the files are from the explorecourses API we used to access the course description data.

BACKEND/ DATA PROCESSING:
This all happens in mycode-stanford.py The backend has naively tokenized every course description, and created a tally of the 100 most frequently used tokens across all course descriptions for a given department in a given year. The departments are those which still exist in 2023, and the academic years span every other year from 2001-2002 to 2023-2024.

FRONT END:
By running python3 benchmarkprogram.py, you can naively see how similar two departments are. The program will first prompt you:
"Type 1 to predict what department a given course description belongs to. Type 2 to compare the similarity of two year-department combinations."

Option 1:
--- If you choose 1, the program will attempt to classify an unseen description, assuming that it comes from a specific year. Both the description and year are given as user input. 
--- It will then tokenize your description, and see which department's most frequent keywords has the greatest overlap with your input.

Option 2:
-- If you choose 2, the program will ask you for two year, department pairs. 
-- It will then calculate the Jaccard similarity (overlap set/ total set) between the sets fo their most frequent keywords. 
