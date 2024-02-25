import advertools as adv
import pandas as pd

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
all_sitemaps_df = pd.DataFrame(columns=['website', 'loc', 'lastmod'])

# Iterate over each sitemap URL
for sitemap_url in sitemap_urls:
    # Extract the domain name to use as the website column value
    website = sitemap_url.split("/")[2]
    
    # Get the sitemap data
    sitemap = adv.sitemap_to_df(sitemap_url)
    
    # Create a new DataFrame with 'loc' and 'lastmod' columns
    filtered_sitemap = pd.DataFrame({
        'website': website,  # Assign the website directly
        'loc': sitemap['loc'],
        'lastmod': sitemap['lastmod']
    })
    
    # Append to the all_sitemaps_df DataFrame
    all_sitemaps_df = pd.concat([all_sitemaps_df, filtered_sitemap], axis=0, ignore_index=True)

# Save the DataFrame to a CSV file
all_sitemaps_df.to_csv('consolidated_sitemaps2.csv', index=False)

print(all_sitemaps_df.head())  # Display the first few rows to verify
