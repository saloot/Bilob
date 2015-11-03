
#----------------------Report Arguments---------------------------
rep_years = [2013,2014,2015]
#-----------------------------------------------------------------

#-----------------------Initialization----------------------------
import csv
import numpy as np
import plotly.plotly as pltly
from plotly.graph_objs import *

usrname = raw_input("What is your PlotLy username? ")
passwd = raw_input("What is your PlotLy API Key? ")
if not passwd:
    passwd = 'wj370nzaqg'
pltly.sign_in(usrname, passwd)

total_income = 0
total_expense = 0

income_months_all = {}
expenses_months_all = {}
membership_fee_all = {}

data_entries = {'Date':[],
                'Income':[],
                'Comments':[],
                'Confirmed Receiving':[],
                'Total':[],
                'Report sent?': [],
        }
#-----------------------------------------------------------------

#-------------------------Parse Data Entries----------------------
data_file_name = './Data/Bilob Charity - Sheet1.csv'
with open(data_file_name, 'rb') as f:
    reader = csv.DictReader (f)
    for line in reader:
        for item in line:
            if item:
                if 'Income'  in item:
                    if line[item]:
                        data_entries[item].append(float(line[item]))
                else:
                    if line[item]:
                        data_entries[item].append(line[item])
                        #data_entries[item].append(int(line[item][0:4]))
#-----------------------------------------------------------------


for rep_year in rep_years:
    months_list = []
    income_months = []
    expenses_months = []
    membership_fee = []
    for i in range(1,13):
        membership_fee.append(0)
        income_months.append(0)
        
        expenses_months.append(0)
        months_list.append((i))
    #-----------------------Analyze the Data--------------------------
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~Calculate Income/Expenses Per Month~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(0,len(data_entries['Date'])):
        item_date = data_entries['Date'][i]
        item_value = data_entries['Income'][i]
        
        if rep_year == rep_years[0]:
            if item_value > 0:
                total_income = total_income + item_value
            else:
                total_expense = total_expense + item_value
            
        if str(rep_year) in item_date:
            temp = item_date[0:-5]
            ind = temp.find('.')
            month = int(temp[ind+1:])
            
            if item_value > 0:
                income_months[month-1] = income_months[month-1] + item_value
            else:
                expenses_months[month-1] = expenses_months[month-1] + item_value
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~Calculate Ozviat Fee Per Month~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(0,len(data_entries['Date'])):
        item_date = data_entries['Date'][i]
        item_value = data_entries['Income'][i]
            
        if str(rep_year) in item_date:
            if ('Ozviat' in data_entries['Comments'][i]) or ('ozviat' in data_entries['Comments'][i]):
                temp = item_date[0:-5]
                ind = temp.find('.')
                month = int(temp[ind+1:])
            
                if item_value > 0:
                    membership_fee[month-1] = membership_fee[month-1] + item_value
                else:
                    print 'Error!'
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
    #~~~~~~~~~~~~~~~~Calculate Ozviat Fee Per Month~~~~~~~~~~~~~~~~~~
    income_months_all[str(rep_year)] = income_months
    expenses_months_all[str(rep_year)] = expenses_months
    membership_fee_all[str(rep_year)] = membership_fee
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
#-----------------------------------------------------------------

#--------------------------Plot the Data--------------------------

#~~~~~~~~~~~~~~~~~~Plot Income/Expenses Per Month~~~~~~~~~~~~~~~~~
for rep_year in rep_years:
    plot_legends = ['Income','Expenses']
    plot_colors = ['#F62817','#1569C7']
    
    x_array = np.vstack([months_list,months_list])
    y_array = np.vstack([income_months_all[str(rep_year)],np.abs(expenses_months_all[str(rep_year)])])
    no_plots = 2
                    
    plot_title = 'Income/Expenses in Year %s' %(rep_year)
    file_name = 'BilobIncomeExpense' + str(rep_year)
    plot_url = export_to_plotly(x_array,y_array,no_plots,plot_legends,'line',plot_colors,'Month','CHF',plot_title,[],[],file_name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~Plot Income/Expenses Per Year~~~~~~~~~~~~~~~~~~
income_year = []
expenses_year = []
for rep_year in rep_years:
    income_year.append(sum(income_months_all[str(rep_year)]))
    expenses_year.append(sum(expenses_months_all[str(rep_year)]))

plot_legends = ['Income','Expenses']
plot_colors = ['#F62817','#1569C7']

        
x_array = np.vstack([rep_years,rep_years])
y_array = np.vstack([income_year,np.abs(expenses_year)])
no_plots = 2
                
plot_title = 'Income/Expenses over the Years'
plot_url = export_to_plotly(x_array,y_array,no_plots,plot_legends,'bar',plot_colors,'Year','CHF',plot_title,[],[],'BilobYearlyIncome')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~Plot Total Income/Expenses~~~~~~~~~~~~~~~~~~~
plot_legends = ['Income','Expenses']
plot_colors = ['#F62817','#1569C7']

        
x_array = np.vstack(['Total','Total'])
y_array = np.vstack([total_income,np.abs(total_expense)])
no_plots = 2
                
plot_title = 'Total Income/Expenses from the Beginning'
plot_url = export_to_plotly(x_array,y_array,no_plots,plot_legends,'bar',plot_colors,'','CHF',plot_title,[],[],'BilobTotallyIncome')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~Plot Membership Fees Per Month/Year~~~~~~~~~~~~~~
plot_colors = ['#F62817','#1569C7','#FBB917']

x_array = []
y_array = []
plot_legends = []

for rep_year in rep_years:
    if len(x_array) == 0:
        x_array = np.vstack([months_list])
        y_array = np.vstack([membership_fee_all[str(rep_year)]])
    else:
        x_array = np.vstack([x_array,months_list])
        y_array = np.vstack([y_array,membership_fee_all[str(rep_year)]])
    plot_legends.append(str(rep_year))    
    
no_plots = len(rep_years)
                
plot_title = 'Membership income in Years'
plot_url = export_to_plotly(x_array,y_array,no_plots,plot_legends,'line',plot_colors,'Month','CHF',plot_title,[],[],'BilobMonthlyMembership')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~Plot Expense Per Case~~~~~~~~~~~~~~~~~~~
# Plot 4
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#-----------------------------------------------------------------





#==============================================================================
#==============================export_to_plotly================================
#==============================================================================
#-------------------------------Descriptions-----------------------------------
# This function saves the plots in a format that is intreprettable by the
# "Vis.js" javascript plugin which displays the resulting graph on the web.

# INPUT:
#    W: the actual graph
#    W_inferred_our: the inferred graph
#    file_name_base_results: the base (usually address to the folder) where the results should be saved
#    file_name_ending: the filename endings

# OUTPUT:
#    None
#------------------------------------------------------------------------------

def export_to_plotly(x_array,y_array,no_plots,plot_legends,plot_type,plot_colors,x_label,y_label,plot_title,error_array=[],error_bar_colors = [],file_name_ind=''):
    
    if len(error_array):
        error_flag = 1
    else:
        error_flag = 0
    
    traces = []
    
    for i in range (0,no_plots):
        X = x_array[i,:]
        Y = y_array[i,:]
        if error_flag:
            e = error_array[i,:]
    
            if plot_type == 'line':
                trace = Scatter(
                    x=X,
                    y=Y,
                    name=plot_legends[i],
                    error_y=ErrorY(
                        type='data',
                        array=e,
                        visible=True,
                        color=error_bar_colors[i],
                        ),
                    marker=Marker(
                       color=plot_colors[i]
                    ),
                    )
            else:
                trace = Bar(
                    x=X,
                    y=Y,
                    marker=Marker(
                       color=plot_colors[i]
                    ),
                    name=plot_legends[i],
                    error_y=ErrorY(
                        type='data',
                        array=e,
                        visible=True,
                        color=error_bar_colors[i],
                        )
                    )
        else:
            
            if plot_type == 'line':
                trace = Scatter(
                    x=X,
                    y=Y,
                    name=plot_legends[i],
                    marker=Marker(
                       color=plot_colors[i],
                    ),
                    )
            else:
                trace = Bar(
                    x=X,
                    y=Y,
                    name=plot_legends[i],
                    marker=Marker(
                       color=plot_colors[i]
                    ),
                    )
            
        
        traces.append(trace)
    data = Data(traces)
    
    
    if plot_type == 'bar':
        layout = Layout(
            title=plot_title,
            barmode='group',
            xaxis=XAxis(
                title=x_label,                
            ),
            yaxis=YAxis(
                title=y_label,                
            ),
        )
    else:
        layout = Layout(
            title=plot_title, 
            xaxis=XAxis(
                title=x_label,                
            ),
            yaxis=YAxis(
                title=y_label,                
            ),
        )
        
    
    fig = Figure(data=data, layout=layout)
    if plot_type == 'bar':        
        if error_flag:
            plot_url = pltly.plot(fig, filename=file_name_ind)
        else:
            plot_url = pltly.plot(fig, filename=file_name_ind)
    else:
        if error_flag:
            plot_url = pltly.plot(fig, filename=file_name_ind)
        else:
            plot_url = pltly.plot(fig, filename=file_name_ind)
    
    
    return plot_url