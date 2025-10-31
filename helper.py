import numpy as np




def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = medal_df
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                    ascending=False).reset_index()
        x = x.sort_values('Year')
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def medal_tally(df):
    # Remove duplicate medal entries
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    # Group by region and sum medal counts
    medal_tally = (
        medal_tally.groupby('region')
        [['Gold', 'Silver', 'Bronze']]
        .sum()
        .sort_values('Gold', ascending=False)
        .reset_index()
    )

    # Add total column
    medal_tally['total'] = (
        medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    )

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')

    return years, country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year',col]) ['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col }, inplace=True)
    return nations_over_time
def most_successful(df, sport):
    # Remove rows with no medals
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if not 'overall'
    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals per athlete
    top_15 = temp_df['Name'].value_counts().reset_index().head(15)
    top_15.columns = ['Name', 'Medals']  # <-- renamed here

    # Merge with filtered temp_df (not original df)
    result = top_15.merge(temp_df, on='Name', how='left')

    # Select relevant columns
    final_result = result[['Name', 'Medals', 'Sport', 'region']].drop_duplicates()

    return final_result




def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df,country):
     temp_df = df.dropna(subset=['Medal'])
     temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

     new_df = temp_df[temp_df['region'] == country]

     pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
     return pt

# def most_successful_countrywise(df, country):
#     temp_df = df.dropna(subset=['Medal'])
#
#     # Filter by country
#     temp_df = temp_df[temp_df['region'] == country]
#
#     # Count medals per athlete
#     x = temp_df['Name'].value_counts().reset_index().head(15)
#     x.columns = ['Name', 'Medals']  # Rename columns properly
#
#     # Merge to get Sport and region info
#     x = x.merge(df[['Name','Sport','region']], on='Name', how='left').drop_duplicates('Name')
#
#     return x

# def most_successful_countrywise(df, country):
#     temp_df = df.dropna(subset=['Medal'])
#
#     temp_df = temp_df[temp_df['region'] == country]
#
#     x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
#         ['index', 'Name_x', 'Sport']].drop_duplicates('index')
#     x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return x

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    # Filter by country
    temp_df = temp_df[temp_df['region'] == country]

    # Count medals per athlete
    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'Medals']  # Rename columns properly

    # Merge to get Sport and region info
    x = x.merge(df[['Name','Sport','region']], on='Name', how='left').drop_duplicates('Name')

    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final