import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def heatmap_github(df_repos):
    # Flatten the data to get a DataFrame with each commit date and corresponding repository
    flat_data = []
    for index, row in df_repos.iterrows():
        for commit_date in row['commits']:
            flat_data.append({'date': commit_date, 'repository': row['name']})

    df_flat = pd.DataFrame(flat_data)

    # Convert 'date' column to datetime format with day-first format
    df_flat['date'] = pd.to_datetime(df_flat['date'], format='%d-%m-%Y')

    # Create a date range for the last year
    end_date = df_flat['date'].max()
    start_date = end_date - pd.DateOffset(days=200)
    date_range = pd.date_range(start=start_date, end=end_date)

    # Count commits per day
    commit_counts = df_flat.groupby('date').size().reindex(date_range, fill_value=0)

    # Prepare hover information with repository details
    hover_data = df_flat.groupby('date')['repository'].apply(lambda x: '<br>'.join(set(x))).reindex(date_range, fill_value='')

    # Create a DataFrame for the heatmap
    heatmap_data = commit_counts.reset_index()
    heatmap_data.columns = ['date', 'count']
    heatmap_data['day_of_week'] = heatmap_data['date'].dt.day_name()
    heatmap_data['year'] = heatmap_data['date'].dt.isocalendar().year
    heatmap_data['week_of_year'] = heatmap_data['date'].dt.isocalendar().week

    # Merge hover data into heatmap data
    heatmap_data['hover_text'] = hover_data.values

    # Aggregate the data by 'day_of_week', 'year', and 'week_of_year' to ensure unique combinations
    heatmap_data_agg = heatmap_data.groupby(['day_of_week', 'year', 'week_of_year']).agg({'count': 'sum', 'hover_text': lambda x: '<br>'.join(set(x))}).reset_index()

    # Sort the DataFrame by year and week_of_year
    heatmap_data_agg = heatmap_data_agg.sort_values(by=['year', 'week_of_year'])


    # Create a combined year-week column for proper ordering
    heatmap_data_agg['year_week'] = heatmap_data_agg.apply(lambda row: f"Week {int(row['week_of_year']):02d} - {row['year']}", axis=1)

    # Pivot the DataFrame to get days as rows and weeks as columns
    heatmap_data_pivot = heatmap_data_agg.pivot(index='day_of_week', columns='year_week', values='count').fillna(0)
    hover_data_pivot = heatmap_data_agg.pivot(index='day_of_week', columns='year_week', values='hover_text').fillna('')

    heatmap_data_pivot = heatmap_data_pivot.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    hover_data_pivot = hover_data_pivot.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    heatmap_data_pivot = heatmap_data_pivot[heatmap_data_agg['year_week'].unique()]
    hover_data_pivot = hover_data_pivot[heatmap_data_agg['year_week'].unique()]

    custom_colorscale = [
        [0, 'lightgray'],  # Light color
        [0.001, 'white'],
        [1, 'green']   # Dark color
    ]

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data_pivot.values,
        x=heatmap_data_pivot.columns,
        y=heatmap_data_pivot.index,
        colorscale=custom_colorscale,
        customdata=hover_data_pivot.values,
        hovertemplate="<b>Year-Week</b>: %{x}<br>" +
                    "<b>Day of Week</b>: %{y}<br>" +
                    "<b>Number of Commits</b>: %{z}<br>" +
                    "<b>Repositories</b>: %{customdata}<br>" +
                    "<extra></extra>",
        hoverongaps=False
    ))

    # Function to create a rounded rectangle path with a hole in the middle

    def rounded_border_path(x0, y0, x1, y1, radius=0.2):
        path = f'M {x0+radius},{y0} ' \
            f'L {x1-radius},{y0} ' \
            f'Q {x1},{y0} {x1},{y0+radius} ' \
            f'L {x1},{y1-radius} ' \
            f'Q {x1},{y1} {x1-radius},{y1} ' \
            f'L {x0+radius},{y1} ' \
            f'Q {x0},{y1} {x0},{y1-radius} ' \
            f'L {x0},{y0+radius} ' \
            f'Q {x0},{y0} {x0+radius},{y0} Z'
        return path

    def rounded_rect_with_hole(x0, y0, x1, y1, radius=0.2):
        outer_path = f"M{x0},{y0} H{x1} V{y1} H{x0} Z"
        inner_path = rounded_border_path(x0+0.09, y0+0.09, x1-0.09, y1-0.09)
        return outer_path + " " + inner_path



    # Calculate the shape parameters for rounded rectangles
    shapes = []
    for i, row in enumerate(heatmap_data_pivot.index):
        for j, col in enumerate(heatmap_data_pivot.columns):
            x0 = j - 0.5
            x1 = j + 0.5
            y0 = i - 0.5
            y1 = i + 0.5

            # Rectangle with a hole
            shapes.append({
                'type': 'path',
                'path': rounded_rect_with_hole(x0, y0, x1, y1),
                'line': {
                    'color': 'white',
                    'width': 1
                },
                'fillcolor': 'white',
                'xref': 'x',
                'yref': 'y'
            })

            shapes.append({
                'type': 'path',
                'path': rounded_border_path(x0+0.1, y0+0.1, x1-0.1, y1-0.1),
                'line': {
                    'color': 'lightgray',
                    'width': 1
                },
                'fillcolor': 'rgba(0,0,0,0)',
                'xref': 'x',
                'yref': 'y'
            })

    fig.update_traces(
        showscale=False
    )
    
    # Convert 'Week XX - YYYY' to 'Month YYYY'
    def week_to_month_year(week_year_str):
        # Parse week and year from the string
        week, year = map(int, week_year_str.replace('Week ', '').split(' - '))
        
        # Convert to a datetime object representing the first day of the week
        date = datetime.strptime(f'{year} {week} 1', '%Y %W %w')
        
        # Format the datetime object to 'Month YYYY'
        return date.strftime('%B %Y')

    month_year_labels = [week_to_month_year(label) for label in heatmap_data_pivot.columns]
    first_occurrences = [month_year_labels.index(label) for label in sorted(set(month_year_labels), key=month_year_labels.index)]




    fig.update_layout(
        yaxis=dict(tickmode='array', 
                tickvals=np.arange(7), 
                ticktext=['', 'Tue', '', 'Thu', '', 'Sat', ''], 
                showgrid=False, 
                zeroline=False,
                scaleanchor="x",  # Ensure the y-axis is scaled equally to the x-axis
                scaleratio=1,
                tickfont=dict(size=20)),
        shapes=shapes,
        plot_bgcolor='white',  # Set the background color to white
        paper_bgcolor='white',  # Set the paper background color to white
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(tickmode='array',
                tickvals=first_occurrences,
                ticktext=[month_year_labels[i].split(' ')[0] for i in first_occurrences],
                showgrid=False, 
                zeroline=False,
                tickfont=dict(size=10)),
        width=1000,
    )
    return fig

def languages_github(df_repos):
    # Assuming sorted_languages is your data
    colors = px.colors.qualitative.Plotly  # Use a color sequence



    # Calculate counts for each language
    language_counts = df_repos['language'].value_counts()


    # Sort by counts
    sorted_languages = language_counts.sort_values(ascending=True)

    # Make sure there are enough colors for all bars
    colors = colors * (len(sorted_languages.index) // len(colors)) + colors[:len(sorted_languages.index) % len(colors)]

    customdata = df_repos.groupby('language').agg({
        'name': lambda x: '<br>          '.join(x.tolist()),
        'stargazers_count': 'sum',
        'watchers_count': 'sum',
        'topics': lambda x: '<br>          '.join(list(set([item for sublist in x.tolist() for item in sublist])))

    })

    # Create histogram
    figure = go.Figure(data=[
        go.Bar(name='Repos per language', 
            y=sorted_languages.index, 
            x=sorted_languages.values, 
            orientation='h',
            width=0.1,
            marker=dict(
                color=colors,
                line=dict(width=0)
            ),
            customdata=customdata,
            hovertemplate="<b>Language</b>: %{y}<br>" +
                "<b>Number of Repositories</b>: %{x}<br>" +
                "<b>Repository Names</b>: %{customdata[0]}<br>" +
                "<b>Total Stars</b>: %{customdata[1]}<br>" +
                "<b>Total Watchers</b>: %{customdata[2]}<br>" +
                "<b>Topics</b>: %{customdata[3]}<br>" +
                "<extra></extra>"
            )
    ])

    figure.update_layout(#title="Number of Repositories per Language",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                        yaxis=dict(showgrid=False, 
                                    tickfont=dict(size=16),
                                    automargin=True,
                                    title_standoff=20,),
                        width=800,
                                    )
    return figure