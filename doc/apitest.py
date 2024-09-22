import requests

url = "https://api-mobile.soundcloud.com/search/query?client_id=dbdsA8b6V6Lw7wzu1x0T4CLxt58yd4Bf&limit=30&q=王菲&filter.content_type=all&version=v6&autocomplete_urn=soundcloud%3Asearch-autocomplete%3A966e6fc62c6142da8f1c84d7be2bad02&page=3"

payload = {}
headers = {
  'Accept': 'application/json; charset=utf-8',
  'ADID': '83b5d936-150e-41c9-bd2a-edbe5e04cae4',
  'ADID-TRACKING': 'true',
  'Authorization': 'OAuth 2-293571-1410263487-kCK3vEG4A5lqd',
  'App-Locale': 'en',
  'Device-Locale': 'en-US',
  'User-Agent': 'SoundCloud/2024.09.16-release (Android 13.0.0; Google Pixel 4)',
  'App-Version': '260090',
  'UDID': 'd047bfb9ffb6bddf6a6796e67936ef85',
  'App-Requested-Features': 'api_ios_podcast=,api_ios_reduced_price=,api_ios_test=,api_test=,system_playlist_in_library=true',
  'App-Environment': 'prod',
  'Cookie': 'datadome=2cXNw44WLZ91mmGJBI425QlzumxPdUfwljJNhaLXAlfoyqMPghMFPZDFcY_IFQgEgvBjCf_kzT~J8VWvUYgvUnkgK~Q1pVuH12OrYNBmvVALn7mJQSYUtvRae9XEW5cm',
  'Host': 'api-mobile.soundcloud.com'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
