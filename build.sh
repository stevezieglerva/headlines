echo "*** Running tests"
python -m coverage run --source . -m unittest discover
coverage report --include get_feeds.py


echo "*** Removing old files ..."
rm headlines_site/content/first_headline/*.*
rm headlines_site/content/second_headline/*.*
rm headlines_site/content/fringe/*.*


echo "*** Creating RSS content pages ..."
python3 get_feeds.py

echo "*** Building site ..."
cd headlines_site
hugo

echo "*** Uploading site ..."
aws s3 sync public/ s3://onlineheadlines.net --delete --cache-control max-age=60
aws s3 sync public/ s3://www.onlineheadlines.net --delete --cache-control max-age=60

echo "*** Invalidating the CloudFront cache to refresh content"
aws cloudfront create-invalidation  --distribution-id E24F2WMFORZD5S --paths "/*"

cd ..
