import PySimpleGUI as sg
import sqlite3

sg.theme('LightBlue')

def sql_connection():
    return sqlite3.connect('userAccounts.db')

def login():
    layout = [
    [sg.Text('Console',font=('helvitica', 20), pad=((100, 0), 0))],
    [sg.T('', size=(10, 1))], 
    [sg.Text('Username',font=('helvitica', 16))],
    [sg.Input(size=(30, 1), font=('Helvetica', 14), text_color='white', key='-username-')],
    [sg.Text('Password',font=('helvitica', 16))],
    [sg.Input(size=(30, 1), font=('Helvetica', 14), text_color='white', key='-password-')],
    [sg.T('', size=(10, 1))], 
    [sg.Button('Login', size=(10,2),  pad=((100, 0), (5, 5)))],
    [sg.T('', size=(70, 1))],
    [sg.Text('New here? Sign up',font=('helvitica', 12),pad=((70, 0), 0), key='-signuplink-', enable_events=True)]]

    window = sg.Window('Login', layout, size=(500,500), margins=(100,100))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Login':
                
            with sql_connection() as conn:
                cursor = conn.cursor()

                username = values['-username-']
                password = values['-password-']

                search_query = "SELECT * FROM users WHERE username = ? AND password = ?"
                userfound = cursor.execute(search_query, (username, password)).fetchone()
                conn.commit()

                if username and password:
                    if userfound:
                        sg.popup("Logged in Successfully")
                        home()
                        window.close()
                    else:
                        sg.popup("User doesn't exist")
                else:
                    sg.popup("Fill all the details")

        elif event == '-signuplink-':
            signup()
            window.close()
        else:
            sg.popup_error('Some error')



def signup():

    layout = [
    [sg.Text('Console',font=('helvitica', 20), pad=((100, 0), 0))],
    [sg.T('', size=(10, 1))], 
    [sg.Text('Email Address',font=('helvitica', 16))],
    [sg.Input(size=(30, 1), font=('Helvetica', 14), text_color='white', key='-email-')],
    [sg.Text('Username',font=('helvitica', 16))],
    [sg.Input(size=(30, 1), font=('Helvetica', 14), text_color='white', key='-username-')],
    [sg.Text('Password',font=('helvitica', 16))],
    [sg.Input(size=(30, 1), font=('Helvetica', 14), text_color='white', key='-password-')],
    [sg.Text('Confirm Password',font=('helvitica', 16))],
    [sg.Input(size=(30, 1), font=('Helvetica', 14), text_color='white', key='-confirmpassword-')],
    [sg.T('', size=(10, 1))],
    [sg.Button('Signup', size=(10,2),  pad=((100, 0), (5, 5)))],
    [sg.T('', size=(10, 1))],
    [sg.Text('Already have an account? Login',font=('helvitica', 12),pad=((30, 0), 0), key='-loginlink-', enable_events=True)]]


    window = sg.Window('Signup', layout, size=(500,500), margins=(100,30))


    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Signup':
            with sql_connection() as conn:
                cursor = conn.cursor()

                create_table = '''
                        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, username TEXT, password TEXT)       
                '''
                cursor.execute(create_table)
                conn.commit()

                email = values['-email-']
                username = values['-username-']
                password = values['-password-']
                confirmpassword = values['-confirmpassword-']
                if email and username and password and confirmpassword:
                    if password == confirmpassword:
                        cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, confirmpassword))
                        sg.popup("Account Created Successfully")
                        conn.commit()
                        login()
                    else:
                        sg.popup("Passwords doesn't match")
                else:
                    sg.popup('Fill all the details')
        elif event == '-loginlink-':
            login()
        else:
            sg.popup_error('Some Error')

    window.close()

def home():
    layout = [
    [sg.Text('Welcome to our Console!',font=('helvitica', 20), pad=((220, 0), (5, 5)))],
    [sg.T('', size=(10, 1))], 
    [sg.Button('Logout', size=(10,2),  pad=((330, 0), (5, 5)))],
    [sg.T('', size=(70, 1))]]

    window = sg.Window('Login', layout, size=(1000,500), margins=(100,100))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Logout':
            window.close()
            login()

        else:
            sg.popup_error('Some error')

    window.close()


signup()
