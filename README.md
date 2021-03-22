# Crawler

Parsing law organizations by crawler
***
### Deploy scrapy project

For deploy project to [Scrapyd](https://github.com/scrapy/scrapyd) server we will use library [Scrapyd-client
](https://github.com/scrapy/scrapyd-client) which allows to do it.

##### Deploying a Project

Install Scrapyd-client: `pip install scrapyd-client`

Inside the project in the `scrapy.cfg` file set the following settings:
```
[deploy]
url = <remote url scrapyd instance>
project = crawler-master
username = username
password = password
```
Then in the terminal execute the following command:
`scrapyd-deploy`.

After this automates the process of building the egg and pushing it to the target Scrapyd server.



