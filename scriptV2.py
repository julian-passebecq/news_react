import advertools as adv
import pandas as pd
from urllib.parse import unquote
import re

# Function to extract and cure the name from the URL
def extract_cured_name(url):
    url = unquote(url)  # Decode URL
    name = url.split('/')[-1]  # Get the last part of the URL
    name = name.split('?')[0]  # Remove URL parameters
    name = name.replace('-', ' ')  # Replace hyphens with spaces
    name = re.sub(r'\.\w+$', '', name)  # Remove file extensions
    return name

# List of sitemap URLs to process
sitemap_urls = [
    'https://www.kevinrchant.com/post-sitemap.xml',
    'https://thomas-leblanc.com/sitemap-1.xml',
    'https://www.oliviertravers.com/post-sitemap.xml',
    'https://data-mozart.com/post-sitemap.xml',
    'https://www.sqlbi.com/wp-sitemap-posts-post-1.xml',
    'https://en.brunner.bi/blog-posts-sitemap.xml',
    'https://pragmaticworks.com/sitemap.xml',
    'https://data-marc.com/sitemap.xml',
    'https://www.data-traveling.com/sitemap.xml',
    'https://datasavvy.me/sitemap.xml',
    'https://www.thatbluecloud.com/sitemap-posts.xml',
]

# Initialize an empty DataFrame to hold all the data
all_sitemaps_df = pd.DataFrame()

# Iterate over each sitemap URL
for sitemap_url in sitemap_urls:
    # Extract the domain name to use as the website column value
    website = sitemap_url.split("/")[2]
    
    # Get the sitemap data
    sitemap = adv.sitemap_to_df(sitemap_url)
    
    # Cure the lastmod date
    sitemap['lastmod'] = pd.to_datetime(sitemap['lastmod']).dt.strftime('%Y %m %d')
    
    # Extract and cure the name
    sitemap['cured_name'] = sitemap['loc'].apply(extract_cured_name)
    
    # Create a new DataFrame with the required columns and the website column
    filtered_sitemap = sitemap[['loc', 'lastmod', 'cured_name']].copy()
    filtered_sitemap['website'] = website
    
    # Append to the all_sitemaps_df DataFrame
    all_sitemaps_df = pd.concat([all_sitemaps_df, filtered_sitemap], axis=0, ignore_index=True)

# Save the DataFrame to a CSV file
all_sitemaps_df.to_csv('consolidated_sitemaps3.csv', index=False)

# Display the first few rows to verify
print(all_sitemaps_df.head())
