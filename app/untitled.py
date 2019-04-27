	with open(file,'w') as new_file, open(file,'r') as read_file:
		writer = csv.writer(new_file)
		reader = csv.reader(read_file)
		writer.writerows(sorted(reader, key=lambda x:int(x[1]))) 
		for y in array[:]:
			print len(array)
			try:
				if int((array[y+1]) == int(array[y])):
					del array[y]
					print array[y]
				elif int((array[y+1]) != int(array[y])):
					new_array.append(int(array[y]))
				else:
					new_array.append(int(array[y]))
					# continue
			except IndexError:
				new_array.append(int(array[y]))
				break
		writer.writerow(new_array)