# BankRupst

### Category

Pwn

### Description

BankRupst is a bank operating in bankruptcy where no laws are applicable.

Build: cargo build --target x86_64-unknown-linux-musl --release

Format : **Hero{flag}**<br>
Author : **ghizmo**

### Files

- chall
- bankrupst.rs

### Write Up

#### TL;DR

- no break in exit option, leading to UAF
- 1, 2-100 (13x), 6, 1, 2-100, 4

#### Analysis

The source code is provided and shows that everything is [unsafe](https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html).

Menu:
- 1) Insert BankRupst card
- 2) Deposit
- 3) Withdraw
- 4) Check Balance
- 5) Remove BankRupst card
- 6) Exit

Option 1 allocates a BankAccount.
Option 2 allows for deposits.
Option 3 allows for withdrawals.
Option 4 checks the bank balance; if the balance is over 1337 we get the flag.
Option 5 removes the card.
Option 6 is for quitting.

However, option 6 does not have a break if the card is still inserted.
Moreover, we see that the deallocation logic between options 5 and 6 is different.
It therefore seems interesting to look into this aspect.


Option 5:
```rust
if opened {
    (*account).balance = 0;
    (*account).deposits = 0;
    ptr::drop_in_place(account);
    opened = false;
    println!("BankRupst card removed.");
} else {
    println!("You must insert your BankRupst card!");
}
```

Option 6:
```rust
if opened {
    (*account).balance = 0;
    (*account).deposits = 0;
    let layout = Layout::new::<BankAccount>();
    dealloc(account as *mut u8, layout);
    account = ptr::null_mut();
    opened = false;
    println!("Thank you for using BankRupst!");
} else {
    println!("Thank you for using BankRupst!");
    break;
}
```

In option 6 we can see an UAF, and the program continues since there is not exit.
So we can alloc again with option 1 and continue deposit to get the flag.


#### Exploitation

```
1
2-100 (13 times)
6
1
2-100
4
```


### Flag

Hero{B4nkk_Rupst3dDd!!1x33x7}
