
# coding: utf-8

# In[1]:

import requests
import os
import json
from bs4 import BeautifulSoup
import urllib.request as rq
import urllib
from zipfile import ZipFile
from io import BytesIO
import lxml
import pandas as pd
import sys


# In[2]:

def find_files(response):
    soup = BeautifulSoup(response.text, "lxml")

    download_url = 'https://freddiemac.embs.com/FLoan/Data/'
    hrefs = []
    for a in soup.find_all('a'):
        hrefs.append(download_url + a['href'])
        
    return hrefs


# In[7]:

# Logging in to the website and downloading the sample files from 2005 onwards 
def downloadSampleFiles(username, password, trainQuarter, testQuarter):
    LOGIN_URL = "https://freddiemac.embs.com/FLoan/secure/auth.php"
    URL = "https://freddiemac.embs.com/FLoan/Data/download.php"
    with requests.session() as c:
    
        payload = {'username': username, 'password': password,                  'action': 'acceptTandC', 'acceptSubmit': 'Continue', 'accept':'Yes'}
    
        try:
            login_response = c.post(LOGIN_URL, data = payload)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
    
        print('Logged in to the website!!', '\n')
        download_response = c.post(URL, data=payload)

        list_of_links = find_files(download_response)
        print('Collected the required file links!!', '\n')
        
        download_path = './Data/historical_data/'

        temp_year_list = [trainQuarter, testQuarter]
        
        existing_year_list = []
        year_list = []

        for path, subdirs, files in os.walk(download_path):
            for file in files:
                existing_year_list.append(file[-10:-4])

        for x in temp_year_list:
            if x not in set(existing_year_list):
                year_list.append(x)
    
        if not os.path.exists(download_path):            
            print('Creating required directories!!', '\n')
            os.makedirs(download_path)
        else:
            print('Directories already exist. Continuing the process!!', '\n')
        
        if not year_list:
            print('Historical Files already exist!!!')
            exit(0)
        else:
            print('Starting historical files download!!', '\n')
            files_required = []
            count = 0
            for link in list_of_links:
                for year in year_list:
                    if ('historical_data1_' + year) in link:
                        count = count + 1
                    if count > 0:        
                        files_required.append([link, 'historical_data1_' + year])
                    count = 0      
        
            for file, filename in files_required:
                samplefile_response = c.get(file)
                samplefile_content = ZipFile(BytesIO(samplefile_response.content)) 
                samplefile_content.extractall(download_path + filename)
                
            print('Sample files downloaded in the path: ' + download_path, '\n')
            
#downloadSampleFiles("prashantvksingh@gmail.com", "V4wlNZow", 'Q12005', 'Q22005')


# In[ ]:

def changedatatype(df):
    #Change the data types for all column
    df[['fico','cd_msa','mi_pct','cnt_borr','cnt_units','cltv','dti','orig_upb','ltv','zipcode','orig_loan_term']] = df[['fico','cd_msa','mi_pct','cnt_borr','cnt_units','cltv','dti','orig_upb','ltv','zipcode','orig_loan_term']].astype('int64')
    df[['flag_sc','servicer_name']] = df[['flag_sc','servicer_name']].astype('str')
    return df


# In[3]:

def changeperformancedatatype(perf_df):
        perf_df[['curr_ln_delin_status','loan_age','remng_mon_to_leg_matur','zero_bal_cd','current_dupb',                 'actual_loss_calc']] = perf_df[['curr_ln_delin_status','loan_age','remng_mon_to_leg_matur',                                                 'zero_bal_cd','current_dupb','actual_loss_calc']].astype('int64')

        perf_df[['mon_rpt_prd','zero_bal_eff_dt','lst_pd_inst_duedt']] = perf_df[['mon_rpt_prd','zero_bal_eff_dt',                                                                                  'lst_pd_inst_duedt']].astype('str')
        return perf_df


# In[ ]:

def fillNAN(df):
    df['fico'] = df['fico'].fillna(0)
    df['flag_fthb']=df['flag_fthb'].fillna('X')
    df['cd_msa']=df['cd_msa'].fillna(0)
    df['mi_pct']=df['mi_pct'].fillna(0)
    df['cnt_units']=df['cnt_units'].fillna(0)
    df['occpy_sts']=df['occpy_sts'].fillna('X')
    df['cltv']=df['cltv'].fillna(0)
    df['dti']=df['dti'].fillna(0)
    df['ltv']=df['ltv'].fillna(0)
    df['channel']=df['channel'].fillna('X')
    df['ppmt_pnlty']=df['ppmt_pnlty'].fillna('X')
    df['prop_type']=df['prop_type'].fillna('XX')
    df['zipcode']=df['zipcode'].fillna(0)
    df['loan_purpose']=df['loan_purpose'].fillna('X')
    df['cnt_borr']=df['cnt_borr'].fillna(0)
    df['flag_sc']=df['flag_sc'].fillna('N')
    return df


# In[4]:

def performance_fillNA(perf_df):
    perf_df['curr_ln_delin_status'] = perf_df['curr_ln_delin_status'].fillna(0)
    perf_df['repurch_flag']=perf_df['repurch_flag'].fillna('Unknown')
    perf_df['mod_flag']=perf_df['mod_flag'].fillna('N')
    perf_df['zero_bal_cd']=perf_df['zero_bal_cd'].fillna(00)
    perf_df['zero_bal_eff_dt']=perf_df['zero_bal_eff_dt'].fillna('199601')
    perf_df['current_dupb']=perf_df['current_dupb'].fillna(0)
    perf_df['lst_pd_inst_duedt']=perf_df['lst_pd_inst_duedt'].fillna('199601')
    perf_df['mi_recoveries']=perf_df['mi_recoveries'].fillna(0)
    perf_df['net_sale_proceeds']=perf_df['net_sale_proceeds'].fillna('U')
    perf_df['non_mi_recoveries']=perf_df['non_mi_recoveries'].fillna(0)
    perf_df['expenses']=perf_df['expenses'].fillna(0)
    perf_df['legal_costs']=perf_df['legal_costs'].fillna(0)
    perf_df['maint_pres_costs']=perf_df['maint_pres_costs'].fillna(0)
    perf_df['taxes_and_insur']=perf_df['taxes_and_insur'].fillna(0)
    perf_df['misc_expenses']=perf_df['misc_expenses'].fillna(0)
    perf_df['actual_loss_calc']=perf_df['actual_loss_calc'].fillna(0)
    perf_df['mod_cost']=perf_df['mod_cost'].fillna(0)
    
    return perf_df


# In[5]:

def minmax(perf_df):
    new1_df = perf_df.groupby(['id_loan'])['current_aupb'].min().to_frame(name = 'min_current_aupb').reset_index()
    new2_df = perf_df.groupby(['id_loan'])['current_aupb'].max().to_frame(name = 'max_current_aupb').reset_index()
    new3_df = perf_df.groupby(['id_loan'])['curr_ln_delin_status'].min().to_frame(name = 'min_curr_ln_delin_status').reset_index()
    new4_df = perf_df.groupby(['id_loan'])['curr_ln_delin_status'].max().to_frame(name = 'max_curr_ln_delin_status').reset_index()
    new5_df = perf_df.groupby(['id_loan'])['zero_bal_cd'].min().to_frame(name = 'min_zero_bal_cd').reset_index()
    new6_df = perf_df.groupby(['id_loan'])['zero_bal_cd'].max().to_frame(name = 'max_zero_bal_cd').reset_index()
    new7_df = perf_df.groupby(['id_loan'])['mi_recoveries'].min().to_frame(name = 'min_mi_recoveries').reset_index()
    new8_df = perf_df.groupby(['id_loan'])['mi_recoveries'].max().to_frame(name = 'max_mi_recoveries').reset_index()
    new11_df = perf_df.groupby(['id_loan'])['non_mi_recoveries'].min().to_frame(name = 'min_non_mi_recoveries').reset_index()
    new12_df = perf_df.groupby(['id_loan'])['non_mi_recoveries'].max().to_frame(name = 'max_non_mi_recoveries').reset_index()
    new13_df = perf_df.groupby(['id_loan'])['expenses'].min().to_frame(name = 'min_expenses').reset_index()
    new14_df = perf_df.groupby(['id_loan'])['expenses'].max().to_frame(name = 'max_expenses').reset_index()
    new15_df = perf_df.groupby(['id_loan'])['legal_costs'].min().to_frame(name = 'min_legal_costs').reset_index()
    new16_df = perf_df.groupby(['id_loan'])['legal_costs'].max().to_frame(name = 'max_legal_costs').reset_index()
    new17_df = perf_df.groupby(['id_loan'])['maint_pres_costs'].min().to_frame(name = 'min_maint_pres_costs').reset_index()
    new18_df = perf_df.groupby(['id_loan'])['maint_pres_costs'].max().to_frame(name = 'max_maint_pres_costs').reset_index()
    new19_df = perf_df.groupby(['id_loan'])['taxes_and_insur'].min().to_frame(name = 'min_taxes_and_insur').reset_index()
    new20_df = perf_df.groupby(['id_loan'])['taxes_and_insur'].max().to_frame(name = 'max_taxes_and_insur').reset_index()
    new21_df = perf_df.groupby(['id_loan'])['misc_expenses'].min().to_frame(name = 'min_misc_expenses').reset_index()
    new22_df = perf_df.groupby(['id_loan'])['misc_expenses'].max().to_frame(name = 'max_misc_expenses').reset_index()
    new23_df = perf_df.groupby(['id_loan'])['actual_loss_calc'].min().to_frame(name = 'min_actual_loss_calc').reset_index()
    new24_df = perf_df.groupby(['id_loan'])['actual_loss_calc'].max().to_frame(name = 'max_actual_loss_calc').reset_index()
    new25_df = perf_df.groupby(['id_loan'])['mod_cost'].min().to_frame(name = 'min_mod_cost').reset_index()
    new26_df = perf_df.groupby(['id_loan'])['mod_cost'].max().to_frame(name = 'max_mod_cost').reset_index()
    
    final_df = new1_df.merge(new2_df,on='id_loan').merge(new3_df,on='id_loan').merge(new4_df,on='id_loan').    merge(new5_df,on='id_loan').merge(new6_df,on='id_loan').merge(new7_df,on='id_loan').merge(new8_df,on='id_loan').    merge(new11_df,on='id_loan').merge(new12_df,on='id_loan').merge(new13_df,on='id_loan').merge(new14_df,on='id_loan').    merge(new15_df,on='id_loan').merge(new16_df,on='id_loan').merge(new17_df,on='id_loan').merge(new18_df,on='id_loan').    merge(new19_df,on='id_loan').merge(new20_df,on='id_loan').merge(new21_df,on='id_loan').merge(new22_df,on='id_loan').    merge(new23_df,on='id_loan').merge(new24_df,on='id_loan').merge(new25_df,on='id_loan').merge(new26_df,on='id_loan')
    
    return final_df


# In[ ]:

def constructcsv():
    download_path = "./Data/"
    writeHeader1 = True
    filename = download_path + "HistoricalOriginationCombined.csv"
    if os.path.exists(filename):
        os.unlink(filename)
    with open(filename, 'w',encoding='utf-8',newline="") as f:
        for subdir,dirs, files in os.walk(download_path):
            for file in files:
                if 'time' not in file:
                    sample_df = pd.read_csv(os.path.join(subdir,file) ,sep="|",names=['fico','dt_first_pi','flag_fthb','dt_matr','cd_msa',"mi_pct",'cnt_units','occpy_sts','cltv','dti','orig_upb','ltv','int_rt','channel','ppmt_pnlty','prod_type','st', 'prop_type','zipcode','id_loan','loan_purpose', 'orig_loan_term','cnt_borr','seller_name','servicer_name','flag_sc'],skipinitialspace=True)
                    sample_df = fillNAN(sample_df)
                    sample_df = changedatatype(sample_df)
                    sample_df['Year'] = ['19'+x if x=='99' else '20'+x for x in (sample_df['id_loan'].apply(lambda x: x[2:4]))]
                    sample_df['Quater'] =sample_df['id_loan'].apply(lambda x: x[4:6])
                    if writeHeader1 is True:
                        sample_df.to_csv(f, mode='a', header=True,index=False)
                        writeHeader1 = False
                    else:
                        sample_df.to_csv(f, mode='a', header=False,index=False)


# In[6]:

def constructperformancecsv():
    download_path = "./Data/"
    print("Started")
    writeHeader1 = True
    filename = download_path + "HistoricalperformanceCombined.csv"
    if os.path.exists(filename):
        os.unlink(filename)
    with open(filename, 'w',encoding='utf-8',newline="") as f:
        for subdir,dirs, files in os.walk(download_path):
            for file in files:
                if 'time_' in file:
                    temp_list = []
                    chunksize = 10 ** 6
                    for chunk in pd.read_csv(os.path.join(subdir,file) ,sep="|",                                              skipinitialspace=True, chunksize=chunksize, low_memory=False, header=None):
                        temp_list.append(chunk)
                    print('DataFrame creation started!!')
                    frames = []
                    for df in temp_list:
                        frames.append(df)
                    sample_df = pd.concat(frames)
                    sample_df.columns = ['id_loan','mon_rpt_prd','current_aupb','curr_ln_delin_status',                                         'loan_age','remng_mon_to_leg_matur', 'repurch_flag','mod_flag',                                          'zero_bal_cd', 'zero_bal_eff_dt','current_int_rte','current_dupb',                                         'lst_pd_inst_duedt','mi_recoveries', 'net_sale_proceeds',                                         'non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs',                                         'taxes_and_insur','misc_expenses','actual_loss_calc', 'mod_cost']
                    print('DataFrame created!!')
                    
                    sample_df['curr_ln_delin_status'] = [999 if x=='R' else x for x in                                                        (sample_df['curr_ln_delin_status'].apply(lambda x: x))]
                    sample_df['curr_ln_delin_status'] = [0 if x=='XX' else x for x in                                                        (sample_df['curr_ln_delin_status'].apply(lambda x: x))]
                    sample_df = performance_fillNA(sample_df)
                    sample_df = changeperformancedatatype(sample_df)
                    filtered_df = minmax(sample_df)
                    filtered_df['Year'] = ['19'+x if x=='99' else '20'+x for x in (filtered_df['id_loan'].apply(lambda x: x[2:4]))]
                    filtered_df['Quarter'] =filtered_df['id_loan'].apply(lambda x: x[4:6])
                    if writeHeader1 is True:
                        filtered_df.to_csv(f, mode='a', header=True,index=False)
                        writeHeader1 = False
                    else:
                        filtered_df.to_csv(f, mode='a', header=False,index=False)                  


# In[ ]:

def main():
    
    user_input = sys.argv[1:]
    print("----Process Started----")
    counter = 0
    if len(user_input) == 0:
        print('No Input provided. Process is exiting!!')
        exit(0)
    for ip in user_input:
        if counter == 0:
            username = str(ip)
        elif counter == 1:
            password = str(ip)
        elif counter == 2:
            trainQuarter = str(ip)
        else:
            testQuarter = str(ip)
        counter += 1
        
    downloadSampleFiles(username, password, trainQuarter, testQuarter)
    #combineOrigFiles()
    constructcsv()


# In[9]:

if __name__ == '__main__':
    main()

