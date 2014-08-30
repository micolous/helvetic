# fitbit without fitbit.com #

Based on: https://www.hackerspace-bamberg.de/Fitbit_Aria_Wi-Fi_Smart_Scale

That document appears to be based on the &lt;V32 FW (V2 protocol).  They reported bugs to Fitbit so they changed the protocol.

All the values are *little-endian* (Intel byte order).

Tested on V35 FW (V3 protocol).

Step 1:

Disconnect one of the batteries in the unit for 10 seconds.  When reconnecting, the screen should display "HI :)", the software version number, then "SETUP ACTIVE".

If this has already been connected to a network, stand on the scales to force it to reset WiFi settings.

Step 2:

Connect to the scales' WiFi network.  This is named something like "Aria 1A2B3C", where the 1A2B3C represents the upper-case base16-encoded last three bytes of the MAC address of the unit.

Step 3:

Fire off a GET request to connect to the network:

```
curl 'http://192.168.240.1/scale/setup?ssid=YourSsidHerecustom_password=YourNetworkPasswordHere' -H 'Cookie: token=YourTokenHere' 
```

Step 4:

Aria then connects to the network and sends a request:

```
GET /scale/register?serialNumber=20F85EXXXXXX&token=ABCD&ssid=YourSsidHere HTTP/1.1
Host: www.fitbit.com
```

Serial number is MAC address of ethernet device.  The SSID is shown in the web interface normally to "help you"...

Scale expects "200 OK" response to that request.

Step 5:

Another "synchronisation" request is made, to get settings. (an upload with 0 measurements)

This request is replayable, that is, we can send the same message to the server.  But we get a slightly different response each time.


## Measurements ##

Measurements lists always show with the newest measurement first, followed by up to 16 other measurements *oldest first*.

They are all marked with timestamps as well as the current state of the clock on the device.  This allows the time of measurement to be retrieved even if the clock goes out of sync.

Aria -> Server comms:

```
POST /scale/upload

struct aria_upload_request3 {
	uint32 protocol_version = 3,
	uint32 battery_percent,
	char[6] mac_address,
	char[16] auth_code,
	uint32 firmware_version,
	uint32 unknown2 = 33,
	uint32 timestamp,
	uint32 measurement_count,
	aria_measurement[measurement_count] measurements,
	uint16 crc16
};

struct aria_measurement {
	uint32 id2 = 2,
	uint32 impedence,
	uint32 weight_g,
	uint32 timestamp,
	uint32 user_id,
	uint32 fat1,
	uint32 covariance,
	uint32 fat2
};
```

Server -> Aria comms:

```
struct aria_upload_response3 {
	uint32 current_timestamp,
	unit_type units,
	status_type status,
	uint8 unknown1 = 0x01,
	uint32 user_count,
	aria_user[user_count] users
	uint16 crc16,
	uint8 unknown2 = 0x66,
	uint8 unknown3 = 0x00
};

enum unit_type uint8 {
	pounds    = 0,
	stone     = 1,
	kilograms = 2
};

enum status_type uint8 {
	configured   = 0x32,
	unconfigured = 0x64
};

struct aria_user {
	uint32 user_id,
	char[20] name,
	uint32 min_weight_tolerance,
	uint32 max_weight_tolerance,
	uint32 age_years,
	gender_type gender,
	uint32 height_mm,
	uint32 weight1,
	uint32 body_fat,
	uint32 covariance,
	uint32 weight2,
	uint32 timestamp,

	uint32 unknown1 = 0,
	uint32 unknown2 = 3,
	uint32 unknown3 = 0
};

enum gender_type uint8 {
	male = 0x02,
	female = 0x00,
	unknown = 0x34
};

```

