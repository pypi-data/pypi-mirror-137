# quick_client.DefaultApi

All URIs are relative to *http://quick-manager*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_gateway**](DefaultApi.md#create_gateway) | **POST** /gateway | Creates a new gateway
[**create_mirror**](DefaultApi.md#create_mirror) | **POST** /topic/mirror | Creates a mirror for a topic
[**create_new_topic**](DefaultApi.md#create_new_topic) | **POST** /topic/{name} | Creates a new topic
[**create_schema**](DefaultApi.md#create_schema) | **POST** /gateway/{name}/schema | Creates a new GraphQL schema
[**delete_application**](DefaultApi.md#delete_application) | **DELETE** /application/{name} | Deletes an application
[**delete_gateway**](DefaultApi.md#delete_gateway) | **DELETE** /gateway/{name} | Deletes a gateway
[**delete_mirror**](DefaultApi.md#delete_mirror) | **DELETE** /topic/{name}/mirror | Deletes mirror of topic
[**delete_topic**](DefaultApi.md#delete_topic) | **DELETE** /topic/{name} | Deletes topic
[**deploy_application**](DefaultApi.md#deploy_application) | **POST** /application | Deploys a new application
[**get_application_information**](DefaultApi.md#get_application_information) | **GET** /application/{name} | Retrieves information about the given application
[**get_applications**](DefaultApi.md#get_applications) | **GET** /applications | Retrieves all deployed quick applications
[**get_avro_write_schema**](DefaultApi.md#get_avro_write_schema) | **GET** /gateway/{name}/schema/{type}/avro | Returns the Gatewy schema in Avro format
[**get_gateway**](DefaultApi.md#get_gateway) | **GET** /gateway/{name} | Retrieves information about a gateway
[**get_graphql_write_schema**](DefaultApi.md#get_graphql_write_schema) | **GET** /gateway/{name}/schema/{type}/graphql | Returns the Gatewy schema in GraphQL format
[**get_topic_information**](DefaultApi.md#get_topic_information) | **GET** /topic/{name} | Gets information about a topic
[**list_all_gateways**](DefaultApi.md#list_all_gateways) | **GET** /gateways | List all deployed gateways
[**list_all_topics**](DefaultApi.md#list_all_topics) | **GET** /topics | List all registered topic


# **create_gateway**
> create_gateway(gateway_creation_data)

Creates a new gateway

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    gateway_creation_data = quick_client.GatewayCreationData() # GatewayCreationData | 

    try:
        # Creates a new gateway
        api_instance.create_gateway(gateway_creation_data)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_gateway: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **gateway_creation_data** | [**GatewayCreationData**](GatewayCreationData.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_mirror**
> create_mirror(mirror_creation_data)

Creates a mirror for a topic

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    mirror_creation_data = quick_client.MirrorCreationData() # MirrorCreationData | 

    try:
        # Creates a mirror for a topic
        api_instance.create_mirror(mirror_creation_data)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_mirror: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mirror_creation_data** | [**MirrorCreationData**](MirrorCreationData.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_new_topic**
> create_new_topic(name, key_type=key_type, value_type=value_type, topic_creation_data=topic_creation_data)

Creates a new topic

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the topic
key_type = quick_client.QuickTopicType() # QuickTopicType | Type of the key (optional)
value_type = quick_client.QuickTopicType() # QuickTopicType | Type of the value (optional)
topic_creation_data = quick_client.TopicCreationData() # TopicCreationData | Additional topic data (optional)

    try:
        # Creates a new topic
        api_instance.create_new_topic(name, key_type=key_type, value_type=value_type, topic_creation_data=topic_creation_data)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_new_topic: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the topic | 
 **key_type** | [**QuickTopicType**](.md)| Type of the key | [optional] 
 **value_type** | [**QuickTopicType**](.md)| Type of the value | [optional] 
 **topic_creation_data** | [**TopicCreationData**](TopicCreationData.md)| Additional topic data | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_schema**
> create_schema(name, schema_data)

Creates a new GraphQL schema

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the gateway
schema_data = quick_client.SchemaData() # SchemaData | GraphQL schema

    try:
        # Creates a new GraphQL schema
        api_instance.create_schema(name, schema_data)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_schema: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the gateway | 
 **schema_data** | [**SchemaData**](SchemaData.md)| GraphQL schema | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_application**
> delete_application(name)

Deletes an application

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the application

    try:
        # Deletes an application
        api_instance.delete_application(name)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the application | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_gateway**
> delete_gateway(name)

Deletes a gateway

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the gateway

    try:
        # Deletes a gateway
        api_instance.delete_gateway(name)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_gateway: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the gateway | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_mirror**
> delete_mirror(name)

Deletes mirror of topic

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the topic

    try:
        # Deletes mirror of topic
        api_instance.delete_mirror(name)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_mirror: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the topic | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_topic**
> delete_topic(name)

Deletes topic

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the topic

    try:
        # Deletes topic
        api_instance.delete_topic(name)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_topic: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the topic | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deploy_application**
> deploy_application(application_creation_data)

Deploys a new application

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    application_creation_data = quick_client.ApplicationCreationData() # ApplicationCreationData | ApplicationCreationData object containing the app's information

    try:
        # Deploys a new application
        api_instance.deploy_application(application_creation_data)
    except ApiException as e:
        print("Exception when calling DefaultApi->deploy_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_creation_data** | [**ApplicationCreationData**](ApplicationCreationData.md)| ApplicationCreationData object containing the app&#39;s information | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application_information**
> get_application_information(name)

Retrieves information about the given application

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the application

    try:
        # Retrieves information about the given application
        api_instance.get_application_information(name)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_application_information: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the application | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_applications**
> get_applications()

Retrieves all deployed quick applications

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    
    try:
        # Retrieves all deployed quick applications
        api_instance.get_applications()
    except ApiException as e:
        print("Exception when calling DefaultApi->get_applications: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_avro_write_schema**
> SchemaData get_avro_write_schema(name, type)

Returns the Gatewy schema in Avro format

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the gateway
type = 'type_example' # str | The type used in the schema of the gateway

    try:
        # Returns the Gatewy schema in Avro format
        api_response = api_instance.get_avro_write_schema(name, type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_avro_write_schema: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the gateway | 
 **type** | **str**| The type used in the schema of the gateway | 

### Return type

[**SchemaData**](SchemaData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gateway schema in Avro Format |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_gateway**
> GatewayDescription get_gateway(name)

Retrieves information about a gateway

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the gateway

    try:
        # Retrieves information about a gateway
        api_response = api_instance.get_gateway(name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_gateway: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the gateway | 

### Return type

[**GatewayDescription**](GatewayDescription.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All information about the gateway |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_graphql_write_schema**
> SchemaData get_graphql_write_schema(name, type)

Returns the Gatewy schema in GraphQL format

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the gateway
type = 'type_example' # str | The type used in the schema of the gateway

    try:
        # Returns the Gatewy schema in GraphQL format
        api_response = api_instance.get_graphql_write_schema(name, type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_graphql_write_schema: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the gateway | 
 **type** | **str**| The type used in the schema of the gateway | 

### Return type

[**SchemaData**](SchemaData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gateway schema in GraphQL Format |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_topic_information**
> TopicData get_topic_information(name)

Gets information about a topic

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    name = 'name_example' # str | The name of the topic

    try:
        # Gets information about a topic
        api_response = api_instance.get_topic_information(name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_topic_information: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the topic | 

### Return type

[**TopicData**](TopicData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All information about the topic |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_all_gateways**
> list[GatewayDescription] list_all_gateways()

List all deployed gateways

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    
    try:
        # List all deployed gateways
        api_response = api_instance.list_all_gateways()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_all_gateways: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[GatewayDescription]**](GatewayDescription.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List all informations about the deployed gateways |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_all_topics**
> list[TopicData] list_all_topics()

List all registered topic

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import quick_client
from quick_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://quick-manager
# See configuration.py for a list of all supported configuration parameters.
configuration = quick_client.Configuration(
    host = "http://quick-manager"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = quick_client.Configuration(
    host = "http://quick-manager",
    api_key = {
        'X-API-Key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-Key'] = 'Bearer'

# Enter a context with an instance of the API client
with quick_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = quick_client.DefaultApi(api_client)
    
    try:
        # List all registered topic
        api_response = api_instance.list_all_topics()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_all_topics: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[TopicData]**](TopicData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of all information about the registered topics |  -  |
**401** | Unexpected error |  -  |
**0** | Unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

