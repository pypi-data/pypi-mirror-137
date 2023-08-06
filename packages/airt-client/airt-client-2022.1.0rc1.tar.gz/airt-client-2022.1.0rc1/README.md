# Python client for airt service 2022.1.0rc1

A python library encapsulating airt service REST API available at:

- <a href="https://api.airt.ai/docs" target="_blank">https://api.airt.ai/</a>

## Docs

Full documentation can be found at the following link:

- <a href="https://docs.airt.ai" target="_blank">https://docs.airt.ai/</a>


## How to install

If you don't have the airt library already installed, please install it using pip.


```console
pip install airt-client
```

## How to use

Before you can use the service, you must acquire a username and password for your developer account. Please fill in the following form to get one:

- [https://bit.ly/3hbXQLY](https://bit.ly/3hbXQLY)

Upon successfully receiving a username/password pair, you have to call the `Client.get_token` method in the `Client` class for getting an application token. 

The username, password, and server address can either be passed explicitly while calling the `Client.get_token` method or stored in environment variables **AIRT_SERVICE_USERNAME**, **AIRT_SERVICE_PASSWORD**, and **AIRT_SERVER_URL**. After successful authentication, you will receive an application token and will be able to access airt services.

Below is a minimal example explaining how to train a model and make predictions using airt services. 

The example assumes the username, password, and server address required for authenticating the `Client` is stored in the environment variables **AIRT_SERVICE_USERNAME**, **AIRT_SERVICE_PASSWORD**, and **AIRT_SERVER_URL** respectively.

For more information, please check:

- [Tutorial](https://docs.airt.ai/Tutorial/) with more elaborate example, and

- [API](https://docs.airt.ai/API/client/Client/) with reference documentation.


### 0. Get token


```python
from airt.client import Client, DataSource

Client.get_token()
```

### 1. Connect data


```python
data_source_s3 = DataSource.s3(
    uri="s3://test-airt-service/ecommerce_behavior"
)

data_source_s3.pull().progress_bar()
print(data_source_s3.head())
```

    100%|██████████| 1/1 [03:11<00:00, 192.00s/it]

                      event_time event_type  product_id          category_id  \
    0  2019-11-01 00:00:00+00:00       view     1003461  2053013555631882655   
    1  2019-11-01 00:00:00+00:00       view     5000088  2053013566100866035   
    2  2019-11-01 00:00:01+00:00       view    17302664  2053013553853497655   
    3  2019-11-01 00:00:01+00:00       view     3601530  2053013563810775923   
    4  2019-11-01 00:00:01+00:00       view     1004775  2053013555631882655   
    5  2019-11-01 00:00:01+00:00       view     1306894  2053013558920217191   
    6  2019-11-01 00:00:01+00:00       view     1306421  2053013558920217191   
    7  2019-11-01 00:00:02+00:00       view    15900065  2053013558190408249   
    8  2019-11-01 00:00:02+00:00       view    12708937  2053013553559896355   
    9  2019-11-01 00:00:02+00:00       view     1004258  2053013555631882655   
    
                   category_code     brand   price    user_id  \
    0     electronics.smartphone    xiaomi  489.07  520088904   
    1  appliances.sewing_machine    janome  293.65  530496790   
    2                       None     creed   28.31  561587266   
    3  appliances.kitchen.washer        lg  712.87  518085591   
    4     electronics.smartphone    xiaomi  183.27  558856683   
    5         computers.notebook        hp  360.09  520772685   
    6         computers.notebook        hp  514.56  514028527   
    7                       None   rondell   30.86  518574284   
    8                       None  michelin   72.72  532364121   
    9     electronics.smartphone     apple  732.07  532647354   
    
                               user_session  
    0  4d3b30da-a5e4-49df-b1a8-ba5943f1dd33  
    1  8e5f4f83-366c-4f70-860e-ca7417414283  
    2  755422e7-9040-477b-9bd2-6a6e8fd97387  
    3  3bfb58cd-7892-48cc-8020-2f17e6de6e7f  
    4  313628f1-68b8-460d-84f6-cec7a8796ef2  
    5  816a59f3-f5ae-4ccd-9b23-82aa8c23d33c  
    6  df8184cc-3694-4549-8c8c-6b5171877376  
    7  5e6ef132-4d7c-4730-8c7f-85aa4082588f  
    8  0a899268-31eb-46de-898d-09b2da950b24  
    9  d2d3d2c6-631d-489e-9fb5-06f340b85be0  


    


### 2. Train


```python
from datetime import timedelta

model = data_source_s3.train(
    client_column="user_id",
    target_column="event_type",
    target="*purchase",
    predict_after=timedelta(hours=3),
)
model.progress_bar()
print(model.evaluate())
```

    100%|██████████| 5/5 [00:00<00:00, 121.12it/s]


                eval
    accuracy   0.985
    recall     0.962
    precision  0.934


### 3. Predict


```python
predictions = model.predict()
predictions.progress_bar()
print(predictions.to_pandas().head())
```

    100%|██████████| 3/3 [00:00<00:00, 75.22it/s]


                  Score
    user_id            
    520088904  0.979853
    530496790  0.979157
    561587266  0.979055
    518085591  0.978915
    558856683  0.977960

