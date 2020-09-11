# headlines

Headlines is a simple news application that gathers the first major headlines from several mixed sources based on the [Media Bias Chart](https://www.adfontesmedia.com/). I focused on the Left and Right views from the "Most Reliable" box. It's meant to provide a mixed view of content without the bias of content algorithms. I'm was getting sick of headlines in my feeds matching this regex: 
```
(Trump|Graham|McConnell|Pelosi|Schumer).* tried to .* and it didn't end well.
```

This should help eliminate articles like that.

It's published at [https://onlineheadlines.net](https://onlineheadlines.net).

## Tech Stack
* [Python script](get_feeds.py#L57) to create markdown content files
* Hugo static site generator using the [hugo-xmag](https://themes.gohugo.io/hugo-xmag/) theme to give it a newspaper feel
* Docker [container](Dockerfile) to run the [build](build.sh)
* AWS ECS to run the container every hour
* AWS S3 website hosting
* AWS CloudFront for DNS routing and SSL cert


