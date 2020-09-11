# headlines

Headlines is a simple news application that gathers the first major headlines from several mixed sources based on the [Media Bias Chart](https://www.adfontesmedia.com/). I focused on the Left and Right views from the "Most Reliable" box. It's meant to provide a mixed view of content without the bias of content algorithms. I'm sick of headlines in my feeds matching this regex: 
```
(Trump|Graham|McConnell|Pelosi|Schumer).* tried to .* and it didn't end well.
```

It's published at [https://onlineheadlines.net](https://onlineheadlines.net).

## Tech Stack
* [Python script](get_feeds.py) to create markdown content files
* Hugo static site generator using the [hugo-xmag](https://themes.gohugo.io/hugo-xmag/) theme to give it a newspaper feel
* Docker container to run the build
* AWS ECS to run the container
* AWS S3 website hosting
* AWS CloudFront for DNS routing and SSL cert


