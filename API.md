# API
## Internal API
### Create request indicator
Request:
```shell
curl --location 'http://127.0.0.1:8000/eos/request_indicator/create_request_indicator' \
--header 'Authorization: Basic YmluaGR1b25nOjEyMzQ1Njc4OTAhQCM=' \
--header 'Content-Type: application/json' \
--header 'Cookie: session_id_admin=127.0.0.1-57433a29-8792-4f7f-8890-3ed6b63ff392; session_id_eos=127.0.0.1-3b197926-5d21-4e85-a099-5201faaf3e4c' \
--data '{
    "indicator": "3342",
    "source_name": "fndwo3",
    "indicator_type": 2,
    "unit": "mg/l",
    "description": "nothing to show",
    "order_no": 1
}'
```
Response:
```json
{
    "meta": {
        "message": "success",
        "code": 200
    },
    "data": {
        "id": 30960105971760758514019197084
    }
}
```
```json
{
    "meta": {
        "message": "Exist an request indicator with the same name or source name 64099973bf8b85a9a3e3e09c",
        "code": 400
    },
    "data": null
}
```

### List request indicator
Request:
```shell
curl --location 'http://127.0.0.1:8000/eos/request_indicator/list_request_indicators?keyword=nothing%20to%20show&page=1&indicator_type=0&page_size=2' \
--header 'Authorization: Basic YmluaGR1b25nOjEyMzQ1Njc4OTAhQCM=' \
--header 'Cookie: session_id_eos=127.0.0.1-89777c07-24f2-4a55-ad71-ffdb5b10693c'
```
Response:
```json
{
    "meta": {
        "total": 4,
        "message": "success",
        "code": 200,
        "page": 1,
        "page_size": 2
    },
    "data": [
        {
            "indicator_type": 2,
            "indicator_id": null,
            "indicator": "3342",
            "source_name": "fndwo3",
            "description": "nothing to show",
            "order_no": 3,
            "reason": "",
            "id": "6406f63699a56541f8e21cd7",
            "unit": "mg/l",
            "approve_status": 0
        },
        {
            "indicator_type": 2,
            "indicator_id": null,
            "indicator": "217d",
            "source_name": "dqqdq",
            "description": "nothing to show",
            "order_no": 2,
            "reason": "",
            "id": "6406f3ffddc9ec5b4c9b93fc",
            "unit": "mg/l",
            "approve_status": 0
        }
    ]
}
```

### Update request indicator
Request:
```shell
curl --location 'http://127.0.0.1:8000/eos/request_indicator/update_request_indicator/640b54328659f142f6e19227' \
--header 'Authorization: Basic YmluaGR1b25nOjEyMzQ1Njc4OTAhQCM=' \
--header 'Content-Type: application/json' \
--header 'Cookie: session_id_eos=127.0.0.1-5fb5a5bc-36ec-4542-806c-85cf1a7401c7' \
--data '{
    "indicator": "H2MG9",
    "source_name": "vat/vut",
    "indicator_type": 5,
    "unit": "mg/ml",
    "description": "chemical",
    "order_no": 3
}'
```
Response:
```json
{
    "meta": {
        "message": "success",
        "code": 200
    },
    "data": null
}
```
```js
{
    "meta": {
        "message": "Indicator type must > 0 and < 5",
        "code": 400
    },
    "data": null
}
```
