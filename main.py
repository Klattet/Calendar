import calendar, datetime
from tkinter import *

today = datetime.datetime.now()

weekday_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

days_in_month = [datetime.date(today.year, today.month, day) for day in range(1, calendar.monthrange(today.year, today.month)[1]+1)]

main_window = Tk()
main_window.minsize(width = 700, height = 500)
main_window.title("Calendar")

Grid.rowconfigure(main_window, 0, weight=1)
Grid.columnconfigure(main_window, 0, weight=1)

frame = Frame(main_window)
frame.grid(row = 0, column = 0, sticky = NSEW)

for r in range(8):
    Grid.rowconfigure(frame, r, weight = 1)
    for c in range(7):
        Grid.columnconfigure(frame, c, weight = 1)
        Button(frame).grid(row = r, column = c, sticky = NSEW)


def create_squares(d_i_m):

    # Clear grid
    for square in frame.grid_slaves():
        square.grid_forget()

    # Make last month button
    past_frame = Frame(frame)
    past_frame.grid(row = 0, column = 0, sticky = NSEW)
    Button(past_frame, text = "Last Month", command = lambda: refresh_past(d_i_m), relief = RAISED, width = 10, height = 1).place(relx=0.5, rely=0.5, anchor=CENTER)

    # Make next month button
    future_frame = Frame(frame)
    future_frame.grid(row = 0, column = 3, sticky = NSEW)
    Button(future_frame, text = "Next Month", command = lambda: refresh_future(d_i_m), relief = RAISED, width = 10, height = 1).place(relx=0.5, rely=0.5, anchor=CENTER)

    # Make month name label
    Label(frame, text = f"{month_list[d_i_m[0].month - 1]}, {d_i_m[0].year}").grid(row = 0, column = 1, columnspan = 2, sticky = NSEW)

    # Make search field
    entry_frame = Frame(frame)
    entry_frame.grid(row = 0, column = 5, columnspan = 2, sticky = NSEW)
    Label(entry_frame, text = "Year").grid(row = 0, sticky = NSEW)
    Label(entry_frame, text = "Month").grid(row = 1, sticky = NSEW)
    year_entry = Entry(entry_frame)
    year_entry.grid(row = 0, column = 1, sticky = NSEW)
    month_entry = Entry(entry_frame)
    month_entry.grid(row = 1, column = 1, sticky = NSEW)
    Button(entry_frame, text = "Search", relief = RAISED, command = lambda: refresh_search(year_entry.get() if year_entry.get() else d_i_m[0].year, month_entry.get() if month_entry.get() else d_i_m[0].month)).grid(row = 2, column = 1, sticky = NSEW)

    # Make weekday row
    for weekday in weekday_list:
        Button(frame, text = weekday, bg = "red", disabledforeground = "white", relief = RIDGE, state = DISABLED, width = 15, height = 1).grid(row = 1, column = weekday_list.index(weekday), sticky = NSEW)

    # Make blank squares top
    for i in range(d_i_m[0].weekday()):
        Button(frame, state = DISABLED, relief = RIDGE, height = 3).grid(row = 2, column = i, sticky = NSEW)

    # Make blank squares bottom
    for i in range(14 + d_i_m[0].weekday() + len(d_i_m), 56):
        Button(frame, state = DISABLED, relief = RIDGE, height = 3).grid(row = int(i / 7), column = i % 7, sticky = NSEW)

    # Make occupied squares
    for day in d_i_m:
        if day == today.date():
            Button(frame, text = day.day, background = "azure3", relief = RIDGE, height = 3).grid(row = int((6 - day.weekday() + day.day) / 7.01) + 2, column = day.weekday(), sticky = NSEW)
        else:
            Button(frame, text = day.day, relief = RIDGE, height = 3).grid(row = int((6 - day.weekday() + day.day) / 7.01) + 2, column = day.weekday(), sticky = NSEW)

# Refresh grid to next month
def refresh_future(d_i_m):
    new_month = d_i_m[0].month + 1
    new_year = d_i_m[0].year
    if new_month > 12:
        new_month = 1
        new_year = new_year + 1
    
    global days_in_month
    days_in_month = [datetime.date(new_year, new_month, day) for day in range(1, calendar.monthrange(new_year, new_month)[1]+1)]
    
    create_squares(days_in_month)

# Refresh grid to last month
def refresh_past(d_i_m):
    new_month = d_i_m[0].month - 1
    new_year = d_i_m[0].year
    if new_month < 1:
        new_month = 12
        new_year = new_year - 1

    global days_in_month
    days_in_month = [datetime.date(new_year, new_month, day) for day in range(1, calendar.monthrange(new_year, new_month)[1] + 1)]

    create_squares(days_in_month)

# Refresh grid to provided month
def refresh_search(year_arg, month_arg):
    if not str(year_arg).isdigit() or not str(month_arg).isdigit(): return
    if not 0 < int(year_arg) < 10000: return
    if not 0 < int(month_arg) < 13: return

    global days_in_month
    days_in_month = [datetime.date(int(year_arg), int(month_arg), day) for day in range(1, calendar.monthrange(int(year_arg), int(month_arg))[1]+1)]

    create_squares(days_in_month)

# Start on current month
create_squares(days_in_month)

main_window.mainloop()
