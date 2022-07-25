from tkinter import *
from tkinter import messagebox
#from tkinter.colorchooser import askcolor
from datetime import datetime
import pytz
import requests


software_version='v1.1'
IST=pytz.timezone('Asia/Kolkata')

app=Tk()

#app gui

app.geometry("700x480+300+100")
app.title(f"Vaccine Availabilty Checker {software_version}")
app.iconbitmap("/Users/HP/Desktop/Extras/Projects/Python - Vaccine Availability Checker/Icons/vaccine.ico")
app.resizable(True,True)
app.config(background="#293241")

## DEFAULT values
PINCODE = '110096'

# Color Value Reference
top_left_frame="#5c4ce1"
top_right_frame="MediumPurple1"


#adding frames

frame1= Frame(app,height=120,width=180,bg=top_left_frame,bd=1,relief=FLAT)
frame1.place(x=0,y=0)

frame2= Frame(app,height=120,width=520,bg=top_right_frame,bd=1,relief=FLAT)
frame2.place(x=180,y=0)

frame3= Frame(app,height=30,width=700,bg="Black",bd=1,relief=RAISED)
frame3.place(x=0,y=120)

# Labels

label_date_now=Label(text="Current Date",bg=top_left_frame,font='verdana 12 bold')
label_date_now.place(x=20,y=40)

label_time=Label(text="Current Time",bg=top_left_frame,font='verdana 12')
label_time.place(x=20,y=60)

label_pincode=Label(text="Pincode",bg=top_right_frame,font='verdana 10 bold')
label_pincode.place(x=220,y=18)

label_date=Label(text="Date[dd:mm:yy]",bg=top_right_frame,font='verdana 8 bold')
label_date.place(x=380,y=18)

label_search_vacc=Label(text="Search",bg=top_right_frame,font='verdana 10 bold')
label_search_vacc.place(x=596,y=65)

label_head_result=Label(text=" Status       \tCentre Name\t     Age-Group      Vaccine         Dose1        Dose2       Total",bg="black",fg="white",font='verdana 10 bold')
label_head_result.place(x=0,y=122)

# Entry Boxes

pincode_txt_var=StringVar()
#result=askcolor(title = "Tkinter Color Chooser")
pincode_txt=Entry(app,width=8,bg="#ffff80",fg="black",font="verdana",textvariable=pincode_txt_var)
pincode_txt['textvariable']=pincode_txt_var
pincode_txt.place(x=220,y=40)


date_txt_var=StringVar()
#result=askcolor(title = "Tkinter Color Chooser")
date_txt=Entry(app,width=10,bg="#ffff80",fg="black",font="verdana",textvariable=date_txt_var)
date_txt.place(x=380,y=40)
date_txt['textvariable']=date_txt_var



# text Box for displaying results

result_box_avl=Text(app,height=20,width=8,bg='#293241',fg='#ecfcff',relief=FLAT,font='verdana 10')
result_box_avl.place(x=3,y=152)

result_box_cent=Text(app,height=20,width=25,bg='#293241',fg='#ecfcff',relief=FLAT,font='verdana 10')
result_box_cent.place(x=89,y=152)

result_box_age=Text(app,height=20,width=12,bg='#293241',fg='#ecfcff',relief=FLAT,font='verdana 10')
result_box_age.place(x=300,y=152)

result_box_vaccine=Text(app,height=20,width=10,bg='#293241',fg='#ecfcff',relief=FLAT,font='verdana 10')
result_box_vaccine.place(x=400,y=152)

result_box_d1=Text(app,height=20,width=9,bg='#293241',fg='#ecfcff',relief=FLAT,font='verdana 10')
result_box_d1.place(x=490,y=152)

result_box_d2=Text(app,height=20,width=6,bg='#293241',fg='#ecfcff',relief=FLAT,font='verdana 10')
result_box_d2.place(x=570,y=152)

result_box_total=Text(app,height=20,width=7,bg='#293241',fg='#ecfcff',relief=FLAT,font='verdana 10')
result_box_total.place(x=638,y=152)



# Checking pincode

def fill_pincode_with_radio():
    curr_pincode=get_pincode_ip_service(url)
    pincode_txt_var.set(curr_pincode)
    

url='https://ipinfo.io/postal'
def get_pincode_ip_service(url):
    response_pincode=requests.get(url).text
    return response_pincode


# Defining Functions

def update_clock():
    raw_TS = datetime.now(IST)
    date_now = raw_TS.strftime("%d %b %Y")
    time_now = raw_TS.strftime("%H:%M:%S %p")
    formatted_now = raw_TS.strftime("%d-%m-%Y")
    label_date_now.config(text = date_now)
    # label_date_now.after(500, update_clock)
    label_time.config(text = time_now)
    label_time.after(1000, update_clock)
    return formatted_now
    


def insert_today_date():
    raw_TS=datetime.now(IST)
    formatted_now=raw_TS.strftime("%d-%m-%Y")
    date_txt_var.set(formatted_now)
    
# API calls

def refresh_api_call(PINCODE,DATE):
    header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={PINCODE}&date={DATE}"
    response = requests.get(request_link, headers = header)
    resp_JSON=response.json()
    return resp_JSON

def clear_result_box():
    result_box_avl.delete('1.0',END)
    result_box_cent.delete('1.0',END)
    result_box_age.delete('1.0',END)
    result_box_vaccine.delete('1.0',END)
    result_box_d1.delete('1.0',END)
    result_box_d2.delete('1.0',END)
    result_box_total.delete('1.0',END)


# Logic for search button

def search_vaccine_avl():
    clear_result_box()
    PINCODE=pincode_txt_var.get().strip()
    DATE=date_txt_var.get()
    resp_JSON=refresh_api_call(PINCODE,DATE)
    
    try:
        if len(resp_JSON['sessions'])==0:
            messagebox.showinfo("INFO","Vaccine not available yet for the given date")
            
        for sess in resp_JSON['sessions']:
            age_limit           =sess['min_age_limit']
            center_name         =sess['name']
            pincode             =sess['pincode']
            vaccine_name        =sess['vaccine']
            available_capacity  =sess['available_capacity']
            qnty_dose_1         =sess['available_capacity_dose1']
            qnty_dose_2         =sess['available_capacity_dose2']
            slot_date           =sess['date']
            
            
            if available_capacity>0:
                curr_status='Available'
            else:
                curr_status='NA'
                
            if age_limit>=45:
                age_group='45+'
            else:
                age_group='18-44'
                
            
            result_box_avl.insert(END, f"{curr_status:^6s}")
            result_box_avl.insert(END,"\n")
            result_box_cent.insert(END, f"{center_name:<30.29s}")
            result_box_cent.insert(END,"\n")
            result_box_age.insert(END, f"{age_group:<6s}")
            result_box_age.insert(END,"\n")
            result_box_vaccine.insert(END, f"{vaccine_name:<8s}")
            result_box_vaccine.insert(END,"\n")
            result_box_d1.insert(END, f"{qnty_dose_1:>5}")
            result_box_d1.insert(END,"\n")
            result_box_d2.insert(END, f"{qnty_dose_2:>5}")
            result_box_d2.insert(END,"\n")
            result_box_total.insert(END, f"{available_capacity:<5}")
            result_box_total.insert(END,"\n")
            
    except KeyError as KE:
        messagebox.showerror("ERROR","No Available center(s) for the given Pincode and date")
        print (pincode_txt_var.get())



                
# Button

search_vaccine=PhotoImage(file="/Users/HP/Desktop/Extras/Projects/Python - Vaccine Availability Checker/Icons/resize.png")
search=Button(app,bg=top_right_frame,relief=RAISED,command='',image=search_vaccine)
search.place(x=600,y=25)
    

# # Radio Button

cur_loc_var=StringVar()
radio_location=Radiobutton(app,text='Current Location',bg=top_right_frame,variable=cur_loc_var,value=cur_loc_var,command=fill_pincode_with_radio)
radio_location.place(x=210,y=70)

# Check Box for Todays Date

chkbox_todays_var=IntVar()
todays_date_chkbox=Checkbutton(app,text='Today',bg=top_right_frame,variable=chkbox_todays_var,onvalue=1,offvalue=0,command=insert_today_date)
todays_date_chkbox.place(x=380,y=70)


update_clock()

app.mainloop()