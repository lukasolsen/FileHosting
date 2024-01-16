# API Routes

This is a list of all the routes that the API has.

### Characters

_Authorization_: (Required) Bearer Token
_Params_: (Optional) ?page=1&limit=10

_User_
**Register**: POST /user/register
_Type_: application/json

```json
"username": "John Doe",
"password": "pass",
```

**Login**: POST /user/login
_Type_: application/json

```json
"username": "John Doe",
"password": "pass"
```

_Download_
**Items**: GET /download/items
_Params_: ?page=1&limit=10
_Authorization_: Bearer Token

**Item**: GET /download/item/:id
_Params_: id
_Authorization_: Bearer Token

**Download**: GET /download/download/:id
_Params_: id
_Response_: [UUID]
_Authorization_: Bearer Token

**Download Redirect (Final)**: GET /download/download*redirect/:uuid
\_Params*: uuid
_:warning:_ **This is a one time use and it's used to download the wanted file.**
