# Package
Use this package to download and analyze twitter sentiments.
# Usage
Before using the package you need to set user parameters obtained by creating a twitter  
app first. The package will need to read the user data from your environment variables stored in the following dict format  

```
user_params = {
    "consumerKey": os.environ.get("consumerKey"),
    "consumerSecret": os.environ.get("consumerSecret"),
    "accessToken": os.environ.get("accessToken"),
    "accessTokenSecret": os.environ.get("accessTokenSecret"),
}
```
## Installation
Install the package as follows:  
`pip3 install twitcent`

## importing the module
In your script simply import the package as follows:  

`from twitcent.twitcent import sentiments_dict`

### Calling the analyzer
The sentiment analysis main function is 'sentiments_dict' which is called under the script as follows:  
`from twitcent.twitcent import sentiments_dict`

### Get the sentiments score by calling
Do this to get scored sentiments `sentiments_dict('#keyword', '180')`.  
Where #keyword is the main keyword hashtag to search, and '180' is a string referring to the number of tweets to pull.  
Be careful not to hit the rate limits allowed by twitter. For this reffer to the  
twitter [API documentation](URL "https://developer.twitter.com/en/docs/twitter-api/rate-limits")