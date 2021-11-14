## Create a HTTP REST service storing and retrieving a larger english text 
## and in a separate request retrieve a summary of that text.
 
An example request for the service would be:

```
  POST / HTTP/1.1
  Accept: application/json
  Content-Type: application/x-www-form-urlencoded
 
  text=This+is+a+long+text
```
 
This endpoint should return a `document_id` which can be used later to retrieve
the document again or request a summary of it.
 
A second endpoint should return a summary of a document with a given document_id.
The response of this endpoint should be something like:

```
  HTTP/1.1 200 OK
  Content-Type: application/json
   
  {
    "document_id";: "example_id",
    "summary": "This is the summary"
  }
``` 

 