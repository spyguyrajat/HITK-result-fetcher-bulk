import sys,os,requests

def get_data(haystack, needle):
	print(haystack)
	a = haystack.split(needle)
	#print("a = ",a)
	#print(a)
	b = a[1].split("</span>")
	return b[0]

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def progress(percent, currentRoll):
	os.system('cls')
	loaded = int(percent/2.5)
	if loaded != 40:
		print('Current Roll -', currentRoll)
	print('Fetching Results  | ', '#'*loaded , '-'*(40-loaded), ' | ', "{:.2f}".format(percent), '%', sep="")

f1 = open("result.txt", 'w+')
final = []
print ("Enter the roll number range (eg : 16616001001 12616001189) : ")
start, end = input().split()
print ("Enter the sem number (eg : 2) : ")
sem = int(input())
print ("Enter your choice : ")
print ("1. Get Results sorted alphabetically")
print ("2. Get Results sorted rankwise")
f1.write("https://github.com/spyguyrajat\n")
choice = int(input())
for x in range(int(start), int(end) + 1) :
	r = requests.post("http://136.232.2.202:8084/hres21o.aspx", data={'roll': x, 'sem': sem})
	string = r.text
	#print("string = ",string)
	percent = ((x - int(start)) *100) / (int(end)-int(start))
	enablePrint()
	progress(percent, x)
	blockPrint()
	if "No such student exists in this database or the student has not given the particular semester exam" in string:
		continue
	name = get_data(string, "<span id=\"lblname\">Name  ")
	roll = get_data(string, "<span id=\"lblroll\">Roll No.  ")
	if sem == 7:
		SGPA = get_data(string, "<span id=\"lblbottom1\">SGPA       ODD(7th.) SEMESTER: ")
	elif sem == 4:
		SGPA = get_data(string, "<span id=\"lblbottom2\">SGPA       EVEN(4th.) SEMESTER: ")
	elif sem == 6 :
		SGPA = get_data(string, "<span id=\"lblbottom2\">SGPA       EVEN(6th.) SEMESTER: ")
	else :
		SGPA = get_data(string, "<span id=\"lblbottom2\">SGPA       EVEN(8th.) SEMESTER: ")
	name = name.encode('ascii', 'ignore').decode('ascii')
	if choice == 1 :
		SGPA = str(float(SGPA))
		SGPA += '0'*(4-len(SGPA))
		f1.write(" ".join([roll, name, SGPA.rjust(27-len(name)), '\n']))
	else :
		tup = (float(SGPA), name, roll)
		final.append(tup)
	print(x)
final.sort(reverse = True)
rank = 0
prev_sgpa = '0.00'
for s, name, r in final:
	s = str(s)
	if len(s) == 3:
		s += '0'
	if prev_sgpa == s:
		f1.write(" ".join([len(str(rank))*' ', s, r, name, '\n']))
	else:
		rank += 1
		f1.write(" ".join([str(rank), s, r, name, '\n']))
		prev_sgpa = s
f1.close()
