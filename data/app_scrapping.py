import pandas as pd
import numpy as np
from tqdm import tqdm

from google_play_scraper import Sort, reviews

from helper import get_top_10_app_ids

app_packages_US = get_top_10_app_ids(country='US')
app_packages_BR = get_top_10_app_ids(country='BR')
app_packages = list(set(app_packages_BR+app_packages_US))

languages = ['en','pt']

app_reviews = []

for ap in tqdm(app_packages):
    for lang in languages:
        for score in list(range(1, 6)):
            for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
                rvs, _ = reviews(
                    ap,
                    lang=lang,
                    #country='',
                    sort=sort_order,
                    count= 100 if score <= 3 else 150,
                    filter_score_with=score
                )
                for r in rvs:
                    r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
                    r['appId'] = ap
                    r['lang'] = lang
                
                app_reviews.extend(rvs)

df = pd.DataFrame(app_reviews)

columns = ['content','score','appId','lang']
df = df[columns]

conditions = [
    (df['score'] <=  3),
    (df['score'] >  3)    
    ]
choices = ['negative','positive']
df['label'] = np.select(conditions, choices)

df.to_csv('reviews.csv', index=None, header=True, quoting=1)
