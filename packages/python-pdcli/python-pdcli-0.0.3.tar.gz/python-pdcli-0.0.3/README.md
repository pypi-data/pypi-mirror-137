# PD cli


## Test
```
export PD_ACCOUNT_TOKEN=xyz

pd ls \
  --statuses=acknowledged,triggered --since=$(date -v -1d +%F) --column \
  | column -t -s$'\t'
```

Default output is json string. In order to extract field:
```shell
# to extract "id" from user record
pd user --user-id=me | jq -r .id
```


## Reference
* https://pypi.org/project/pdpyras/
* https://developer.pagerduty.com/api-reference/
