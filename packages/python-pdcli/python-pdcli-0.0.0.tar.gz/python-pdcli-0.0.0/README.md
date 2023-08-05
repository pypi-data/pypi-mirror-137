# PD cli


## Test
```
export PD_ACCOUNT_TOKEN=xyz

pd ls \
  --statuses=acknowledged,triggered --since=$(date -v -1d +%F) --column \
  | column -t -s$'\t'
```

## Reference
* https://pypi.org/project/pdpyras/
* https://developer.pagerduty.com/api-reference/
