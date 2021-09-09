#! /usr/bin/env python3

import os
import sys
import warnings
import getpass
from atlassian import Confluence
from tabulate import tabulate
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.exceptions import SessionClosedException


wiki_url = 'https://wiki.net'
wiki_user = getpass.getuser()
wiki_pass = getpass.getpass(prompt='Password ')
wiki_prt_pg_id = os.getenv('wiki_prnt_id')

if not sys.warnoptions:
    warnings.simplefilter("ignore")


def triage_form():
    conf = Confluence(url=wiki_url, username=wiki_user, password=wiki_pass)

    basic = input_group("Basic Info",
                        [textarea("URL: ", type=URL, rows=1, required=True, help_text='URL with issue', name='url'),
                         textarea("Service Name: ", required=True, type=TEXT, rows=1, help_text='service name',
                                  name='srv_name'),
                         textarea("API : ", required=True, type=TEXT, rows=1, name='api'),
                         radio("Is this customer impacting?", options=[('Yes', 'yes'), ('No', 'no')], required=True,
                               name='cus_impact'),
                         select("Which environment is this occurring ?",
                                options=[('PROD', 'prd'), ('SOAK', 'soak'), ('UAT', 'uat'), ('INT', 'int')],
                                required=True, name='env'),
                         textarea("Please provide brief description: ", type=TEXT, rows=3, name='descp'),
                         textarea("Sample Account Number which shows issue: ", type=NUMBER, rows=1, required=True,
                                  placeholder='numbers only', name='acct_num'),
                         textarea("What is the customer experience ?", type=TEXT, rows=3, required=True,
                                  name='cus_exp'),
                         textarea("Describe how is this impacting customers ?", type=TEXT, required=True, rows=3,
                                  name='cus_imp'),
                         textarea("How many customers are impacted ?", type=NUMBER, rows=1, required=True,
                                  placeholder='0-1000', help_text='numbers only', name='cus_imp_cnt'),
                         textarea("Sample Request that shows the issue: ", type=TEXT, rows=3, help_text='request info',
                                  required=True, name='req'),
                         radio("What is the urgency on this issue ?",
                               options=[('High', 'high'), ('Med', 'medium'), ('Low', 'low')],
                               help_text='High:1-4 hrs, Med:next business day, Low: Sprint', required=True, name='urg'),
                         textarea("Describe briefly on urgency", type=TEXT, rows=2, help_text='Be precise & clear',
                                  name='urg_txt'),
                         radio("Were there any Deployment and/or Feature rollout recently ?",
                               options=[('Yes', 'yes'), ('No', 'no')], required=True, name='depl_feat'),
                         radio("Did this issue occur in Beta testing ?", options=[('Yes', 'yes'), ('No', 'no')],
                               required=True, name='beta_test'),
                         radio("Does this request have Session ID in it ?", options=[('Yes', 'yes'), ('No', 'no')],
                               required=True, name='sess_id')])
    headers = ['Field', 'Content']
    tab_data = ['Url', basic['url']], ['Service Name', basic['srv_name']], \
               ['API', basic['api']], ['Customer Impact', basic['cus_impact']], \
               ['Environment', basic['env']], ['Description', basic['descp']], \
               ['Sample Acct', basic['acct_num']], ['Customer experince', basic['cus_exp']], \
               ['Impacted customers count', basic['cus_imp_cnt']], \
               ['Sample Request', basic['req']], ['Urgency', basic['urg']], \
               ['Urgency Justification', basic['urg_txt']], \
               ['Deployment recently', basic['depl_feat']], \
               ['Beta Testing', basic['beta_test']], ['Session-ID', basic['sess_id']]

    print(tab_data)

    if basic['sess_id'] == 'yes':
        sess_info = input_group("Please provide Session information: ",
                                [textarea("Affiliate: ", type=TEXT, rows=1, required=True, name='aff'),
                                 textarea("Channel: ", type=TEXT, rows=1, required=True, name='chan'),
                                 textarea("Agent: ", type=TEXT, rows=1, required=True, name='agent'),
                                 textarea("Sample response that shows the issue: ", type=TEXT, rows=3, required=True,
                                          name='resp')])
        print(sess_info)
        session_data = ['Affliate', sess_info['aff']], \
                       ['Channel', sess_info['chan']], \
                       ['Agent', sess_info['agent']], \
                       ['Sample response with issue', sess_info['resp']]
        print(session_data)
        tab_data += session_data

    basic_data = tabulate(tab_data, headers=headers, tablefmt="html")
    print(tab_data)
    popup('Submitted form', [put_table(tab_data, header=headers)])

    status = conf.update_or_create(title='Triage form', body=basic_data, parent_id=wiki_prt_pg_id)

    return status


def app():
    try:
        triage_form()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        app()
        # start_server(app, port=9995, debug=True)
    except SessionClosedException:
        print("session closed unexpectedly")
