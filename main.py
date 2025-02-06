import csv
import glob
import os
import pandas as pd
from datetime import datetime

data_directory_22 = "C:/Users/lydia/Documents/PythonProjects/Data/TrumpFunding/FEC/Data_For_Use/indiv22/by_date"
data_directory_24 = "C:/Users/lydia/Documents/PythonProjects/Data/TrumpFunding/FEC/Data_For_Use/indiv24/by_date"
directories = [data_directory_22, data_directory_24]

cand_comm_link = "C:/Users/lydia/Documents/PythonProjects/Data/TrumpFunding/FEC/Data_For_Use/candidate_committee_linkages_21-24.csv"
cont_by_indiv = "C:/Users/lydia/Documents/PythonProjects/Data/TrumpFunding/FEC/Data_For_Use/cont_by_indiv_21-24.csv"
cont_by_comm = "C:/Users/lydia/Documents/PythonProjects/Data/TrumpFunding/FEC/Data_For_Use/cont_by_committee_21-24.csv"

# output csv
trump_contributors_csv = "C:/Users/lydia/Documents/PythonProjects/Data/TrumpFunding/FEC/Processing/trump_contributors.csv"

# date filters
start_date = pd.to_datetime("11152022", format="%m%d%Y")
end_date = pd.to_datetime("11052024", format="%m%d%Y")

#transaction types (codes in cont_by_comm)
pro_cand_code = ["24C", "24E"]

#trump's candidate id
trump_cand_id = "P80001571"

# consolidate contributions by individuals txt files into 1 csv file
# for directory in directories:
# 	for txt_file in glob.glob(os.path.join(directory, '*.txt')):
# 		with open(txt_file, 'r') as in_file:
# 			lines = [line.replace("\n", "").split("|") for line in in_file]
# 			with open(cont_by_indiv, 'a', newline="") as out_file:
# 				writer = csv.writer(out_file)
# 				writer.writerows(lines)

# make a dataframe of each csv
cand_comm_df = pd.read_csv(cand_comm_link, encoding="latin-1", dtype="string")
# cont_by_indiv_df = pd.read_csv(cont_by_indiv, encoding="latin-1", dtype="string")
cont_by_comm_df = pd.read_csv(cont_by_comm, encoding="latin-1", dtype="string")

# convert date column to datetime format for individual contribution df
# cont_by_indiv_df.TRANSACTION_DT = pd.to_datetime(cont_by_indiv_df.TRANSACTION_DT, format="%m%d%Y")

# make a committee id list - get the committee ids from the candidate committee linkage df where the candidate id is trump_cand_id
#							 get the committee ids from the contribution by committee df where the candidate id is trump_cand_id and the transaction type supports the candidate
#                            concat the two committee id dfs (only unique values)
comm_ids_1 = cand_comm_df[cand_comm_df.CAND_ID == trump_cand_id].CMTE_ID
comm_ids_2 = cont_by_comm_df[(cont_by_comm_df.CAND_ID == trump_cand_id)
							 & (cont_by_comm_df.TRANSACTION_TP.isin(pro_cand_code))
							].CMTE_ID
comm_ids = pd.concat([comm_ids_1, comm_ids_2], ignore_index=True).unique().tolist()
print(comm_ids)

# make a df of individuals who contributed to trump's campaign - get all rows from cont_by_indiv_df where:
# 	the CMTE_ID is in comm_ids
#	the transaction date is between 11/15/22 and 11/05/24 (from when he officially announced he was running to when he
#	was elected)
# trump_contributors_df = cont_by_indiv_df[(cont_by_indiv_df.CMTE_ID.isin(comm_ids))
# 										 & (start_date <= cont_by_indiv_df.TRANSACTION_DT)
# 										 & (cont_by_indiv_df.TRANSACTION_DT <= end_date)]
# print(trump_contributors_df.head())
# trump_contributors_df.to_csv(trump_contributors_csv, mode="a", index=False)
