import pandas as pd
import matplotlib.pyplot as plt
import datetime

def get_final_df():
    df_us = pd.read_csv('../data/youtube-new/USvideos.csv')
    df_fr = pd.read_csv('../data/youtube-new/FRvideos.csv')
    df_ca = pd.read_csv('../data/youtube-new/CAvideos.csv')
    df_de = pd.read_csv('../data/youtube-new/DEvideos.csv')
    df_gb = pd.read_csv('../data/youtube-new/GBvideos.csv')
    df_in = pd.read_csv('../data/youtube-new/INvideos.csv')
    df_jp = pd.read_csv('../data/youtube-new/JPvideos.csv', encoding='latin1')
    df_kr = pd.read_csv('../data/youtube-new/KRvideos.csv', encoding='latin1')
    df_mx = pd.read_csv('../data/youtube-new/MXvideos.csv', encoding='latin1')
    df_ru = pd.read_csv('../data/youtube-new/RUvideos.csv', encoding='latin1')
    df_us['region'] = 'North America'
    df_ca['region'] = 'North America'
    df_mx['region'] = 'North America'
    df_gb['region'] = 'Europe'
    df_fr['region'] = 'Europe'
    df_de['region'] = 'Europe'
    df_ru['region'] = 'Europe'
    df_kr['region'] = 'Asia'
    df_in['region'] = 'Asia'
    df_jp['region'] = 'Asia'
    frames = [df_us, df_ca, df_mx, df_gb, df_fr, df_de, df_ru, df_kr, df_jp, df_in]
    df_concat_data = pd.concat(frames)
    df_concat_data['net_likes']=df_concat_data['likes']-df_concat_data['dislikes']
    df_concat_data['like_ratio']=df_concat_data['likes']/(df_concat_data['likes']+df_concat_data['dislikes'])
    df_concat_data['twitter_ratio']=df_concat_data['likes']/df_concat_data['comment_count']
    return df_concat_data[['views','likes','dislikes', 'category_id', 'tags','net_likes','like_ratio','twitter_ratio', 'region']]

df_final = get_final_df()
json_categories = pd.read_json('../data/youtube-new/US_category_id.json')
id_map = {int(item["id"]) : item["snippet"]["title"] for item in json_categories["items"]}

data = df_final[['region','views','category_id']]
#region_groups = data.groupby('region')
#region_groups['views'].sum()
#region_groupcat = df_final[['region', 'views', 'category_id']].groupby(['region', 'category_id'])
#cata_views = region_groupcat['views'].sum()

asia = data[data['region'] == 'Asia']
asia['category_names'] = asia['category_id'].map(id_map)
asia_total_views = asia['views'].sum()
asia['percent_views'] = asia['views']/asia_total_views


asia_cat = asia.groupby('category_id')
percent_views = asia_cat.sum()['percent_views']
percent_views.plot.bar(title = 'Relative Popularity of Asian Categories')
#percent_views.plot.bar(title = 'Relative Popularity of Asian Categories', xticks= 'category_names')