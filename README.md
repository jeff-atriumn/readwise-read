# readwise-read
A handful of scripts to read Readwise content via the API. Readwise is a service that helps you save, organize, and review highlights from digital content. [Readwise.io](https://readwise.io/).

## Prerequisites
- Python 3.x

## scripts
| title | description | test |
| ----- | ----------- | ---- |
| [readwise_shortlist.py](readwise_shortlist.py) | Open & Read a random sampling (5) of Readwise items in your shortlist | [test_readwise_shortlist.py](test_readwise_shortlist.py) |

## usage
- Make sure you have Python 3.x installed on your system.
- Create and populate a `config.ini` file with the relevant Readwise API token, which you can find/create [here](https://readwise.io/access_token).
```ini
[config]
readwise_api_token = token_string
```

```console
foo@bar:~$ pip install -r requirements.txt
foo@bar:~$ python3 readwise_shortlist.py
