# air_conditioner_api_mqtt_agent

air_conditioner_apiの横で動作するMQTTのagent。
MQTT経由でsubscribeしていたコマンドイベントから、air confitioner apiを叩くことができる。


# Subscribe Topics

<details>
<summary>detail</summary>

prefix: `{PROJECT_ID}/air_conditioner_api_mqtt_agent`

## on hot or cool

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


## on dehumidify

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


## off

##### topic

`{prefix}/off`

##### schema

```js
None
```


## ping

##### topic

`{prefix}/ping`

##### schema

```js
None
```



## reboot

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

## ack

ping ack

##### topic

`{prefix}/ack`

##### schema

- mqtt_agent: boolean
- air_conditioner_api: boolean

true: OK, false: not running

```json
{
    "mqttAgent": true,
    "airConditionerApi": true
}
```



## state

latest air conditioner state

##### topic

`{prefix}/state`

##### schema

- isRunning: boolean
- type: string = "cool" | "hot" | "dehumidify"
- temperature: number | null = 16 ~ 31 | null(only type="dehumidify")
- dehumidificationLevel: number | null = 1 ~ 3 | null(only type ="hot" or "cool")
- airflowLevel: string = "a" | "1" | "2" | "3"


type = "cool" or "hot"

```json
{
    "isRunning": true,
    "type": "cool",
    "temperature": 26,
    "dehumidificationLevel": null,
    "airflowLevel": "3"
}
```



type = "off"

```json
{
    "isRunning": true,
    "type": "hot",
    "temperature": 27,
    "dehumidificationLevel": null,
    "airflowLevel": "a"
}
```



type = "dehumidify"

```json
{
    "isRunning": false,
    "type": "dehumidify",
    "temperature": null,
    "dehumidificationLevel": 2,
    "airflowLevel": "2"
}
```




</details>







