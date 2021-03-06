# Community Discussions API

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/)
- [Motor](https://motor.readthedocs.io/)
- [Poetry](https://python-poetry.org/)
- [Dynaconf](https://www.dynaconf.com/)

## Installation

In order to install the dependencies, run:

```shell
make install
```

Then you can run the command below to run the application:

```shell
make run
```

Visit [localhost:8000/docs](http://localhost:8000/docs) in your browser and you should see the documentation for the API automatically generated by FastAPI.

## Documentation

To visit the interactive API documentation, access [localhost:8000/docs](http://localhost:8000/docs):

![API Documentation](./img/docs.png)

## Examples

- Search for topics about `Life`:

```shell
curl -X 'GET' \
  'http://localhost:8000/api/v1/topics/search?skip=0&limit=10&term=Life' \
  -H 'accept: application/json'
```

- List comments:

```shell
curl -X 'GET' \
  'http://localhost:8000/api/v1/topics/{topic_id}/comments?skip=0&limit=20' \
  -H 'accept: application/json'
```

## Modeling

- Topic: a topic is a discussion about a specific subject.

```json
{
  "_id": "9b1ebb4f-e3e8-4b04-bc03-ee8ac954399a",
  "title": "Someone can help me?",
  "content": "What's the meaning of life?",
  "username": "John Doe",
  "created": "2021-08-08T18:14:40.692017",
  "updated": "2021-08-08T19:53:47.165000",
  "type": "topic"
}
```

- Comment: a comment is a reply to a topic.

```json
[
  {
    "_id": "9b1ebb4f-e3e8-4b04-bc03-ee8ac954399b",
    "topic": "9b1ebb4f-e3e8-4b04-bc03-ee8ac954399a",
    "reply": null,
    "content": "I think the meaning of life is 42.",
    "username": "Nephew Bob",
    "created": "2021-08-08T20:53:47.123000",
    "updated": null,
    "type": "comment"
  },
  {
    "_id": "9b1ebb4f-e3e8-4b04-bc03-ee8ac954399c",
    "topic": "9b1ebb4f-e3e8-4b04-bc03-ee8ac954399a",
    "reply": "9b1ebb4f-e3e8-4b04-bc03-ee8ac954399b",
    "content": "What?",
    "username": "John Doe",
    "created": "2021-08-08T20:54:47.123000",
    "created": "2021-08-08T20:54:49.123000",
    "type": "comment"
  }
]
```
