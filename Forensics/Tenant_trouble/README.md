# Tenant trouble

## Presentation

It seems that a user account has been compromised, could you identify the account in question and the start of the attack?

(The IP addresses in the file have been replaced by a random set of addresses, so don't try anything on these IP addresses)

sha256 : 3bfe375726cbae2ba4b74ede74e057f4777d80925650b899119fb27055d7c70a
Format : Hero{YYYY-MM-DD;jane.doe@company.com}

## Solve 

The file given is a csv file with the following header:

```
$ head -n 1 winchester77_signin_logs_2024.csv 
CreationTime,Operation,UserId,ObjectId,ResultStatus,ClientIP,AppId,RequestId,CorrelationId
```

Those logs looks like to be about login, you can see successfull and failed attempt to login.

To have a better understanding of the logs you need to do a Statistic analysis on few fields.

* How many different user is there ?

* When does the logs start/end ?

* How many event per month ?

* How many failed/succeeded ? 


**USER reparition**: 

```
$ cat winchester77_signin_logs_2024.csv | cut -d"," -f3 | sort | uniq 
catherine.debourgh@winchester77.onmicrosoft.com
charles.bingley@winchester77.onmicrosoft.com
elizabeth.bennet@winchester77.onmicrosoft.com
fiztwilliam.darcy@winchester77.onmicrosoft.com
george.wickham@winchester77.onmicrosoft.com
jane.bennet@winchester77.onmicrosoft.com
lydia.bennet@winchester77.onmicrosoft.com
mister.bennet@winchester77.onmicrosoft.com
UserId

$ cat winchester77_signin_logs_2024.csv | cut -d"," -f3 | sort | uniq | wc -l
9
```

There is 8 user account

**Date range** :

```
$ cat winchester77_signin_logs_2024.csv | cut -d"," -f1 | head -n 2
CreationTime
2024-01-01T08:20:33Z

$ cat winchester77_signin_logs_2024.csv | cut -d"," -f1 | tail -n 1
2024-10-25T17:53:20Z
```

The date range start from January,01 and goes until October, 25.

**Event reparition**:


```
$ cat winchester77_signin_logs_2024.csv | cut -d"-" -f1,2 | sort | uniq -c
    192 2024-01
    169 2024-02
    164 2024-03
    182 2024-04
    224 2024-05
    188 2024-06
    216 2024-07
    216 2024-08
    214 2024-09
    182 2024-10
```

There is no high peak

One common attack linked to account compromission is any kind of brute-force :

We gotta check the success/fail reparition :

```
$ cat winchester77_signin_logs_2024.csv | cut -d"," -f5 | sort | uniq -c
    457 Failed
   1490 Succeeded
```

and fail per user 

```
$ cat winchester77_signin_logs_2024.csv | grep "Failed" | cut -d"," -f3 | sort | uniq -c
      6 catherine.debourgh@winchester77.onmicrosoft.com
      3 charles.bingley@winchester77.onmicrosoft.com
     20 elizabeth.bennet@winchester77.onmicrosoft.com
      5 fiztwilliam.darcy@winchester77.onmicrosoft.com
     15 george.wickham@winchester77.onmicrosoft.com
     20 jane.bennet@winchester77.onmicrosoft.com
     24 lydia.bennet@winchester77.onmicrosoft.com
    364 mister.bennet@winchester77.onmicrosoft.com
```

Now we can see a really high peak of fail for user *mister.bennet@winchester77.onmicrosoft.com*


When did the brute-force happened ?

```
$ cat winchester77_signin_logs_2024.csv | grep "Failed" | grep "mister.bennet@winchester77.onmicrosoft.com" | cut -d"T" -f1 | sort | uniq -c
      1 2024-01-15
      4 2024-05-02
      2 2024-05-03
      4 2024-05-06
      3 2024-05-07
    ...
```

There was a lot of hit, the attackant tried to be discreet by doing verry little attempt per day some days. That was really targetted ^^'

Some would jump into thinking that the attack started 2024/01/15 but let's take a look on what happened this day :

```
$ cat winchester77_signin_logs_2024.csv | grep "mister.bennet@winchester77.onmicrosoft.com" | grep 2024-01-15
2024-01-15T10:26:37Z,UserLoggedIn,mister.bennet@winchester77.onmicrosoft.com,Login,Succeeded,144.231.115.9,Azure Active Directory,600dd015-ea6f-4422-a956-098c3f459479,26e764f7-5280-4c98-be72-3908838a1e94
2024-01-15T15:01:05Z,UserLoginFailed,mister.bennet@winchester77.onmicrosoft.com,Login,Failed,163.41.99.114,Azure Active Directory,4921487c-99a2-418d-bd31-f6b049b9f291,484eb89-2331-498e-b982-5f6be710e0g1
2024-01-15T15:02:16Z,UserLoggedIn,mister.bennet@winchester77.onmicrosoft.com,Login,Succeeded,163.41.99.114,Azure Active Directory,1021487c-99a2-418d-bd31-f6b049b9f291,404fbaf6-2f31-418e-b9a2-5f6be714e031
```

Mister bennet logged-in in the morning at 10am, and another time a 3pm. There is one fail but this happen right before a successfull attempt from the same IP addresses.

This is a normal user behavior, sometimes we mess up with our password.

There was no fail from January to May so we can conclude that the attack started back in the 2024-05-02.

**flag: HERO{2024-05-02;mister.bennet@winchester77.onmicrosoft.com}**
