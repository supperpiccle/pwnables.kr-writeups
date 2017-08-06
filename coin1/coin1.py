from pwn import *

conn = remote("127.0.0.1", 9007);


#this function will take a given problem
#and come up with a solution
def solveProblem(s):
	subProblems = s.split(" ")[0].split("=")[1]
	findCoin(0, int(subProblems) - 1)#this function is recursive
	

#this recursive function will call
#itself with a new beginIndex and endIndex
#which are imaginary indexes in which the fake coin
#is in
#NOTE: this function uses a form of binary search!
#to understand this solution read about binary search!
def findCoin(beginIndex, endIndex):
	#pick a half point
	halfPoint = (endIndex - beginIndex) / 2	 + beginIndex

	#construct a string from beginIndex to
	#half point to give to the server
	strList = ""
	for i in range(beginIndex, halfPoint + 1):
		strList = strList + " " + str(i)	
	#remove the first space that appears in 
	#the list
	strList = strList[1:]

	#print the string for us to see:)
	print
	print strList


	#send the line to the server
	conn.sendline(strList)

	#get a result
	result = conn.recv()

	#If the string has correct then
	#we are done.
	if "Correct" in result:
		print result
		return

	#print the result for us to see
	print result

	#the next lines are what makes this function
	#recursive:).  If you don't know about recursive
	#functions go read about them!  They make problems
	#like this very easy to solve (Note that a loop approach
	#could have worked and been implemented but would
	#be much more difficult to understand and write

	#if the result is NOT evenly divideable by 10
	#then the coin is somewhere between beginIndex
	#and the halfway point so we simply call this
	#function with those points as the new begin and end 
	if int(result) % 10 != 0:
		 findCoin(beginIndex, halfPoint) #found

	#if the result IS evenly dividable by 10 then 
	#the solution is from halfPoint+1 to the end.
	#We add +1 to halfway point because that position
	#was also tested
	elif int(result) % 10 == 0:
		 findCoin(halfPoint + 1, endIndex) #not found




##MAIN FUNCTION
probsSolved = 0
while True: #Keep going until the end of time!
	s = conn.recv() #This will recieve intro stuff
	print s
	if(s[0] == 'N'): #we got a number of coins to go through 
			#this is the beginning of computation
		solveProblem(s) #solve this problem
		probsSolved += 1
		print probsSolved
