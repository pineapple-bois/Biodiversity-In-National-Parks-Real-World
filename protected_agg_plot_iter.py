sw_birds_df['is_protected'] = sw_birds_df.conservation_status != 'Least Concern'

parks_pro_counts = sw_birds_df.groupby(['state', 'park_name', 'is_protected'])\
                    .common_names.nunique()\
                    .reset_index()\
                    .pivot(columns='is_protected',
                            index=['state', 'park_name'],
                            values='common_names')\
                            .reset_index()
parks_pro_counts.columns = ['state', 'park_name', 'not_protected', 'protected']

percentage = round(parks_pro_counts.protected / (parks_pro_counts.protected + parks_pro_counts.not_protected) * 100, 2)
parks_pro_counts['%age_protected'] = percentage

# Split 'park_name' in this dataframe to remove 'National Park'
parks_pro_counts['park_name'] = parks_pro_counts['park_name'].apply(lambda x: x[:-13] if x.endswith(" National Park") else x)
# lambda function doesn't apply to indices [8] or [11] so,
parks_pro_counts.at[8, 'park_name'] = 'Sequoia & Kings Canyon'
parks_pro_counts.at[11, 'park_name'] = 'Great Sand Dunes'

print(parks_pro_counts)

# Plotting only states with more than 2 National Parks.
# Defining a new states_list with above criteria
colours = {'Protected': '#FFAB70', 'Not Protected': '#45AD3E'}
handles = [mpatches.Patch(color=colour, label=label) for label, colour in colours.items()]
states_list_short = ['AZ', 'CA', 'CO', 'UT']

plt.figure(figsize=(20,15))
plt.suptitle('Proportion of Protected Bird Species', fontsize=30, y=1.05)
for i, state in enumerate(states_list_short):
    data = pd.DataFrame(parks_pro_counts[parks_pro_counts['state'] == state])
    plt.subplot(2,2,(i+1))
    plt.title(state, fontsize=25)
    plt.barh(y=data.park_name, width=data.not_protected, color='#45AD3E')
    bars = plt.barh(y=data.park_name, width=data.protected, color='#FFAB70')
    data = data.reset_index(drop=True)
    for j, bar in enumerate(bars):
        plt.annotate(str(data.loc[j, '%age_protected'].round(1)) + '%',
            (bar.get_width() + bar.get_width()/10, bar.get_y() + bar.get_height()/2),
            fontsize=12, color='b')
    plt.yticks(rotation=0, fontsize=14)
    plt.xticks(np.arange(25,400,25))
    plt.xlabel('Number of Species', fontsize=12)
    plt.legend(handles=handles, fontsize=14)
    plt.grid(True)

plt.subplots_adjust(top=0.5)
plt.tight_layout()
plt.show()