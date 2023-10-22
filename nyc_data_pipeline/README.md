# NYC Data Fetching Classes Documentation

This documentation covers three classes, `NYCPublicDataFetcher`, `NYCEndpointFetcher`, and `NYCUrlFetcher`, designed to streamline the fetching of public data from New York City's websites. These classes make use of asynchronous fetching and web scraping techniques to efficiently extract and provide data.

## Dependencies

- `requests`
- `BeautifulSoup` from `bs4`
- `logging`
- `subprocess`
- `aiohttp`
- `os`
- `random`

## NYCPublicDataFetcher Class

The `NYCPublicDataFetcher` class is designed to fetch content from a starting URL and extract view IDs and their corresponding links.

### Core Methods

1. **fetch_content(url: str)**: Asynchronously fetches content from a given URL.
2. **extract_view_ids_and_links(content: str)**: Extracts view IDs and links from the given content.
3. **run()**: Fetches content from the start URL and extracts the data.

Usage:
```python
fetcher = NYCPublicDataFetcher(start_url="https://example.com")
data = fetcher.run()


```

# **`NYCEndpointFetcher` Class Overview**

## NYCEndpointFetcher Class

The `NYCEndpointFetcher` class fetches content from URLs and extracts API endpoints.

### Core Methods

1. **fetch_content(url: str)**: Asynchronously fetches content from a given URL and extracts the API endpoint.
2. **bash_resource_link(file_name: str)**: Extracts the resource link from a file using a bash command.
3. **run(data_dict: dict)**: Fetches content from URLs in the data dictionary and extracts endpoints.

Usage:
```python
endpoint_fetcher = NYCEndpointFetcher()
endpoints = endpoint_fetcher.run(data_dict)

```


---

# **`NYCUrlFetcher` Class Overview**
```markdown
## NYCUrlFetcher Class

The `NYCUrlFetcher` class fetches content from a URL and extracts data category URLs using different user agents to avoid blocking.

### Core Methods

1. **fetch_content(url: str)**: Asynchronously fetches content from a URL and saves the content to a file.
2. **extract_data(html_content: str)**: Extracts data category URLs from the HTML content.
3. **run(url: str)**: Fetches content from a given URL and extracts data categories.

Usage:
```python
url_fetcher = NYCUrlFetcher()
data_categories = url_fetcher.run(url="https://example.com")

```


## Usage

Initialize the desired class and call its `run()` method with the appropriate arguments:

```python
fetcher = NYCPublicDataFetcher(start_url="https://data.cityofnewyork.us/browse")
data = fetcher.run()

endpoint_fetcher = NYCEndpointFetcher()
endpoints = endpoint_fetcher.run(data)

url_fetcher = NYCUrlFetcher()
categories = url_fetcher.run(url="https://data.cityofnewyork.us/browse")
