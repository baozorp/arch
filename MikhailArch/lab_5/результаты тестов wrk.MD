# Тесты WRK

| Тест          | Avg Latency | Stdev Latency | Max Latency | +/- Stdev | Avg Req/Sec | Total Requests | Total Transfer |
|---------------|-------------|---------------|-------------|-----------|--------------|----------------|----------------|
| Без Redis     | 76.03ms     | 27.69ms       | 704.39ms    | 92.95%    | 334.61       | 40035          | 139.24MB       |
| С Redis       | 46.84ms     | 22.01ms       | 438.24ms    | 91.84%    | 553.28       | 66126          | 28.63MB        |


## Тест без Redis
baozorp@MacBook-Air Architectory % wrk -t4 -c100 -d30s 'http://localhost:8080/api/users/show_all_users?offset=0&limit=100'
Running 30s test @ http://localhost:8080/api/users/show_all_users?offset=0&limit=100
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    76.03ms   27.69ms 704.39ms   92.95%
    Req/Sec   334.61     58.26   500.00     69.82%
  40035 requests in 30.06s, 139.24MB read
Requests/sec:   1331.96
Transfer/sec:      4.63MB

## Тест с redis
baozorp@MacBook-Air Architectory % wrk -t4 -c100 -d30s 'http://localhost:8080/api/users/show_all_users?offset=0&limit=100' 

Running 30s test @ http://localhost:8080/api/users/show_all_users?offset=0&limit=100
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    46.84ms   22.01ms 438.24ms   91.84%
    Req/Sec   553.28    127.31   800.00     75.59%
  66126 requests in 30.05s, 28.63MB read
Requests/sec:   2200.48
Transfer/sec:      0.95MB