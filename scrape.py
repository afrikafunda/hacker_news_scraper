import requests
from bs4 import BeautifulSoup
import pprint

# Fetch the content of the first page of Hacker News
res = requests.get('https://news.ycombinator.com/news')

# Fetch the content of the second page of Hacker News
res2 = requests.get('https://news.ycombinator.com/news?p=2')

# Fetch the content of the second page of Hacker News
soup = BeautifulSoup(res.text, 'html.parser')
# Parse the HTML content of the second page using Beautiful Soup
soup2 = BeautifulSoup(res2.text, 'html.parser')
# Select all the story links from the first page
links = soup.select('.titleline > a') 
# Select all the subtext elements (which contain vote information) from the first page
subtext = soup.select('.subtext')
# Select all the story links from the second page
links2 = soup2.select('.titleline > a') 
# Select all the subtext elements (which contain vote information) from the first page
subtext2 = soup2.select('.subtext')

# Combine the story links and subtext elements from both pages
mega_links = links + links2
mega_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
  """
    Sort the Hacker News stories by the number of votes in descending order.
    
    Parameters:
    hnlist (list): List of dictionaries containing Hacker News stories with votes.
    
    Returns:
    list: Sorted list of stories by votes in descending order.
    """
  return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
  """
    Create a custom list of Hacker News stories with more than 99 votes.
    
    Parameters:
    links (list): List of BeautifulSoup elements containing the story links.
    subtext (list): List of BeautifulSoup elements containing the subtext (votes).
    
    Returns:
    list: List of dictionaries containing the title, link, and votes of each story.
    """
  hn = []
  for idx, item in enumerate(links):
    title = item.getText() # Get the title of the story
    href = item.get('href', None) # Get the URL of the story
    vote = subtext[idx].select('.score') # Get the vote element

    # Check if the story has votes
    if len(vote):
      points = int(vote[0].getText().replace(' points', ''))  # Extract the number of votes
      # Include the story if it has more than 99 votes
      if points > 99:
        hn.append({'title': title, 'link': href, 'votes': points})
  return sort_stories_by_votes(hn)

# Create the custom Hacker News list and print it using pprint for better readability
pprint.pprint(create_custom_hn(mega_links, mega_subtext))
