#!/usr/bin/env python3
"""
DeviceManagement Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import datetime
from typing import List, Optional

import setup_vendor_path  # noqa
import pg8000

################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 9 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None
    except pg8000.ProgrammingError as e:
        print("""Error, config file incorrect: check your password and username""")
        print(e)
        return None
    except Exception as e:
        print(e)
        return None

    # return the connection to use
    return connection


#####################################################
#   Query (a + a[i])
#   Login
#####################################################

def check_login(employee_id, password: str) -> Optional[dict]:
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
	
	# Note: this example system is not well-designed for security.
	# There are several serious problems. One is that the database
	# stores passwords directly; a better design would "salt" each password
	# and then hash the result, and store only the hash.
	# Also, we are not doing anything to prevent sql injection in this code.
	# This is ok for a toy assignment, but do not use this code as a model when you are
	# writing a real system for a client or yourself.

    # TODO
    # Check if the user details are correct!
    # Return the relevant information (watch the order!)

    # TODO Dummy data - change rows to be useful!
    # NOTE: Make sure you take care of ORDER!!!
	
    '''
    employee_info = [
        1337,                       # empid
        'Porter Tato Head',         # name
        '123 Fake Street',          # homeAddress
        datetime.date(1970, 1, 1),  # dateOfBirth
    ]

    user = {
        'empid': employee_info[0],
        'name': employee_info[1],
        'homeAddress': employee_info[2],
        'dateOfBirth': employee_info[3],
    }

    return user
    '''

    # Ask for the database connection, and get the cursor set up
    conn = database_connect()
    if(conn is None):
        return None

    cur = conn.cursor()
    result = None

    try:
        # Try executing the SQL and get from the database
        sql = """SELECT *
                 FROM public.employee
                 WHERE empid=%s AND password=%s"""
        cur.execute(sql, (employee_id, password))
        sql_result = cur.fetchone()              # Fetch the first row

        result = {
        'empid': sql_result[0],
        'name': sql_result[1],
        'homeAddress': sql_result[2],
        'dateOfBirth': sql_result[3],
        }

    except Exception as e:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
        print(e)

    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return result



#####################################################
#   Query (f[i])
#   Is Manager?
#####################################################

def is_manager(employee_id: int) -> Optional[str]:
    """
    Get the department the employee is a manager of, if any.
    Returns None if the employee doesn't manage a department.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of departments
    '''
    manager_of = 'RND'

    return manager_of
    '''
     # Get the database connection and set up the cursor
    conn = database_connect()
    if(conn is None):
        return None
    # Sets up the rows as a dictionary
    cur = conn.cursor()
    val = None
    try:
        # Try getting all the information returned from the query
        # NOTE: column ordering is IMPORTANT
        cur.execute("""
                        SELECT name
                        FROM public.department
                        WHERE manager = %s""", [employee_id])
        sql_result = cur.fetchall()

        if len(sql_result) == 0:
            pass
        else:
            val = str(sql_result)

    except Exception as e:
        # If there were any errors, we print something nice and return a NULL value
        print("Error fetching from database")
        print(e)

    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return val



#####################################################
#   Query (a[ii])
#   Get My Used Devices
#####################################################

def get_devices_used_by(employee_id: int) -> list:
    """
    Get a list of all the devices used by the employee.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of devices issued to the user!
    # Each "Row" contains [ deviceID, manufacturer, modelNumber]
    # If no devices = empty list []
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    devices = []
    try:
    	cur.execute("""SELECT D.deviceId, D.manufacturer, D.modelNumber 
    		FROM DeviceUsedBy DU JOIN Device D USING(deviceID) 
    		WHERE DU.empid = %s""",[employee_id])
    	res = cur.fetchall()
    	if len(res) == 0:
    		pass
    	else:
    		devices = res
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    devices = [
        [7, 'Zava', '1146805551'],
        [13, 'Skyndu', '5296853075'],
        [24, 'Yakitri', '8406089423'],
    ]
    '''

    return devices


#####################################################
#   Query (a[iii])
#   Get departments employee works in
#####################################################

def employee_works_in(employee_id: int) -> List[str]:
    """
    Return the departments that the employee works in.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of departments
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    departments = []
    try:
    	cur.execute("""SELECT department 
    		FROM public.EmployeeDepartments 
    		WHERE empID = %s""",[employee_id])
    	res = cur.fetchall()
    	if len(res) == 0:
    		pass
    	else:
    		departments = res
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    departments = ['IT', 'Marketing']
    '''

    return departments


#####################################################
#   Query (c)
#   Get My Issued Devices
#####################################################

def get_issued_devices_for_user(employee_id: int) -> list:
    """
    Get all devices issued to the user.
        - Return a list of all devices to the user.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of devices issued to the user!
    # Each "Row" contains [ deviceID, purchaseDate, manufacturer, modelNumber ]
    # If no devices = empty list []
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    devices = []
    cur.execute("""SELECT deviceId,purchaseDate,manufacturer,modelNumber 
    	FROM public.Device 
    	WHERE issuedto = %s""",[employee_id])
    res = cur.fetchall()
    if len(res) == 0:
    	pass
    else:
    	devices = res
    cur.close()
    conn.close()

    '''
    devices = [
        [7, datetime.date(2017, 8, 28), 'Zava', '1146805551'],
        [8, datetime.date(2017, 9, 22), 'Topicware', '5798231046'],
        [6123, datetime.date(2017, 9, 5), 'Dabshots', '6481799600'],
        [1373, datetime.date(2018, 4, 19), 'Cogibox', '6700815444'],
        [8, datetime.date(2018, 2, 10), 'Feednation', '2050267274'],
        [36, datetime.date(2017, 11, 5), 'Muxo', '8768929463'],
        [17, datetime.date(2018, 1, 14), 'Izio', '5886976558'],
        [13, datetime.date(2017, 9, 8), 'Skyndu', '5296853075'],
        [24, datetime.date(2017, 10, 22), 'Yakitri', '8406089423'],
    ]
    '''
    return devices


#####################################################
#   Query (b)
#   Get All Models
#####################################################

def get_all_models() -> list:
    """
    Get all models available.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the list of models with information from the model table.
    # Each "Row" contains: [manufacturer, description, modelnumber, weight]
    # If No Models = EMPTY LIST []
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    models = []
    try:
    	cur.execute("""SELECT * FROM public.Model""")
    	res = cur.fetchall()
    	if len(res) == 0:
    		pass
    	else:
    		models = res
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    models = [
        ['Feednation', 'Expanded didactic instruction set', '2050267274', 31],
        ['Zoombox', 'Profit-focused global extranet', '8860068207', 57],
        ['Shufflebeat', 'Robust clear-thinking functionalities', '0288809602', 23],
        ['Voonyx', 'Vision-oriented bandwidth-monitored instruction set', '5275001460', 82],
        ['Tagpad', 'Fundamental human-resource migration', '3772470904', 89],
        ['Wordpedia', 'Business-focused tertiary orchestration', '0211912271', 17],
        ['Skyndu', 'Quality-focused web-enabled parallelism', '5296853075', 93],
        ['Tazz', 'Re-engineered well-modulated contingency', '8479884797', 95],
        ['Dabshots', 'Centralized empowering protocol', '6481799600', 68],
        ['Rhybox', 'Re-contextualized bifurcated orchestration', '7107712551', 25],
        ['Cogibox', 'Networked disintermediate application', '6700815444', 27],
        ['Meedoo', 'Progressive 24-7 orchestration', '3998544224', 43],
        ['Zoomzone', 'Reverse-engineered systemic monitoring', '9854941272', 50],
        ['Meejo', 'Secured static implementation', '3488947459', 75],
        ['Topicware', 'Extended system-worthy forecast', '5798231046', 100],
        ['Izio', 'Open-source static productivity', '5886976558', 53],
        ['Zava', 'Polarised incremental paradigm', '1146805551', 82],
        ['Demizz', 'Reduced hybrid website', '9510770736', 63],
        ['Muxo', 'Switchable contextually-based throughput', '8768929463', 40],
        ['Wordify', 'Front-line fault-tolerant middleware', '8465785368', 84],
        ['Twinder', 'Intuitive contextually-based local area network', '5709369365', 78],
        ['Jatri', 'Horizontal disintermediate workforce', '8271780565', 31],
        ['Chatterbridge', 'Phased zero tolerance architecture', '8429506128', 39],
    ]
    '''
    return models


#####################################################
#   Query (d[ii])
#   Get Device Repairs
#####################################################

def get_device_repairs(device_id: int) -> list:
    """
    Get all repairs made to a device.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the repairs done to a certain device
    # Each "Row" contains:
    #       - repairid
    #       - faultreport
    #       - startdate
    #       - enddate
    #       - cost
    # If no repairs = empty list
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    repairs = []
    try:
    	cur.execute("""SELECT repairID, faultreport, startdate, enddate,cost 
    		FROM public.Repair 
    		WHERE doneTo = %s""",[device_id])
    	res = cur.fetchall()
    	if len(res) == 0:
    		pass
    	else:
    		repairs = res
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    repairs = [
        [17, 'Never, The', datetime.date(2018, 7, 16), datetime.date(2018, 9, 22), '$837.13'],
        [18, 'Gonna', datetime.date(2018, 8, 3), datetime.date(2018, 9, 22), '$1726.99'],
        [19, 'Give', datetime.date(2018, 9, 4), datetime.date(2018, 9, 17), '$1751.01'],
        [20, 'You', datetime.date(2018, 7, 21), datetime.date(2018, 9, 23), '$1496.36'],
        [21, 'Up', datetime.date(2018, 8, 17), datetime.date(2018, 9, 18), '$1133.88'],
        [22, 'Never', datetime.date(2018, 8, 8), datetime.date(2018, 9, 24), '$1520.95'],
        [23, 'Gonna', datetime.date(2018, 9, 1), datetime.date(2018, 9, 29), '$611.09'],
        [24, 'Let', datetime.date(2018, 7, 5), datetime.date(2018, 9, 15), '$1736.03'],
    ]
    '''
    return repairs


#####################################################
#   Query (d[i])
#   Get Device Info
#####################################################

def get_device_information(device_id: int) -> Optional[dict]:
    """
    Get related device information in detail.
    """

    # TODO Dummy Data - Change to be useful!
    # Return all the relevant device information for the device
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    device = []
    try:
    	cur.execute("""SELECT * 
    		FROM public.Device 
    		WHERE deviceid = %s""",[device_id])
    	device_info = cur.fetchone()
    	if len(device_info) == 0:
    		pass
    	else:
    		device = {'device_id': device_info[0],'serial_number': device_info[1],'purchase_date': device_info[2],'purchase_cost': device_info[3],
    		'manufacturer': device_info[4],'model_number': device_info[5],'issued_to': device_info[6],
    }
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    device_info = [
        1,                      # DeviceID
        '2721153188',           # SerialNumber
        datetime.date(2017, 12, 19),  # PurchaseDate
        '$1009.10',             # PurchaseCost
        'Zoomzone',             # Manufacturer
        '9854941272',           # ModelNumber
        1337,                   # IssuedTo
    ]
    '''
    return device


#####################################################
#   Query (d[iii/iv])
#   Get Model Info by Device
#####################################################

def get_device_model(device_id: int) -> Optional[dict]:
    """
    Get model information about a device.
    """

    # TODO Dummy Data - Change to be useful!
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    model = []
    try:
    	cur.execute("""SELECT * 
    		FROM public.Model
    		WHERE manufacturer = (SELECT manufacturer FROM public.Device WHERE deviceID = %s) AND modelNumber = (SELECT modelNumber FROM Device WHERE deviceID = %s)""",[device_id,device_id])
    	model_info = cur.fetchone()
    	if len(model_info) == 0:
    		pass
    	else:
    		model = {'manufacturer': model_info[0],'model_number': model_info[1],'description': model_info[2],'weight': model_info[3],}
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    model_info = [
        'Zoomzone',              # manufacturer
        '9854941272',            # modelNumber
        'brick--I mean laptop',  # description
        2000,                    # weight
    ]


    '''
    return model


#####################################################
#   Query (e)
#   Get Repair Details
#####################################################

def get_repair_details(repair_id: int) -> Optional[dict]:
    """
    Get information about a repair in detail, including service information.
    """

    # TODO Dummy data - Change to be useful!
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    repair = []
    try:
    	cur.execute("""SELECT R.repairID, R.faultreport, R.startdate, R.enddate, R.cost, S.abn, S.serviceName, S.email, R.doneTo 
    		FROM public.Repair R JOIN public.Service S ON (R.doneBy = S.abn) 
    		WHERE R.repairID = %s""",[repair_id])
    	repair_info = cur.fetchone()
    	if len(repair_info)== 0:
    		pass
    	else:
    		repair = {'repair_id': repair_info[0],'fault_report': repair_info[1],'start_date': repair_info[2],'end_date': repair_info[3],'cost': repair_info[4],
    		'done_by': {'abn': repair_info[5],'service_name': repair_info[6],'email': repair_info[7],},'done_to': repair_info[8]}
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    repair_info = [
        17,                    # repair ID
        'Never, The',          # fault report
        datetime.date(2018, 7, 16),  # start date
        datetime.date(2018, 9, 22),  # end date
        '$837.13',             # cost
        '12345678901',         # service ABN
        'TopDrive',            # service name
        'repair@example.com',  # service email
        1,                     # done to device
    ]

    
    '''
    return repair


#####################################################
#   Query (f[ii])
#   Get Models assigned to Department
#####################################################

def get_department_models(department_name: str) -> list:
    """
    Return all models assigned to a department.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the models allocated to the department.
    # Each "row" has: [ manufacturer, modelnumber, maxnumber ]
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    model_allocations = []
    try:
    	cur.execute("""SELECT manufacturer,modelNumber,maxnumber 
    		FROM public.ModelAllocations
    		WHERE department = %s""",[department_name])
    	res = cur.fetchall()
    	if len(res) == 0:
    		pass
    	else:
    		model_allocations = res
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    model_allocations = [
        ['Devpulse', '4030141218', 153],
        ['Gabcube', '1666158895', 186],
        ['Feednation', '2050267274', 275],
        ['Zoombox', '8860068207', 199],
        ['Shufflebeat', '0288809602', 208],
        ['Voonyx', '5275001460', 264],
        ['Tagpad', '3772470904', 227],
    ]
    '''
    return model_allocations


#####################################################
#   Query (f[iii])
#   Get Number of Devices of Model owned
#   by Employee in Department
#####################################################

def get_employee_department_model_device(department_name: str, manufacturer: str, model_number: str) -> list:
    """
    Get the number of devices owned per employee in a department
    matching the model.

    E.g. Model = iPhone, Manufacturer = Apple, Department = "Accounting"
        - [ 1337, Misty, 20 ]
        - [ 351, Pikachu, 10 ]
    """

    # TODO Dummy Data - Change to be useful!
    # Return the number of devices owned by each employee matching department,
    #   manufacturer and model.
    # Each "row" has: [ empid, name, number of devices issued that match ]
    conn = database_connect()
    if conn is None:
    	return None

    cur = conn.cursor()
    employee_counts = []
    try:
    	cur.execute("""SELECT E.empid, E.name, COUNT(D.issuedTo) 
    		FROM public.Employee E JOIN public.Device D (E.empid = D.issedTo) JOIN public.EmployeeDepartments ED USING(empid) 
    		WHERE ED.department = %s AND D.manufacturer = %s AND D.modelNumber = %s
    		GROUP BY E.empid""",[department_name,manufacturer,model_number])
    	res = cur.fetchall()
    	if len(res) == 0:
    		pass
    	else:
    		employee_counts = res
    except Exception as e:
    	print("Error fetching database")
    	print(e)
    cur.close()
    conn.close()
    '''
    employee_counts = [
        [1337, 'Misty', 20],
        [351, 'Pikachu', 1],
        [919, 'Hermione', 8],
    ]
    '''
    return employee_counts


#####################################################
#   Query (f[iv])
#   Get a list of devices for a certain model and
#       have a boolean showing if the employee has
#       it issued.
#####################################################

def get_model_device_assigned(model_number: str, manufacturer: str, employee_id: int) -> list:
    """
    Get all devices matching the model and manufacturer and show True/False
    if the employee has the device assigned.

    E.g. Model = Pixel 2, Manufacturer = Google, employee_id = 1337
        - [123656, False]
        - [123132, True]
        - [51413, True]
        - [8765, False]
    """

    # TODO Dummy Data - Change to be useful!
    # Return each device of this model and whether the employee has it
    # issued.
    # Each "row" has: [ device_id, True if issued, else False.]
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    device_assigned = []
    try:
    	cur.execute("""SELECT deviceID, CASE WHEN issuedTo = %s THEN 'True' ELSE 'FALSE' END 
    		FROM public.Device 
    		WHERE manufacturer = %s AND modelNumber = %s""",[employee_id,manufacturer,model_number])
    	res = cur.fetchall()
    	if Len(res) == 0:
    		pass
    	else:
    		device_assigned = res
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    device_assigned = [
        [123656, False],
        [123132, True],
        [51413, True],
        [8765, False],
    ]
    '''
    return device_assigned


#####################################################
#   Get a list of devices for this model and
#       manufacturer that have not been assigned.
#####################################################

def get_unassigned_devices_for_model(model_number: str, manufacturer: str) -> list:
    """
    Get all unassigned devices for the model.
    """
    # TODO Dummy Data - Change to be useful!
    # Return each device of this model that has not been issued
    # Each "row" has: [ device_id ]
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    device_unissued = []
    try:
    	cur.execute("""SELECT deviceID 
    		FROM public.Device
    		WHERE (modelNumber = %s OR manufacturer = %s) AND issuedTo IS NULL""",[manufacturer,model_number])
    	res = cur.fetchall()
    	if Len(res) == 0:
    		pass
    	else:
    		device_unissued = res
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    device_unissued = [123656, 123132, 51413, 8765]
    '''
    return device_unissued


#####################################################
#   Get Employees in Department
#####################################################

def get_employees_in_department(department_name: str) -> list:
    """
    Return all the employees' IDs and names in a given department.
    """
    # TODO Dummy Data - Change to be useful!
    # Return the employees in the department.
    # Each "row" has: [ empid, name ]
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    employees = []
    try:
    	cur.execute("""SELECT E.empid, E.name 
    		FROM public.Employee E JOIN public.EmployeeDepartments ED USING(empid) 
    		WHERE ED.department = %s""",[department_name])
    	res = cur.fetchall()
    	if len(res) == 0:
    		pass
    	else:
    		employees = res
    except Exception as e:
    	print("Error fetcing database")
    	print(e)
    cur.close()
    conn.close()
    '''
    employees = [
        [15905, 'Rea Fibbings'],
        [9438, 'Julia Norville'],
        [36020, 'Adora Lansdowne'],
        [98809, 'Nathanial Farfoot'],
        [58407, 'Lynne Smorthit'],
    ]
    '''
    return employees


#####################################################
#   Query (f[v])
#   Issue Device
#####################################################

def issue_device_to_employee(employee_id: int, device_id: int):
    """
    Issue the device to the chosen employee.
    """
    # TODO issue the device from the employee
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already issued?
    #       - Employee not in department?
    # return (False, "Device already issued")
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    ops = True
    detail = None
    cur.execute(""" SELECT issuedTo FROM public.Device WHERE deviceID = %s """,[device_id])
    p_it = cur.fetchone()
    if p_it == [None]:
    	cur.execute("""UPDATE public.Device SET issuedTo = %s WHERE deviceId = %s""",[employee_id,device_id])
    	cur.execute("""SELECT issuedTo FROM public.Device WHERE deviceID = %s""",[device_id])
    	n_it = cur.fetchone()
    	key = n_it[0]
    	employee_id_int = int(employee_id)
    	print(key)
    	print(employee_id)
    	print(type(key))
    	print(type(employee_id_int))
    	if key != employee_id_int:
    		ops = False
    		detail = "Employee not in department"
    else:
    	ops = False
    	detail = "Device already issued"
    cur.close()
    conn.close()
    return (ops, detail)


#####################################################
#   Query (f[vi])
#   Revoke Device Issued to User
#####################################################

def revoke_device_from_employee(employee_id: int, device_id: int):
    """
    Revoke the device from the employee.
    """
    # TODO revoke the device from the employee.
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already revoked?
    #       - employee not assigned to device?

    # return (False, "Device already unassigned")
    conn = database_connect()
    if conn is None:
    	return None
    cur = conn.cursor()
    ops = True
    detail = None
    cur.execute(""" SELECT issuedTo FROM public.Device WHERE deviceID = %s """,[device_id])
    p_it = cur.fetchone()

    if p_it != [None]:
    	if p_it[0] == int(employee_id):
    		cur.execute("""UPDATE public.Device SET issuedTo = NULL WHERE issuedTo = %s AND deviceId = %s""",[employee_id,device_id])
    	else:
    		ops = False
    		detail = "Employee not assigned to device"
    else:
    	ops = False
    	detail = "Device already revoked"
    cur.close()
    conn.close()
    return (ops, detail)

if (__name__ == '__main__'):
	print("check_login('03081')")
	print("is_manager('72')")
	print("get_devices_used_by('12247')")
	print("employee_works_in('84')")
	print("get_issued_devices_for_user('12247')")
	print("get_all_models()")
	print("get_device_repairs('1')")
	print("get_device_information('1')")
	print("get_device_model('1')")
	print("get_repair_details()")
	print("get_employees_in_department()")
	print("get_department_models()")
	print("get_model_device_assigned()")
	print("get_unassigned_devices_for_model()")
	print("get_employee_department_model_device()")
	print("issue_device_to_employee()")
	print("revoke_device_from_employee()")