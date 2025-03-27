from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
from PIL import Image, ImageTk
import randomcolor

def connect_database():
    try:
        connection=pymysql.connect(host='localhost', user='root',password='1234')
        cursor=connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connectivity issue. Open MYSQL command line client')
        return None,None
    cursor.execute('CREATE DATABASE IF NOT EXISTS Product_loading')
    cursor.execute('USE product_loading')
    cursor.execute('CREATE TABLE IF NOT EXISTS truckload_data(rowid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,prodid INT, description VARCHAR(255), weight INT,length INT, width INT, height INT)')
    return cursor,connection
  

def ltreeview_data():
    cursor,connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('SELECT * from product_data')
        response= cursor.fetchall()
        mainpagetreeview.delete(*mainpagetreeview.get_children())
        for record in response:
            mainpagetreeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def truck_treeview_data():
    cursor,connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('SELECT * from truckload_data')
        response= cursor.fetchall()
        trucktreeview.delete(*trucktreeview.get_children())
        for record in response:
            trucktreeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def select_data(event,prodid_entry,description_entry,weight_entry,length_entry,width_entry,height_entry):
    index=mainpagetreeview.selection()
    content=mainpagetreeview.item(index)
    row=content['values']
    clear_fields(prodid_entry,description_entry,weight_entry,length_entry,width_entry,height_entry,False)
    prodid_entry.insert(0,row[0])
    description_entry.insert(0,row[1])
    weight_entry.insert(0,row[2])
    length_entry.insert(0,row[3])
    width_entry.insert(0,row[4])
    height_entry.insert(0,row[5])

def select_truck_data(event,truckloadselection_entry):
    index=trucktreeview.selection()
    content=trucktreeview.item(index)
    row=content['values']
    clear(truckloadselection_entry,False)
    truckloadselection_entry.insert(0,row[0])
    

def clear(truckloadselection_entry,check):
    truckloadselection_entry.delete(0,END)
    if check:
        truck_treeview_data.selection_remove(truck_treeview_data.selection())


def clear_fields(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry,check):
    prodid_entry.delete(0,END)
    description_entry.delete(0,END)
    weight_entry.delete(0,END)
    length_entry.delete(0,END)
    width_entry.delete(0,END)
    height_entry.delete(0,END)
    if check:
        mainpagetreeview.selection_remove(mainpagetreeview.selection())

def add_to_load(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry):
    prodid=prodid_entry.get()
    description=description_entry.get()
    weight=weight_entry.get()
    length=length_entry.get()
    width=width_entry.get()
    height=height_entry.get()
    if (prodid=='' or description=='' or weight=='' or length=='' or width==''or height=='' ):
        messagebox.showerror('Error', 'All fields are required')
        return
    else:
       cursor,connection=connect_database()
       if not cursor or not connection:
           return
       try:
            cursor.execute('INSERT INTO truckload_data VALUES(NULL,%s,%s,%s,%s,%s,%s)',(prodid,description,weight,length,width,height))
            connection.commit()
            truck_treeview_data()
            get_total_weight()
            prodid_entry.delete(0,END)
            description_entry.delete(0,END)
            weight_entry.delete(0,END)
            length_entry.delete(0,END)
            width_entry.delete(0,END)
            height_entry.delete(0,END)
       except Exception as e:
               messagebox.showerror('Error',f'Error due to {e}')
       finally:
            cursor.close()
            connection.close()

def delete_selection(truckloadselection_entry):
    selection=truckloadselection_entry.get()
    if selection == '':
        messagebox.showerror('Error','please select a product')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
                return
        try:
                cursor.execute('DELETE from truckload_data WHERE rowid=%s',(selection))
                connection.commit()
                truck_treeview_data()
                truckloadselection_entry.delete(0,END)
        except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
        finally:
                cursor.close()
                connection.close()

def search(search_combobox, search_entry):
    combo=search_combobox.get()
    entry=search_entry.get()
    if combo == "Search By":
        messagebox.showerror('Error', 'No Option is selected')
    elif entry == '':
       messagebox.showerror('Error', 'Enter a value to search')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
                return
        try:
                cursor.execute(f"select * from product_data WHERE {combo} like '%{entry}%'")
                records=cursor.fetchall()
                mainpagetreeview.delete(*mainpagetreeview.get_children())
                for record in records:
                    mainpagetreeview.insert('',END,value=record)              
        except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
        finally:
                cursor.close()
                connection.close()

def showall(search_combobox,search_entry):
    ltreeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search By')

def clear_all():
     cursor,connection=connect_database()
     if not cursor or not connection:
                return
     try:
                cursor.execute('DROP TABLE truckload_data')
                cursor.execute('CREATE TABLE IF NOT EXISTS truckload_data(rowid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,prodid INT, description VARCHAR(255), weight INT, length INT, width INT, height INT)')
                connection.commit()
                truck_treeview_data()
         
     except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
     finally:
                cursor.close()
                connection.close()
     
def get_total_weight():
     cursor,connection=connect_database()
     if not cursor or not connection:
                return
     try:
                cursor.execute('SELECT SUM(weight) from truckload_data')
                weight=cursor.fetchall()
                connection.commit()
                return weight[0][0]
     except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
     finally:
                cursor.close()
                connection.close()

def get_total_length():
     cursor,connection=connect_database()
     if not cursor or not connection:
                return
     try:
                cursor.execute('SELECT SUM(length) from truckload_data')
                length=cursor.fetchall()
                connection.commit()
                return length[0][0]
     except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
     finally:
                cursor.close()
                connection.close()



def add_a_part(truck_bed_frame):
      cursor,connection = connect_database()
      if not cursor or not connection:
            return
      try:
            cursor.execute('SELECT * from truckload_data')
            response= cursor.fetchall()
            count=[]
            for record in response:
                rand_color=randomcolor.RandomColor()
                color=rand_color.generate()
                canvas=Canvas(truck_bed_frame,width=round(record[4]/5),height=round(record[5]/5), bd=0,bg=color)
                canvas.place(relx=.5,rely=.5, anchor=CENTER)
                canvas.grid(row=0,column=response.index(record))
                canvas.config(highlightthickness=0)
                
      except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}')
      finally:
            cursor.close()
            connection.close()

def load_form(Window):
    
   
    Total_weight=get_total_weight()
    Total_length=get_total_length()
    truck_image=ImageTk.PhotoImage(Image.open('semileft.png'))

    employee_frame=Frame(Window,width=1200,height=735)
    employee_frame.place(x=165, y=40)
    headingLabel=Label(employee_frame,text='Load Form',font=('Tahoma',20), bg='black', fg='white')
    headingLabel.place(x=0,y=0, relwidth=1)
    back_button=Button(employee_frame,text='Home',command=lambda: employee_frame.destroy())
    back_button.place(x=10, y=10)

    insideframe=Frame(employee_frame,width=1200,height=695)
    insideframe.place(x=0,y=40)

    search_frame = Frame(insideframe,height=40,width=800)
    search_frame.place(x=5,y=10)

    search_combobox= ttk.Combobox(search_frame,values=('ProdId', 'Description', 'Weight','Length','Width','Height'),font=('Tahoma',12), state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0,column=0,padx=20)

    search_entry=Entry(search_frame, font=('Tahoma',12),bg='lightyellow')
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text='SEARCH',font=('Tahoma', 12),width=10,cursor='hand2',command=lambda: search(search_combobox,search_entry))
    search_button.grid(row=0,column=2,padx=10)

    show_button=Button(search_frame,text='SHOW ALL',font=('Tahoma', 12),width=10,cursor='hand2',command=lambda: showall(search_combobox,search_entry))
    show_button.grid(row=0,column=3,padx=10)

    treeframe=Frame(insideframe,height=300,width=800)
    treeframe.place(x=5,y=45)

    vertical_scrollbar=Scrollbar(treeframe,orient=VERTICAL)

    global mainpagetreeview
    mainpagetreeview=ttk.Treeview(treeframe,columns=('prodid','description','weight','length','width','height'),show='headings',yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side=RIGHT,fill='y')
    vertical_scrollbar.config(command=mainpagetreeview.yview)
    mainpagetreeview.pack(pady=(10,0))

    mainpagetreeview.heading('prodid',text='ProdID')
    mainpagetreeview.heading('description',text='Description')
    mainpagetreeview.heading('weight',text='Weight(kg)')
    mainpagetreeview.heading('length',text='Length(mm)')
    mainpagetreeview.heading('width',text='Width(mm)')
    mainpagetreeview.heading('height',text='Height(mm)')

    mainpagetreeview.column('prodid', width=140)
    mainpagetreeview.column('description', width=140)
    mainpagetreeview.column('weight', width=140)
    mainpagetreeview.column('length', width=80)
    mainpagetreeview.column('width', width=80)
    mainpagetreeview.column('height', width=80)

    mainpagetreeview.bind('<ButtonRelease-1>',lambda event: select_data(event,prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry))

    detail_frame=Frame(insideframe,height=30,width=800)
    detail_frame.place(x=5,y=290)

    prodid_label=Label(detail_frame,text='ProdId',font=('Tahoma',10))
    prodid_label.grid(row=0,column=0,padx=5,pady=2,sticky='w')
    prodid_entry=Entry(detail_frame,font=('Tahoma',10),width=10,bg='lightyellow')
    prodid_entry.grid(row=0,column=1,padx=5,pady=2)

    description_label=Label(detail_frame,text='Description',font=('Tahoma',10))
    description_label.grid(row=0,column=2,padx=5,pady=2,sticky='w')
    description_entry=Entry(detail_frame,font=('Tahoma',10),width=20,bg='lightyellow')
    description_entry.grid(row=0,column=3,padx=5,pady=2)

    weight_label=Label(detail_frame,text='Weight',font=('Tahoma',10))
    weight_label.grid(row=0,column=4,padx=5,pady=2,sticky='w')
    weight_entry=Entry(detail_frame,font=('Tahoma',10), width=10,bg='lightyellow')
    weight_entry.grid(row=0,column=5,padx=5,pady=2)

    length_label=Label(detail_frame,text='Length',font=('Tahoma',10))
    length_label.grid(row=1,column=0,padx=5,pady=2,sticky='w')
    length_entry=Entry(detail_frame,font=('Tahoma',10),width=10,bg='lightyellow')
    length_entry.grid(row=1,column=1,padx=5,pady=2)

    width_label=Label(detail_frame,text='Width',font=('Tahoma',10))
    width_label.grid(row=1,column=2,padx=5,pady=2,sticky='w')
    width_entry=Entry(detail_frame,font=('Tahoma',10),width=10,bg='lightyellow')
    width_entry.grid(row=1,column=3,padx=5,pady=2)

    height_label=Label(detail_frame,text='Height',font=('Tahoma',10))
    height_label.grid(row=1,column=4,padx=5,pady=2,sticky='w')
    height_entry=Entry(detail_frame,font=('Tahoma',10), width=10,bg='lightyellow')
    height_entry.grid(row=1,column=5,padx=5,pady=2)

    add_button = Button(detail_frame,text='Add To Truck',font=('Tahoma',10),width=15,cursor='hand2',command=lambda: add_to_load(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry))
    add_button.grid(row=0,column=6,padx=8)

    insiderightframe=Frame(insideframe,width=480, height=330,bg='black')
    insiderightframe.place(x=710,y=30)

    truck_load_label=Label(insiderightframe,text='Truck Load List',font=('Tahoma bold',12),bg='black',fg='white')
    truck_load_label.pack()

    vertical_scrolltruck=Scrollbar(insiderightframe,orient=VERTICAL)

    global trucktreeview
    trucktreeview= ttk.Treeview(insiderightframe,columns=('rowid','prodid2','description2','weight2','length2','width2','height2'),show='headings',yscrollcommand=vertical_scrolltruck.set)
    vertical_scrolltruck.pack(side=RIGHT,fill='y')
    vertical_scrolltruck.config(command=trucktreeview.yview)
    trucktreeview.pack()

    trucktreeview.heading('rowid',text='row')
    trucktreeview.heading('prodid2',text='ProdID')
    trucktreeview.heading('description2',text='Descr')
    trucktreeview.heading('weight2',text='Weight')
    trucktreeview.heading('length2',text='Length')
    trucktreeview.heading('width2',text='Width')
    trucktreeview.heading('height2',text='Height')

    trucktreeview.column('rowid', width=40)
    trucktreeview.column('prodid2', width=60)
    trucktreeview.column('description2', width=100)
    trucktreeview.column('weight2', width=60)
    trucktreeview.column('length2', width=60)
    trucktreeview.column('width2', width=60)
    trucktreeview.column('height2', width=60)

    trucktreeview.bind('<ButtonRelease-1>',lambda event: select_truck_data(event,truckloadselection_entry))

    delete_frame=Frame(insiderightframe,bg='black')
    delete_frame.pack()

    truckloadselection_entry=Entry(delete_frame,font=('Tahoma',12), width=10,bg='lightyellow')
    truckloadselection_entry.grid(row=0,column=0,padx=5,pady=5)

    delete_button = Button(delete_frame,text='Delete',font=('Tahoma',12),width=10,cursor='hand2',command=lambda: delete_selection(truckloadselection_entry))
    delete_button.grid(row=0,column=1,padx=5,pady=5)

    clearall_button = Button(delete_frame,text='CA',font=('Tahoma',12),bg='black',fg='white',width=3,cursor='hand2',command=lambda: clear_all())
    clearall_button.grid(row=0,column=2,padx=5,pady=5)

    sum_button = Button(delete_frame,text='=',font=('Tahoma',12),width=3,cursor='hand2',command=lambda: load_form(Window))
    sum_button.grid(row=0,column=3,padx=5,pady=5)

    bottomframe=Frame(insideframe,width=1200, height=350,bg='gray63')
    bottomframe.place(x=0,y=350)

    bottom_left_frame=Frame(bottomframe,width=840, height=350,bg='gray63')
    bottom_left_frame.place(x=0,y=0)

    

    TruckImageLabel=Label(bottom_left_frame, image=truck_image)
    TruckImageLabel.image=truck_image
    TruckImageLabel.place(x=0,y=200)

    truck_bed_frame=Frame(bottom_left_frame,width=660, height=100,bg='white')
    truck_bed_frame.place(x=150,y=220)

    add_a_part(truck_bed_frame)

 

    bottom_right_frame=Frame(bottomframe,width=330, height=350,bg='gray63')
    bottom_right_frame.place(x=880,y=0)


    total_label=Label(bottom_right_frame,text='TOTAL PRODUCT WEIGHT',font=('Tahoma',12),bg='gray63')
    total_label.grid(row=0,column=0,padx=5,pady=5,sticky='w')

    total_label2=Label(bottom_right_frame,text=f'{Total_weight}',font=('Tahoma bold',14),bg='white')
    total_label2.grid(row=0,column=1,padx=5,pady=5,sticky='w')

    total_label3=Label(bottom_right_frame,text='kg',font=('Tahoma',12),bg='gray63')
    total_label3.grid(row=0,column=2,padx=5,pady=5,sticky='w')

    length_label=Label(bottom_right_frame,text='TOTAL LENGTH',font=('Tahoma',12),bg='gray63')
    length_label.grid(row=1,column=0,padx=5,pady=5,sticky='w')

    length_label2=Label(bottom_right_frame,text=f'{Total_length}',font=('Tahoma bold',14),bg='white')
    length_label2.grid(row=1,column=1,padx=5,pady=5,sticky='w')

    length_label3=Label(bottom_right_frame,text='mm',font=('Tahoma',12),bg='gray63')
    length_label3.grid(row=1,column=2,padx=5,pady=5,sticky='w')
   

    ltreeview_data()
    truck_treeview_data()

