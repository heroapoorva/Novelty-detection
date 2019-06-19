with open('clean.json') as json_file:  
    lines=json_file.readlines()
with open('dict.json') as json_file:  
    data = json.load(json_file)
print("Read the news files and the dictionary")

(top_dict,indices)=get_top(20000,data)
print("got dictionary")

lines=dictionary_array(lines)
print("Parsing finished!")

(start_position,end_position)=date_dictionary(lines)
print("Dictionary created")

start_date=str(input("Enter the date from which you want to start comparing\n The format should be YYYYMMDD.\n"))
end_date=str(input("Enter the date till which you want to compare, the date is not included.\n The format should be YYYYMMDD.\n"))
nn=input("Specify index of the news article you want compare against the window.")
matrix=create_matrix(lines[start_position[start_date]:start_position[end_date]],top_dict,indices)
print("Matrix created.")
for i in range(start_position[str(end_date)]+1, end_position[str(end_date)]):
    (sp, si) = tfidf(matrix, lines, top_dict, indices, i, start_position[start_date])
    print(si)
