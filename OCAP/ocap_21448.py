import pyodbc
from skywater_email import *
import smtplib
'''

Query the open OCAP 21448 that's between steps 1-11 and
have not had any progress made in the past 3 days.

'''
def sql_query(sql_in):
    username = 'ccag'
    password = 'king123'
    try:
        conn = pyodbc.connect('DSN=echits4;UID=ccag,PWD=king123')

        cur = conn.cursor()
        cur.execute(sql_in)
        data_out = []
        for row in cur:
            data_out.append(list(row))
        cur.close()
    except pyodbc.Error as error:
            print("Error while working with SQLite: ", error)
    finally:
        if (conn):
            conn.close()
            print("SQLite connection is closed")
    return data_out


sql_in ="select ocap_entry_id, process_tool, creation_time, creation_who, last_action, next_step_id from ocap_entry where ocap_form_id = 21448 and next_step_id <= 11 and next_step_id >= 1 and last_action < CURRENT_DATE - 3"
data_out = sql_query(sql_in)
text_block = []
for i in data_out:
    text_template = "\nOCAP ID: %i, Tool: %s, Creation Time: %s, Who: %s, Last Action Time: %s, Step: %i" %(i[0], i[1],i[2].strftime("%Y-%m-%d"), i[3],i[4].strftime("%Y-%m-%d %H:%M"), i[5])
    text_block.append(text_template)

print('text block length')
print(len(text_block))

if not len(text_block) == 0:

	subject = "OCAP 21448 Still Open Alert"

	body =''' 
	Below are a list of open Reticle Conversion OCAPS for OCAP 21448 that have
	been open for longer than 3 days and have not progressed past step 11.
	This is an automated email from Chase Grieves, do not reply back. \n\n'''+ "\n".join(text_block)



	to_list = ['chase.grieves@skywatertechnology.com','Jeff.Schefske@SkyWaterTechnology.com','Jeremy.Warren@SkyWaterTechnology.com','Mark.Nelson@skywatertechnology.com']

	send_email(to_list,subject, body)
