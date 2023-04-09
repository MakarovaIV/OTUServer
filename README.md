# OTUServer

### Description
Homework 4 from OTUS.

TASK: Develop web server that partially implements the HTTP protocol.
The web server must be able to:
- Scale to multiple workers
- The number of workers is given by the command line argument -w
- Respond with 200, 403 or 404 to GET requests and HEAD requests
- Reply 405 to other requests
- Return files at an arbitrary path in DOCUMENT_ROOT.
- The /file.html call should return the contents of DOCUMENT_ROOT/file.html
- DOCUMENT_ROOT is given by the command line argument -r
- Return index.html as a directory index
- The /directory/ call should return DOCUMENT_ROOT/directory/index.html
- Respond with the following headers for successful GET requests: Date, Server,
- Content-Length, Content-Type, Connection
- Valid Content-Type for: .html, .css, .js, .jpg, .jpeg, .png, .gif, .swf
- Understand spaces and %XX in filenames

### Run
```commandline
python3 httpd.py -a HOST -p PORT -w NUM OF WORKERS -r DOCUMENTROOT 
```
where:
- `-a` - host address, by default `127.0.0.1`
- `-p` - port, by default `8080`
- `-w` - number of workers, by default `20`
- `-r` - DOCUMENT_ROOT, by default `tests`

### Run tests
```commandline
python3 -m unittest tests/httptest.py -v
```

### Perfomance testing
Run Web-server

```commandline
ab -n 50000 -c 100 -r http://127.0.0.1:8080/
```

Results
```commandline
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        OtuServer
Server Hostname:        localhost
Server Port:            8080

Document Path:          /
Document Length:        0 bytes

Concurrency Level:      100
Time taken for tests:   108.418 seconds
Complete requests:      50000
Failed requests:        11369
   (Connect: 0, Receive: 80, Length: 11209, Exceptions: 80)
Non-2xx responses:      28563
Total transferred:      7987200 bytes
HTML transferred:       3417120 bytes
Requests per second:    461.18 [#/sec] (mean)
Time per request:       216.836 [ms] (mean)
Time per request:       2.168 [ms] (mean, across all concurrent requests)
Transfer rate:          71.94 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    4  84.3      0    7228
Processing:     0  165 4142.3      1  107394
Waiting:        0    2 305.2      0   67775
Total:          0  170 4181.6      1  108416

Percentage of the requests served within a certain time (ms)
  50%      1
  66%      1
  75%      1
  80%      1
  90%      1
  95%      2
  98%      2
  99%      3
 100%  108416 (longest request)
```
Results with `num_of_workers` = 100
```commandline
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        OtuServer
Server Hostname:        localhost
Server Port:            8080

Document Path:          /
Document Length:        0 bytes

Concurrency Level:      100
Time taken for tests:   11.395 seconds
Complete requests:      50000
Failed requests:        10641
   (Connect: 0, Receive: 0, Length: 10641, Exceptions: 0)
Non-2xx responses:      28033
Total transferred:      7999360 bytes
HTML transferred:       3514080 bytes
Requests per second:    4387.93 [#/sec] (mean)
Time per request:       22.790 [ms] (mean)
Time per request:       0.228 [ms] (mean, across all concurrent requests)
Transfer rate:          685.56 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       2
Processing:     0    1   0.5      0      12
Waiting:        0    0   0.3      0      12
Total:          0    1   0.5      1      12
WARNING: The median and mean for the processing time are not within a normal deviation
        These results are probably not that reliable.

Percentage of the requests served within a certain time (ms)
  50%      1
  66%      1
  75%      1
  80%      1
  90%      1
  95%      1
  98%      2
  99%      3
 100%     12 (longest request)
```