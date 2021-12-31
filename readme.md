# TinyURL API

## What is TinyURL API?
It is a Flask based API that shortens the full URL to alphanumeric 6 character string. 

Examples;
- URL = www.google.com --> Shortcode = abc123
- URL = www.amazon.com --> Shortcode = 123def

## Installation & Running the API. 
`git clone https://github.com/earik87/tinyurl ~/tinyurl`

Activate virtual environment with the following command in its directory `venv\Scripts\activate`. Then, to run the flask application, run the following commands in the command shell.

```
set FLASK_APP=application.py
$env:FLASK_APP = "application.py"
flask run
```

## Usage.
Note; Commands are used and tested in Windows. They might differ in MacOS and Linux.

- To shorten the URL, post request can be used as following from the shell. 

`curl --header "Content-Type: application/json" --request POST --data '{ \"url\":\"www.facebook.com\",\"shortcode\":\"abc123\"}' http://localhost:5000/shorten`

Output;
```
{
  "shortcode": "abc123"
}
```

- To get the URL from a shortcode, use the following GET command. 
`curl -i http://localhost:5000/abc123`

Output; 
```
{
  "url": "www.facebook.com"
}
```

- To get the statistics from the shortcode, use the following GET command.
`curl -i http://localhost:5000/abc123/stats`

Output;
```
{
  "created": "2021-12-31T21:31:27.331Z",
  "lastRedirect": "2021-12-31T21:34:58.241Z",
  "redirectCount": 1
}
```

## Testing.
Run `pytest` command to execute tests in `test_application.py` file.  

