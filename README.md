# ansible-modules
A few modules to make life in AWS context easier: dealing with subnet lookup and parsing/formatting strings with a sprintf function

# sprintf
This modules gives you the sprintf flexibility you sometimes need.  

This would be the basic example
```
- hosts: localhost

  tasks:

  - set_fact: msg="This is a short demo"

  - name: test the module
    debug: msg="{{ msg | sprintf('{0} {3}') }}"
```
Returning this output
```
ok: [localhost] => {
    "msg": "This short"
}
```

A more practical (and the reason i created it) example is perhaps parsing a zone file and creating Route53 record from it

```
zone file in this format (leaving out the MX NS  etc entries)

myserver 3600 IN A 10.0.0.1
mydb  3600 IN CNAME my-db-server.io
```
The playbook to parse this file and create records from it
```
- hosts: localhost

  tasks:

  - name: Parse zone file
    debug: msg="Server {{ item | sprintf('{0}') }} ttl {{ item | sprintf('{1}') }} IP {{ item | sprintf('{4}') }}"
    with_lines: cat zonefile
 ```
 This gives this output (I used debug but you can ofcourse use route53 or even curl if you wanted to use the GoDaddy API)
 ```
 ok: [localhost] => (item=myserver 3600 IN A 10.0.0.1) => {
    "item": "myserver 3600 IN A 10.0.0.1", 
    "msg": "Server myserver ttl 3600 IP 10.0.0.1"
}
ok: [localhost] => (item=mydb  3600 IN CNAME my-db-server.io) => {
    "item": "mydb  3600 IN CNAME my-db-server.io", 
    "msg": "Server mydb ttl 3600 IP my-db-server.io"
}
```

 
