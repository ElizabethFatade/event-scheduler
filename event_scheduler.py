from tkinter import *
import sqlite3
from datetime import datetime
import pytz

root = Tk()
root.title("Create an Event")
root.geometry("450x600")

# Create a database or connect to one
conn = sqlite3.connect('events_book.db')

# Create Cursor
c = conn.cursor()

# Commit Changes
conn.commit()

# Create Table
command1 = 'CREATE TABLE events(event_name text, day integer, month integer, year integer, ' \
           'start_time string, end_time string)'
# c.execute(command1)

# Gets the local Eastern Time in America
tz_east = pytz.timezone('America/New_York')
datetime_east = datetime.now(tz_east)

# This is the current time & AM period
hr = datetime_east.strftime("%I")
min = datetime_east.strftime("%M")
period = datetime_east.strftime("%p")


# CREATE A QUERY FUNCTION
def query():
    # Create a database or connect to one
    conn = sqlite3.connect('events_book.db')
    # Create Cursor
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM events")
    events = c.fetchall()

    # Loop through Records
    print_events = ''
    for event in events:
        print_events += str(event[0]) + ", " + str(event[2]) + "/" + str(event[1]) + "/" + str(event[3]) + \
                        '\t' + str(event[6]) + '\n'
    query_label = Label(root, text=print_events)
    query_label.grid(row=12, column=0, columnspan=2)

    # Commit Changes
    conn.commit()
    # Close Connection
    conn.close()


# CREATE A SUBMIT FUNCTION FOR DATABASE
def submit():
    # Create a database or connect to one
    conn = sqlite3.connect('events_book.db')
    # Create Cursor
    c = conn.cursor()

    # Insert into Table
    c.execute("INSERT INTO events VALUES (:event_name, :day, :month, :year, :start_time, :end_time)",
    {
        'event_name': event_name.get(),
        'day': day.get(),
        'month': month.get(),
        'year': year.get(),
        'start_time': start_time.get(),
        'end_time': end_time.get()
    })

    # Commit Changes
    conn.commit()
    # Close Connection
    conn.close()

    # Clear the text Boxes
    event_name.delete(0, END)
    day.delete(0, END)
    month.delete(0, END)
    year.delete(0, END)
    start_time.delete(0, END)
    end_time.delete(0, END)

# CREATE A DELETE FUNCTION TO DELETE A RECORD
def delete():
    # Create a database or connect to one
    conn = sqlite3.connect('events_book.db')
    # Create Cursor
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE FROM events WHERE oid = " + delete_box.get())
    delete_box.delete(0, END)

    # Commit Changes
    conn.commit()
    # Close Connection
    conn.close()


# CREATE AN SAVE FUNCTION
def save():
    # Create a database or connect to one
    conn = sqlite3.connect('events_book.db')
    # Create Cursor
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("""UPDATE events SET
        event_name = :event,
        day = :day,
        month = :month,
        year = :year,
        start_time = :start_time,
        end_time = :end_time
        
        WHERE oid = :oid""",
              {
                  'event': event_name_edit.get(),
                  'day': day_edit.get(),
                  'month': month_edit.get(),
                  'year': year_edit.get(),
                  'start_time': start_time_edit.get(),
                  'end_time': end_time_edit.get(),

                  'oid': record_id
              })

    # Commit Changes
    conn.commit()
    # Close Connection
    conn.close()

    # Close the new window after updating
    editor.destroy()


# CREATE AN EDIT FUNCTION TO EDIT A RECORD
def edit():
    global editor
    editor = Tk()
    editor.title("Edit a Record")
    editor.geometry("450x240")

    # Create a database or connect to one
    conn = sqlite3.connect('events_book.db')
    # Create Cursor
    c = conn.cursor()

    record_id = delete_box.get()
    # Query the database
    c.execute("SELECT * FROM events WHERE oid = " + record_id)
    records = c.fetchall()

    # Create Global Variables for Text Box names
    global event_name_edit
    global day_edit
    global month_edit
    global year_edit
    global start_time_edit
    global end_time_edit

    # Create entry boxes/widgets
    event_name_edit = Entry(editor, width=25)
    event_name_edit.grid(row=0, column=1, pady=(10, 0))
    day_edit = Entry(editor, width=25)
    day_edit.grid(row=1, column=1)
    month_edit = Entry(editor, width=25)
    month_edit.grid(row=2, column=1)
    year_edit = Entry(editor, width=25)
    year_edit.grid(row=3, column=1)
    start_time_edit = Entry(editor, width=25)
    start_time_edit.grid(row=4, column=1)
    end_time_edit = Entry(editor, width=25)
    end_time_edit.grid(row=5, column=1)

    # Create entry box labels
    event_name_label = Label(editor, text="Event Name")
    event_name_label.grid(row=0, column=0, pady=(10, 0))
    day_label = Label(editor, text="Day")
    day_label.grid(row=1, column=0)
    month_label = Label(editor, text="Month")
    month_label.grid(row=2, column=0)
    year_label = Label(editor, text="Year")
    year_label.grid(row=3, column=0)
    start_time_label = Label(editor, text="Start Time (hr:min AM/PM)")
    start_time_label.grid(row=4, column=0)
    end_time_label = Label(editor, text="End Time (hr:min AM/PM)")
    end_time_label.grid(row=5, column=0)

    # Loop through Records
    for record in records:
        event_name_edit.insert(0, record[0])
        day_edit.insert(0, record[1])
        month_edit.insert(0, record[2])
        year_edit.insert(0, record[3])
        start_time_edit.insert(0, record[4])
        end_time_edit.insert(0, record[5])

    # CREATE A SAVE BUTTON TO SAVE EDITED RECORD
    buttons(editor, "Save", save, 6, 0, 132)


# Deals with the different buttons on the GUI surface
def buttons(window, string, comm, r, c, i_padx):
    button = Button(window, text = string, command = comm)
    button.grid(row = r, column = c, columnspan = 2, pady = 10, padx = 10, ipadx = i_padx)


# Create entry boxes/widgets
event_name = Entry(root, width = 25)
event_name.grid(row = 0, column = 1, pady = (10, 0))
day = Entry(root, width = 25)
day.grid(row = 1, column = 1)
month = Entry(root, width = 25)
month.grid(row = 2, column = 1)
year = Entry(root, width = 25)
year.grid(row = 3, column = 1)
start_time = Entry(root, width = 25)
start_time.insert(0, hr + ":" + min + " " + period)
start_time.grid(row = 4, column = 1)
end_time = Entry(root, width = 25)
end_time.insert(0, hr + ":" + min + " " + period)
end_time.grid(row = 5, column = 1)


delete_box = Entry(root, width = 25)
delete_box.grid(row = 9, column = 1, pady = 5)

# Create entry box labels
event_name_label = Label(root, text = "Event Name")
event_name_label.grid(row = 0, column = 0, pady = (10, 0))
day_label = Label(root, text = "Day")
day_label.grid(row = 1, column = 0)
month_label = Label(root, text = "Month")
month_label.grid(row = 2, column = 0)
year_label = Label(root, text = "Year")
year_label.grid(row = 3, column = 0)
start_time_label = Label(root, text = "Start Time (hr:min AM/PM)")
start_time_label.grid(row = 4, column = 0)
end_time_label = Label(root, text = "End Time (hr:min AM/PM)")
end_time_label.grid(row = 5, column = 0)

delete_box_label = Label(root, text = "Select   ID")
delete_box_label.grid(row = 9, column = 0, pady = 5)


# Create Submit Button
buttons(root, "Add Event to Calendar", submit, 6, 0, 100)

# Create a Query Button
buttons(root, "Show Events", query, 7, 0, 132)

# Create a Delete Button
buttons(root, "Delete Record", delete, 10, 0, 127)

# Create an Edit Button
buttons(root, "Edit Record", edit, 11, 0, 136)

# Close Connection
conn.close()

root.mainloop()
