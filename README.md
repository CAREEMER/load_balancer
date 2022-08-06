# Dynamic load balancer written in Python 3.10.5

## Env variables:
    - HOST: "0.0.0.0"
    - PORT: 8888
    - UPSTREAM-{index: int - starting with 0}: json {"domain": "app.localhost", "pool": ["host_1:port_1", "host_2:port_2", "host_3:port_3"], "default": true}