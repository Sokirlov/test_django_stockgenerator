# Django test work
The task consists of two parts:  
1. Create a shop with dynamic pricing, where prices are updated every 5 seconds.  
2. Develop an order cart that calculates the final price based on the logic provided in the task.

In this project, I used the following technologies:  

- [Django Rest Framework](https://www.django-rest-framework.org/): To build a robust and scalable API.  
- [Djoser](https://djoser.readthedocs.io/): For user registration and authentication.  
- [Swagger](https://pypi.org/project/drf-yasg/#quickstart): To provide comprehensive API documentation.  
- [Celery](https://docs.celeryq.dev/en/latest/django/index.html): For handling asynchronous and scheduled tasks.  
- [PostgreSQL](https://hub.docker.com/_/postgres): As the primary database for data storage.  
- [Redis](https://hub.docker.com/_/redis): Used as a message broker to facilitate task queues and caching.  
- [Channels](https://channels.readthedocs.io/): To enable real-time communication via WebSocket for messaging.  
- [Docker](https://docs.docker.com/): To streamline development, deployment, and containerization of the project.  



----



This project include functionality:

- [Registration and authorization](#authentication) url: /auth/

- [Base logic](#models)

- [Api](#api_endpoints-)
- [Websocket](#websocket-) 

[//]: # ()

[//]: # ()
[//]: # (So, on index url you can view [swagger]&#40;'http://localhost:8000/'&#41;. It helps you with api endpoints)

[//]: # ()
[//]: # (It has products, currency prices and discounts.<br />)

[//]: # (The peculiarity is that prices for products that )

[//]: # (are added to discounts can be generated automatically )

[//]: # (using Celery or you can call it manually.)


## Authentication
**Djoser** provides authentication functionality, including:
- _User Management_: Create and verify users via email.  
- _Password Handling_: Change and reset passwords securely.  
- _Profile Updates_: Modify user data easily.  
- _Token Management_: Obtain and refresh authentication tokens.  

___
## MODELS
This application has that models Goods, Price, Sale, Order. <br> 
The models Goods and Price are has basic functionality that you can explore in [swagger](http://localhost:8000). 

- **Model Goods**
In the detailed view of **Goods**, you can see the complete history of all associated prices.


-  **Model Sale** 
To create a **SALE**, follow these steps:
   1. **Define Sale Details**: Set a `name`, `min_price`, and `max_price`.
   2. **Attach Goods**: Link the goods that will be included in the sale.

    ###### Price Generation
    - **Automated Task**: Use **Celery Beat** to schedule tasks at specific times or intervals.
    These tasks will dynamically generate new prices for the goods attached to the sale.  
    - **On-Demand Update**: Send a **PUT** request via the API to generate prices immediately. 
    Note that this action is rate-limited to one request every 5 seconds.
<br /><br />
- **Model Order** 

  Each user can view only their own orders.  
  When an order is created, it uses the price that was active at the moment of creation.  
  The order includes a field called `order_sum`, which represents the final price.  
        - This value is calculated based on the exchange rate at the time of the order.  
        - The logic for calculating the `order_sum` follows the rules specified in the task.

___


## API_Endpoints  

The API includes the following endpoints:  
- `/api/currency` – Show all currencies.  
- `/api/goods` – Manage goods information.  
- `/api/prices` – Handle prices for goods.  
- `/api/sales` – Manage sales and related tasks.  
- `/api/orders` – Create and view orders.  

You can explore these endpoints using:  

- **Swagger UI** – Interactive API documentation for easy testing and understanding.  
- **Browsable API (DRF HTML View)** – A user-friendly, web-based interface to test and interact with the endpoints.  

___

## Websocket 
 [ws://127.0.0.1:8000/ws/price_updates/](ws://127.0.0.1:8000/ws/price_updates/)
 
Documentation in progres...