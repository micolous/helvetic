# Google Fit #

API Explorer: https://developers.google.com/apis-explorer/#p/fitness/v1/

Documentation:

* https://developers.google.com/fit/rest/v1/data-sources
* https://developers.google.com/fit/rest/v1/reference/users/dataSources

Data created with the REST API shows up in the Android app, but doesn't show up as a *defined source* in the "Connected Apps" view (because no Android App).  Data gets dropped in like magic...

This API is exposed by google-api-client-python, and requires OAuth credentials of the user to be stored.

## Creating a datasource for a user ##

At setup time, a data source needs to be defined for the user which stores their measurements.

Scales are supported as a well-known sensor type (`com.google.weight`) with a defined schema (`weight: floatPoint`).

```javascript
POST https://www.googleapis.com/fitness/v1/users/me/dataSources

{
 "application": {
  "name": "au.id.micolous.helvetic"
 },
 "dataType": {
  "field": [
   {
    "format": "floatPoint",
    "name": "weight"
   }
  ],
  "name": "com.google.weight"
 },
 "device": {
  "manufacturer": "FitBit",
  "model": "Aria",
  "type": "scale",
  "uid": "1234",
  "version": "1"
 },
 "type": "raw"
}

Response
 
{
 "dataStreamId": "raw:com.google.weight:292824132082:FitBit:Aria:1234",
 "type": "raw",
 "dataType": {
  "name": "com.google.weight",
  "field": [
   {
    "name": "weight",
    "format": "floatPoint"
   }
  ]
 },
 "device": {
  "uid": "1234",
  "type": "scale",
  "version": "1",
  "model": "Aria",
  "manufacturer": "FitBit"
 },
 "application": {
  "name": "au.id.micolous.helvetic"
 }
}
```


## Updating that data source ##

Data sources are kept in "sessions", which is a time window defined as nanoseconds since the UNIX epoch.  Weight sessions are measured in an "instant", so the start and end times are identical.

This gets aggregated into a single data source used by the Android application and web client.

```javascript
PATCH https://www.googleapis.com/fitness/v1/users/me/dataSources/raw%3Acom.google.weight%3A292824132082%3AFitBit%3AAria%3A1234/datasets/1417698736000000000-1417698736000000000?key={YOUR_API_KEY}

{
 "dataSourceId": "raw:com.google.weight:292824132082:FitBit:Aria:1234",
 "maxEndTimeNs": "1417698736000000000",
 "minStartTimeNs": "1417698736000000000",
 "point": [
  {
   "dataTypeName": "com.google.weight",
   "endTimeNanos": "1417698736000000000",
   "startTimeNanos": "1417698736000000000",
   "value": [
    {
     "fpVal": 95
    }
   ]
  }
 ]
}
```

