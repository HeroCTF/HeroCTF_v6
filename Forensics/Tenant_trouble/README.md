# Tenant trouble

TODO


Statistic analysis

```
$ cat winchester77_signin_logs_2024.csv | cut -d"," -f3 | sort | uniq -c | sort -g
      1 UserId
     48 fiztwilliam.darcy@winchester77.onmicrosoft.com
    191 charles.bingley@winchester77.onmicrosoft.com
    194 george.wickham@winchester77.onmicrosoft.com
    206 catherine.debourgh@winchester77.onmicrosoft.com
    214 lydia.bennet@winchester77.onmicrosoft.com
    215 elizabeth.bennet@winchester77.onmicrosoft.com
    217 jane.bennet@winchester77.onmicrosoft.com
    663 mister.bennet@winchester77.onmicrosoft.com
```


```
cat winchester77_signin_logs_2024.csv | grep Fail | cut -d"," -f3 | sort | uniq -c | sort -g
      3 charles.bingley@winchester77.onmicrosoft.com
      5 fiztwilliam.darcy@winchester77.onmicrosoft.com
      6 catherine.debourgh@winchester77.onmicrosoft.com
     15 george.wickham@winchester77.onmicrosoft.com
     20 elizabeth.bennet@winchester77.onmicrosoft.com
     20 jane.bennet@winchester77.onmicrosoft.com
     24 lydia.bennet@winchester77.onmicrosoft.com
    366 mister.bennet@winchester77.onmicrosoft.com

```

compte: mister.bennet@winchester77.onmicrosoft.com




start date


```
$ cat winchester77_signin_logs_2024.csv | grep Fail | grep mister | cut -d"T" -f1 | sort | uniq -c | sort -g
      1 2024-01-15
      1 2024-05-09
      1 2024-05-13
      1 2024-05-14
      1 2024-05-16
      1 2024-05-20
      1 2024-05-28
      1 2024-06-03

```

but if if u pay attention 

```
cat winchester77_signin_logs_2024.csv | grep Fail | grep mister | cut -d"," -f1 | sort | uniq -c | sort -g
      1 2024-01-15T15:01:05Z
      1 2024-05-02T11:05:37Z
```
 u can be tempted to say 2024-01-15T15:01:05Z

 but

 ```
 $ cat winchester77_signin_logs_2024.csv | grep mister | cut -d"," -f1,4-6
 ...
     1 2024-01-12T18:22:50Z,Login,Succeeded,12.183.78.167
      1 2024-01-15T10:26:37Z,Login,Succeeded,144.231.115.9
      1 2024-01-15T15:01:05Z,Login,Failed,163.41.99.114
      1 2024-01-15T15:02:16Z,Login,Succeeded,163.41.99.114
      1 2024-01-16T09:06:58Z,Login,Succeeded,69.120.197.233
      1 2024-01-16T09:18:49Z,Login,Succeeded,93.213.101.161

 ```

It looks like a regular user first failed and Success to login, real attack start 

```
2024-05-02
```


flag: 

HERO{2024-05-02;mister.bennet@winchester77.onmicrosoft.com}
