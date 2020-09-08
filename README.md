# air_conditioner_api_mqtt_agent

air_conditioner_apiの横で動作するMQTTのagent


# Subscribe Topics

<details>
<summary>detail</summary>

prefix: `{PROJECT_ID}/air_conditioner_api_mqtt_agent`

### on

##### topic

`{prefix}/on/cool`
`{prefix}/on/hot`

##### schema

- temperature: number = 16~31
- airflowLevel: string = "a" | "1" | "2" | "3"

```json
{
    "temperature": 26,
    "airflowLevel": "2"
}
```


### on

##### topic

`{prefix}/on/dehumidify`

##### schema

- dehumidificationLevel: number = 1~3
- airflowLevel: string = "a" | "1" | "2" | "3"

```json
{
    "dehumidificationLevel": 2,
    "airflowLevel": "2"
}
```


### ping

##### topic

`{prefix}/ping`

##### schema

```js
None
```



### reboot

rebbot this mqtt agent

##### topic

`{prefix}/reboot`

##### schema

```js
None
```

</details>





# Publish Topics

<details>
<summary>detail</summary>

prefix: `{PROJECT_ID}/air_conditioner_api_mqtt_agent`

### ack

ping ack

##### topic

`{prefix}/ack`

##### schema

```js
None
```



### state

latest air conditioner state

##### topic

`{prefix}/state`

##### schema


- type: string = "cool" | "hot" | "dehumidify" | "off"
- temperature: number | null = 16 ~ 31 | null(only type="off" or "dehumidify")
- dehumidificationLevel: number | null = 1 ~ 3 | null(only type = "off" or "hot" or "cool")
- airflowLevel: string = "a" | "1" | "2" | "3" | "null"(only type="off")


type = "cool" or "hot"

```json
{
    "type": "cool",
    "temperature": 26,
    "dehumidificationLevel": null,
    "airflowLevel": "3"
}
```



type = "off"

```json
{
    "type": "off",
    "temperature": null,
    "dehumidificationLevel": null,
    "airflowLevel": null
}
```



type = "dehumidify"

```json
{
    "type": "off",
    "temperature": null,
    "dehumidificationLevel": 2,
    "airflowLevel": "2"
}
```




</details>







