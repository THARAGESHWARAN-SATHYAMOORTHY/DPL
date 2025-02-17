import pandas as pd
import matplotlib.pyplot as plt 
import math

worst={}
teams = ['CSK', 'DC', 'GT', 'KKR', 'LSG', 'MI', 'PBKS', 'RR', 'RCB', 'SRH']
for i in teams:
    xls = pd.ExcelFile(f'./Teams/{i}/BATSMEN/{i}_BATSMEN.xlsx')
    dfs = {}
    worst={}
    for sheet in xls.sheet_names:
        dfs[sheet] = pd.read_excel(xls, sheet_name=sheet)

    for i in dfs:
        a={}
        for index, row in dfs[i].iterrows():
            if row['Ground']!='-':  
                if row['Runs'] != '-':
                    if row['S/R'] != '-':
                        row["Runs"]=str(row["Runs"]).replace("*","")
                        if row['Ground'] not in a: 
                            a[row['Ground']]=[int(row['Runs']),int(row['S/R']),1]
                        else:
                            a[row['Ground']]=[ a[row['Ground']][0]+int(row['Runs']), a[row['Ground']][1]+int(row['S/R']), a[row['Ground']][2]+1]
        worst[i]=a

    for i in worst:
        for j in worst[i]:
            worst[i][j]=[worst[i][j][0]/worst[i][j][2],worst[i][j][1]/worst[i][j][2]]

    weight_runs = 0.7
    weight_sr = 0.3

    for batsman, data in worst.items():
        scores = {ground: (weight_runs * stats[0] + weight_sr * stats[1], stats) for ground, stats in data.items()} 
        worst_ground = min(scores.items(), key=lambda x: x[1][0])  
        best_ground = max(scores.items(), key=lambda x: x[1][0])  
        print(f"{batsman} performs worst at {worst_ground[0]} with a score of {worst_ground[1][0]} (runs: {worst_ground[1][1][0]}, strike rate: {worst_ground[1][1][1]}).")  # replace 'against' with 'at'
        print(f"{batsman} performs best at {best_ground[0]} with a score of {best_ground[1][0]} (runs: {best_ground[1][1][0]}, strike rate: {best_ground[1][1][1]}).")  # replace 'against' with 'at'
        print("\n")

    num_players = len(worst)
    num_cols = 2
    num_rows = math.ceil(num_players / num_cols)

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, num_rows*5))

    for idx, (player, data) in enumerate(worst.items()):
        ax1 = axs[idx // num_cols, idx % num_cols]

        grounds = list(data.keys()) 
        avg_runs = [ground_data[0] for ground_data in data.values()]  
        avg_strike_rate = [ground_data[1] for ground_data in data.values()] 

        color = 'tab:blue'
        ax1.set_xlabel('Grounds')
        ax1.set_ylabel('Average Runs', color=color)
        ax1.bar(grounds, avg_runs, color=color) 
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Average Strike Rate', color=color)
        ax2.plot(grounds, avg_strike_rate, color=color)  
        ax2.tick_params(axis='y', labelcolor=color)

        ax1.set_title(f'Performance of {player}')

    if num_players % num_cols != 0:
        for idx in range(num_players, num_rows * num_cols):
            fig.delaxes(axs.flatten()[idx])

    fig.tight_layout()
    plt.show()