import advertools as adv
import pandas as pd
from urllib.parse import urlparse, unquote
import re

def extract_cured_name(url):
    """
    Extracts a more readable name from a URL.
    """
    # Parse the URL to get the path
    path = urlparse(unquote(url)).path
    # Remove leading and trailing slashes
    path = path.strip('/')
    # Take the last part of the path as the potential title
    name = path.split('/')[-1]
    # Remove common file extensions and URL parameters
    name = re.sub(r'\.\w+$', '', name).split('?')[0]
    # Replace hyphens with spaces for readability
    name = name.replace('-', ' ').strip()
    # Check if the name is just numeric (e.g., dates) or empty and return an empty string in those cases
    if name.replace(' ', '').isdigit() or not name:
        return ''
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

# Process each sitemap URL
for sitemap_url in sitemap_urls:
    # Extract the domain name to use as the website column value
    website = urlparse(sitemap_url).netloc
    
    # Get the sitemap data
    sitemap = adv.sitemap_to_df(sitemap_url)
    
    # Format the lastmod date and extract the cured name
    sitemap['lastmod'] = pd.to_datetime(sitemap['lastmod']).dt.strftime('%Y %m %d')
    sitemap['cured_name'] = sitemap['loc'].apply(extract_cured_name)
    
    # Create a new DataFrame with the required columns
    filtered_sitemap = pd.DataFrame({
        'website': website,
        'loc': sitemap['loc'],
        'lastmod': sitemap['lastmod'],
        'cured_name': sitemap['cured_name']
    })
    
    # Append to the consolidated DataFrame
    all_sitemaps_df = pd.concat([all_sitemaps_df, filtered_sitemap], ignore_index=True)

# Save the DataFrame to a CSV file
all_sitemaps_df.to_csv('consolidated_sitemapsv3.csv', index=False)

# Print the first few rows to verify
print(all_sitemaps_df.head())
