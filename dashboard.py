from tkinter import *
from tkinter import ttk
from loadpage import load_form
import pymysql
from tkinter import messagebox

def connect_database():
    try:
        connection=pymysql.connect(host='localhost', user='root',password='1234')
        cursor=connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connectivity issue. Open MYSQL command line client')
        return None,None
    cursor.execute('CREATE DATABASE IF NOT EXISTS Product_loading')
    cursor.execute('USE product_loading')
    cursor.execute('CREATE TABLE IF NOT EXISTS product_data(prodid INT PRIMARY KEY, description VARCHAR(255), weight INT, length INT, width INT,height INT)')
    return cursor,connection
  


def treeview_data():
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


def add_info(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry):
    prodid=prodid_entry.get()
    description=description_entry.get()
    weight=weight_entry.get()
    height=height_entry.get()
    width= width_entry.get()
    length=length_entry.get()
    if (prodid=='' or description=='' or weight=='' or height=='' or width==''or length==''):
        messagebox.showerror('Error', 'All fields are required')
        return
    else:
       cursor,connection=connect_database()
       if not cursor or not connection:
           return
       try:
            cursor.execute('INSERT INTO product_data VALUES(%s,%s,%s,%s,%s,%s)',(prodid,description,weight,length,width,height))
            connection.commit()
            treeview_data() 
            messagebox.showinfo('Success', 'Data added')
            prodid_entry.delete(0,END)
            description_entry.delete(0,END)
            weight_entry.delete(0,END)
            height_entry.delete(0,END)
            width_entry.delete(0,END)
            length_entry.delete(0,END)
       except Exception as e:
               messagebox.showerror('Error',f'Error due to {e}')
       finally:
            cursor.close()
            connection.close()
           
def update_info(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry):
    prodid=prodid_entry.get()
    description=description_entry.get()
    weight=weight_entry.get()
    height=height_entry.get()
    width= width_entry.get()
    length=length_entry.get()
    selected=mainpagetreeview.selection()
    if not selected:
        messagebox.error('Error', 'No row is selected')
    else:
         if (prodid=='' or description=='' or weight=='' or height=='' or width=='' or length==''):
             messagebox.showerror('Error', 'All fields are required')
             return
         else:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return
            else:
                try:
                    cursor.execute('UPDATE product_data SET description=%s, weight=%s, length=%s, width=%s,height=%s WHERE prodid=%s',(description,weight,length,width,height,prodid))
                    connection.commit()
                    messagebox.showinfo('Success','Update successful')
                    treeview_data()
                    prodid_entry.delete(0,END)
                    description_entry.delete(0,END)
                    weight_entry.delete(0,END)
                    height_entry.delete(0,END)
                    width_entry.delete(0,END)
                    length_entry.delete(0,END)
                except Exception as e:
                       messagebox.showerror('Error',f'Error due to {e}')
                finally:
                        cursor.close()
                        connection.close()


def delete_info(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry):
    prodid=prodid_entry.get()
    selected=mainpagetreeview.selection()
    if not selected:
        messagebox.showerror('Error','Nothing is selected')
    else:
        result=messagebox.askyesno('Confirm','Do you really want to delete the record')
        if result:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('DELETE from product_data WHERE prodid=%s',(prodid))
                connection.commit()
                treeview_data()
                messagebox.showinfo('Success', 'Record is deleted')
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
       

def clear_fields(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry,check):
    prodid_entry.delete(0,END)
    description_entry.delete(0,END)
    weight_entry.delete(0,END)
    length_entry.delete(0,END)
    width_entry.delete(0,END)
    height_entry.delete(0,END)
    if check:
        mainpagetreeview.selection_remove(mainpagetreeview.selection())

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
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search By')





Window=Tk()
Window.wm_attributes('-transparentcolor','#ab23ff')
Window.title('Berkel Loading APP')
Window.geometry('1370x788')
Window.resizable(0,0)
Window.config(bg='white')




b_image=PhotoImage(file='berkle.png')


titleLabel=Label(Window,compound=LEFT,text=' Loading Management System',font=('Tahoma',20),bg='black',fg='red', anchor='w', padx='10')
titleLabel.place(x=0,y=0,relwidth=1)

leftFrame=Frame(Window)
leftFrame.place(x=0,y=70, width=155, height=555)

ImageLabel=Label(leftFrame, image=b_image)
ImageLabel.pack()

menuLabel=Label(leftFrame,text='Menu',font=('tahoma',20),bg='gray')
menuLabel.pack(fill=X)

page1_button=Button(leftFrame,text='Load Page',font=('tahoma',20),command=lambda: load_form(Window))
page1_button.pack(fill=X)

rightmainframe=Frame(Window, width=1050, height=587,bg='white')
rightmainframe.place(x=210,y=60)

topFrame=Frame(rightmainframe,height=235,bg='white')
topFrame.place(x=0,y=0,relwidth=1)


search_frame = Frame(topFrame,bg='white')
search_frame.pack()

search_combobox= ttk.Combobox(search_frame,values=('ProdId', 'Description', 'Weight','Length','Width','Height'),font=('Tahoma',12), state='readonly')
search_combobox.set('Search By')
search_combobox.grid(row=0,column=0,padx=20)

search_entry=Entry(search_frame, font=('Tahoma',12),bg='lightyellow')
search_entry.grid(row=0,column=1)

search_button=Button(search_frame,text='SEARCH',font=('Tahoma', 12),width=10,cursor='hand2',command=lambda: search(search_combobox,search_entry))
search_button.grid(row=0,column=2,padx=20)

show_button=Button(search_frame,text='SHOW ALL',font=('Tahoma', 12),width=10,cursor='hand2',command=lambda: showall(search_combobox,search_entry))
show_button.grid(row=0,column=3,padx=20)

vertical_scrollbar=Scrollbar(topFrame,orient=VERTICAL)

mainpagetreeview=ttk.Treeview(topFrame,columns=('prodid','description','weight','length','width','height'),show='headings',yscrollcommand=vertical_scrollbar.set)
vertical_scrollbar.pack(side=RIGHT,fill='y')
vertical_scrollbar.config(command=mainpagetreeview.yview)
mainpagetreeview.pack(pady=(10,0))

mainpagetreeview.heading('prodid',text='ProdID')
mainpagetreeview.heading('description',text='Description')
mainpagetreeview.heading('weight',text='Weight(kg)')
mainpagetreeview.heading('length',text='Length(mm)')
mainpagetreeview.heading('width',text='Width(mm)')
mainpagetreeview.heading('height',text='Height(mm)')

mainpagetreeview.column('prodid', width=160)
mainpagetreeview.column('description', width=160)
mainpagetreeview.column('weight', width=160)
mainpagetreeview.column('length', width=160)
mainpagetreeview.column('width', width=160)
mainpagetreeview.column('height', width=160)

mainpagetreeview.bind('<ButtonRelease-1>',lambda event: select_data(event,prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry))

detail_frame=Frame(rightmainframe)
detail_frame.place(x=0,y=270,relwidth=1)

prodid_label=Label(detail_frame,text='ProdId',font=('Tahoma',12))
prodid_label.grid(row=0,column=0,padx=20,pady=10,sticky='w')
prodid_entry=Entry(detail_frame,font=('Tahoma',12),bg='lightyellow')
prodid_entry.grid(row=0,column=1,padx=20,pady=10)

description_label=Label(detail_frame,text='Description',font=('Tahoma',12))
description_label.grid(row=0,column=2,padx=20,pady=10,sticky='w')
description_entry=Entry(detail_frame,font=('Tahoma',12),bg='lightyellow')
description_entry.grid(row=0,column=3,padx=20,pady=10)

weight_label=Label(detail_frame,text='Weight',font=('Tahoma',12))
weight_label.grid(row=0,column=4,padx=20,pady=10,sticky='w')
weight_entry=Entry(detail_frame,font=('Tahoma',12),bg='lightyellow')
weight_entry.grid(row=0,column=5,padx=20,pady=10)

length_label=Label(detail_frame,text='Length',font=('Tahoma',12))
length_label.grid(row=1,column=0,padx=20,pady=10,sticky='w')
length_entry=Entry(detail_frame,font=('Tahoma',12),bg='lightyellow')
length_entry.grid(row=1,column=1,padx=20,pady=10)

width_label=Label(detail_frame,text='Width',font=('Tahoma',12))
width_label.grid(row=1,column=2,padx=20,pady=10,sticky='w')
width_entry=Entry(detail_frame,font=('Tahoma',12),bg='lightyellow')
width_entry.grid(row=1,column=3,padx=20,pady=10)

height_label=Label(detail_frame,text='Height',font=('Tahoma',12))
height_label.grid(row=1,column=4,padx=20,pady=10,sticky='w')
height_entry=Entry(detail_frame,font=('Tahoma',12),bg='lightyellow')
height_entry.grid(row=1,column=5,padx=20,pady=10)


bottomframe=Frame(rightmainframe,bg='white')
bottomframe.place(x=200,y=500)

add_button = Button(bottomframe,text='Add',font=('Tahoma',12),width=10,cursor='hand2',command=lambda: add_info(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry))
add_button.grid(row=0,column=0,padx=20)

update_button = Button(bottomframe,text='Update',font=('Tahoma',12),width=10,cursor='hand2', command=lambda: update_info(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry))
update_button.grid(row=0,column=1,padx=20)

delete_button = Button(bottomframe,text='Delete',font=('Tahoma',12),width=10,cursor='hand2',command=lambda: delete_info(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry))
delete_button.grid(row=0,column=2,padx=20)

clear_button = Button(bottomframe,text='Clear',font=('Tahoma',12),width=10,cursor='hand2', command=lambda: clear_fields(prodid_entry, description_entry,weight_entry,length_entry,width_entry,height_entry,True))
clear_button.grid(row=0,column=3,padx=20)

treeview_data()

Window.mainloop()


#topframe is the main frame for the main page.