---
layout: post
title: This Websites Is Now Available on IPFS, ENS, and Handshake
category: technology
tags: ipfs distributed
---

In the past few months there has been a lot of chatter about `web3` and what it means and doesn't mean for the future of the web. There's a lot of hype around NFTs, mostly because of the money that is exchanging hands, and instead of outright dismissing it I wanted to dive deeper to understand it better.

## Setting up an ENS Domain

I first thought about NFTs when I discovered you can buy [ENS Domains](https://ens.domains) and then set them up like a standard DNS name with the additional benefit of using them as an identity. I went through the ENS purchase - setting up [Coinbase Wallet](https://www.coinbase.com/wallet) - and buying the domain with some ETH. My overall impression was is there's a lot of fees. Registering the domain and other actions are relatively inexpensive, but the [gas fees](https://cryptocurrencysimple.com/all-you-must-know-about-what-are-eth-gas-fees/) are much higher and take up the bulk of the transaction cost. Skipping over all the details, it cost about 400$ to fully setup `eciptik.eth` - registering, reverse lookup to my wallet address, and setting the metadata.

The final results of setting up the ENS domain are here [ecliptik.eth](https://app.ens.domains/name/ecliptik.eth/details) and it resolves to  at [https://ecliptik.eth](https://ecliptik.eth.limo) on IPFS. This name also includes additional features like setting my [Avatar image to an NFT I own](https://medium.com/the-ethereum-name-service/nft-avatar-support-for-ens-profiles-bd4a5553f089) (which is one I created myself and put on [opensea.io](https://opensea.io) for free).

## Setting up a Handshake Domain

The next domain setup was [Handshake](https://handshake.org) which is a "Decentralized naming and certificate authority" and has an auction process to acquire a Handshake domain. I setup [Bob Wallet](https://bobwallet.io) and went through the [airdrop claim](https://github.com/handshake-org/hs-airdrop) to get some HNS. Eventually I ended up using [Namebase](https://www.namebase.io) to handle the auction and management details and after about 14 days (due to the auction process) I was the new owner of the `ecliptik` Handshake domain.

The one interesting thing I noticed is that the `ecliptik` domain was already up for auction when I checked. After some research I found that if you register an ENS domain name and it's not claimed on Handshake, there are bots that will automatically start and auction for it.  Because it was a bot and not someone else trying to buy it, I easily outbid and acquired the name with no counter bids. I also acquired a few other names like `amfora` and `rawtext` since I had some more HNS.

Accessing the HNS domain requires some additional software or using DNS servers that support it, the Namebase article [How to Access Handshake Sites](https://learn.namebase.io/starting-from-zero/how-to-access-handshake-sites) has how to set this all up.

Handshake names are also available using the `hns.to` domain, and mine is accessible at [https://ecliptik.hns.to](https://ecliptik.hns.to)

## Mirroring To IPFS

Now that I had the DNS and Handshake domains I had to figure out how to use them. ENS has a lot of documentation on using [IPFS](https://ipfs.io) to point an ENS domain to, and then it's fully part of the "Distributed Web". After doing some research I found that [Fleek.co](https://fleek.co) provides free Web, IPFS, ENS, and Handshake features. I followed their setup guide and now whenever I push to `main` on my [Github Pages repo](https://github.com/ecliptik/ecliptik.github.io), it automatically publishes it to IPFS using InterPlanetary Name System ([IPNS](https://docs.ipfs.io/concepts/ipns/)) which resolves the name `ecliptik.ens` to the current version of this blog.

Now whenever I publish to this blog, it's automatically updated on IPFS and available at [ipns://ecliptik.eth](ipns://ecliptik.eth), and via http at [https://ecliptik.eth.limo](https://ecliptik.eth.limo).

Accessing ENS and IPFS directly  requires some additional software outside of traditional browsers, but [Brave](https://brave.com) has support both for ENS and IPFS.

## Wrapping Up

Learning about ENS, Handshake, and IPFS was a lot of fun, and while I highly doubt that `web3` is "the future", these technologies have a lot of offer for the future of the Internet. I am particularly fond of IPFS as it reminds me of [Bittorrent](https://www.bittorrent.org) but without having to setup a torrent/magnet link and seed. Getting started with IPFS is easy, and hosting your own IPFS node locally is a quick and  free way to participate in the distributed web.

I really understood the power of IPFS when I saw the different ways you could use it as a [Gateway](https://docs.ipfs.io/concepts/ipfs-gateway/), enabling any application that uses http to access content on IPFS. This really shines with git and package repositories, see [OpenBSD 6.9 packages using IPFS](https://dataswamp.org/~solene/2021-05-01-ipfs-openbsd-69.html) for a real-world application.
