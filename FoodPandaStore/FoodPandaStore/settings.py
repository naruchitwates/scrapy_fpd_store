# -*- coding: utf-8 -*-

# Scrapy settings for FoodPandaStore project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


from FoodPandaStore.FoodPandaStore.credentials import credentials


BOT_NAME = 'FoodPandaStore'

SPIDER_MODULES = ['FoodPandaStore.spiders']
NEWSPIDER_MODULE = 'FoodPandaStore.spiders'

# Database Connection String
CONNECTION_STRING = 'postgresql+psycopg2://{username}:{password}@{host}/{database}'.format(
    driver = credentials.get('DB_DRIVER', None),
    host = credentials.get('DB_HOST', None),
    username = credentials.get('DB_USERNAME', None),
    password = credentials.get('DB_PASSWORD', None),
    database = credentials.get('DB_NAME', None),
)

### S3 Storage
AWS_ACCESS_KEY_ID = credentials.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = credentials.get('AWS_SECRET_ACCESS_KEY', None)
IMAGES_STORE = credentials.get('AWS_BUCKET_URI', None)


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'FoodPandaStore (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 5
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'FoodPandaStore.middlewares.FoodpandastoreSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'FoodPandaStore.middlewares.FoodpandastoreDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'FoodPandaStore.pipelines.FoodpandastorePipeline': 100,
#    'FoodPandaStore.pipelines.FoodpandastoreInfoPipeline': 100
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

