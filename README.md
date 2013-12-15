mysqlcheck
==========

Health Check Daemon for Mysql Galera/Percona XtraDB -  Used for HAProxy Health Check


## HAProxy Config
```
listen dbcluster1
        bind *:3306
        mode tcp
        timeout client 60000ms
        timeout server 60000ms
        balance leastconn
        option httpchk HEAD /api/clustersize/3
        option allbackups
        default-server port 3305 inter 2s downinter 5s rise 3 fall 2 slowstart 60s maxconn 256 maxqueue 128 weight 100
        server 172.16.3.21_3306 172.16.3.21:3306 check
        server 172.16.3.22_3306 172.16.3.22:3306 check
        server 172.16.3.23_3306 172.16.3.23:3306 check
```
