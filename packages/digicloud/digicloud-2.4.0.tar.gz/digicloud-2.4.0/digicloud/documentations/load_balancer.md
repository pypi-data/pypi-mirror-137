Load Balancer

Load balancing refers to the process of distributing a set of tasks over a set of resources,
with the aim of making their overall processing more efficient.
Load balancing can optimize the response time and avoid unevenly overloading some compute nodes
while other compute nodes are left idle.

## Examples:

1 **Create a Load Balancer**

    $ digicloud load balancer create 
        --name my_load_balancer_name
        --description "My load balancer description"
2 **List Load Balancer**

    $ digicloud load balancer list
3 **Load Balancer details**

    $ digicloud load balancer show my_load_balancer_name
4 **Update a Load balancer**

    $ digicloud load balancer update my_load_balancer_name
        --name my_new_load_balancer_name
        --description "My load balancer description"
        --delay 10
        --timeout 5
        --max-retries 3
        --path /newpath
        --http-version 1.1
        --http-method GET
        --algorithm round_robin
5 **Delete a Load Balancer**

    $ digicloud load balancer delete my_load_balancer_name

Application

A load balancer contain an application. Application is the placeholder of your backend and frontend.

## Examples:

6 **Create Application**

    $ digicloud load balancer application create
        my_load_balancer
        --port 8008
        --algorithm source_ip

Backend Member

Backend member is the end part of load balancer, where your instance do a task.
You should provide resource_id, ip_address and also port of your instance.

## Examples:
7 **Create Backend Member**

    $ digicloud load balancer member add
        my_load_balancer
        --resource-id my_resource_id
        --ip-address 1.1.1.1
        --port 8000
8 **Delete a Backend Member**

    $ digicloud load balancer member delete
        my_load_balancer
        my_backend_member


Health Check

Health check try to check your backend members. Is your instance ready to do any task or not.

## Examples:

9 **Create Health Check**

    $ digicloud load balancer health check create
        my_load_balancer
        --delay 10
        --timeout 10
        --max-retries 3
        --path "/"
        --http-version 1.0/1.1
        --http-method GET/POST
