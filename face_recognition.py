from distutils import spawn
from tkinter import*
from tkinter import ttk
from tokenize import Name
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import os
import numpy as np
import pyttsx3




engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 is for female voice and 0 is for male voice

def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()

class Face_Recognition:
	def __init__(self, root):
		self.root=root
		self.root.geometry("1530x790+0+0")
		self.root.title("Face Recongnition System")

		title_lbl=Label(self.root,text="FACE RECOGNITION",font=("Sketchy In Snow", 35,"bold"),bg="red",fg="white")
		title_lbl.place(x=0,y=0,width=1530,height=45)

		#Image in top bar
		img_top=Image.open(r"F:\machine\img\face_detector1.jpg")
		
		img_top=img_top.resize((650,700),Image.ANTIALIAS)
		self.photoimg_top=ImageTk.PhotoImage(img_top)

		f_lbl=Label(self.root,image=self.photoimg_top)
		f_lbl.place(x=0,y=55,width=650,height=700) 


		#Image in side right bar
		img_bottom=Image.open(r"F:\machine\img\face.jpg")
		
		img_bottom=img_bottom.resize((950,700),Image.ANTIALIAS)
		self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

		f_lbl=Label(self.root,image=self.photoimg_bottom)
		f_lbl.place(x=650,y=55,width=950,height=700) 

		#button
		b1_1=Button(f_lbl,text="Face Recongnition", command=self.face_recog,cursor="hand2",font=("times new roman", 18,"bold"),bg="red",fg="white")
		b1_1.place(x=365,y=620,width=200,height=40)

	#========Attendance========
	def mark_attendance(self,i,r,n,d,e):
		with open("MyTest.csv","r+",newline="\n") as f:
			myDataList=f.readlines()
			name_list=[]
			for line in myDataList:
				entry=line.split((","))
				name_list.append(entry[0])
			if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
				now=datetime.now()
				d1=now.strftime("%d/%m/%Y")
				dtString=now.strftime("%H:%M:%S")
				f.writelines(f"\n{i},{r},{n},{d},{e},{dtString},{d1},Present")
	


	#=======face recognition=====
	def face_recog(self):
		def draw_boundary(img,classifier,scaleFactor,minNeighbors,color,text,clf):
			gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

			coord=[]

			for (x,y,w,h) in features:
				cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
				id,predict=clf.predict(gray_image[y:y+h,x:x+w])
				confidence=int((100*(1-predict/300)))

				conn=mysql.connector.connect(host="localhost",username="root",password="1234",database="face_recognizer")
				my_cursor=conn.cursor()


				#Fetching Name
				my_cursor.execute("SELECT Name FROM student WHERE Student_id="+str(id))
				n=my_cursor.fetchone()
				#n=str(n)
				#print (n)
				n="+".join(n)


				#For department fetching
				my_cursor.execute("SELECT Student_id FROM student WHERE Student_id="+str(id))
				i=my_cursor.fetchone()
				#i = str(i)
				i="+".join(i)

				#For course fetching
				my_cursor.execute("select Email from student where Student_id="+str(id))
				e=my_cursor.fetchone()
				#e = str(e)
				e="+".join(e)

				'''#For year fetching
				my_cursor.execute("select Year from student where Student_id="+str(id))
				y=my_cursor.fetchone()
				y = str(y)
				#y="+".join(y)

				#For semester fetching
				my_cursor.execute("select Semester from student where Student_id="+str(id))
				s=my_cursor.fetchone()
				s = str(s)
				#s="+".join(s)'''



				#Fetching registration
				my_cursor.execute("SELECT Reg FROM student WHERE Student_id="+str(id))
				r=my_cursor.fetchone()
				#r = str(r)
				r="+".join(r)

				#Fetching Student ID
				my_cursor.execute("SELECT Dep FROM student WHERE Student_id="+str(id))
				d=my_cursor.fetchone()
				#d = str(d)
				d="+".join(d)


				
				if confidence>55:
					cv2.putText(img,f"{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
					cv2.putText(img,f"{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
					cv2.putText(img,f"{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
					cv2.putText(img,f"{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
					#cv2.putText(img,f"Semester:{s}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
					self.mark_attendance(i,r,n,d,e)
					speak_va('Welcome'+n)
					
					
				
				#If face doesn't match	
				else:
					cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
					cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
					speak_va('Unknown Face')
				coord=[x,y,w,h]
			return coord
		
		def recognize(img,clf,faceCascade):
			coord=draw_boundary(img,faceCascade,1.1,10,(255,25,255),"Face",clf)

			return img
		faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
		clf=cv2.face.LBPHFaceRecognizer_create()
		clf.read("classifier.xml")

		video_cap=cv2.VideoCapture(0) # it was 0 inside

		while True:
			ret,img=video_cap.read()
			img=recognize(img,clf,faceCascade)
			cv2.imshow("Welcome to Face Recongnition",img)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		video_cap.release()
		cv2.destroyAllWindows()			



					

					





if __name__=="__main__":
	root=Tk()
	obj=Face_Recognition(root)
	root.mainloop()			
