# fitbit without fitbit.com #

Based on: https://www.hackerspace-bamberg.de/Fitbit_Aria_Wi-Fi_Smart_Scale

That document appears to be based on the &lt;V32 FW (V2 protocol).  They reported bugs to Fitbit so they changed the protocol.

All the values are *little-endian* (Intel byte order).

Tested on V35 FW (V3 protocol).

## Setup process ##

### Step 1: Activate setup mode ###

Disconnect one of the batteries in the unit for 10 seconds.  When reconnecting, the screen should display "HI :)", the software version number, then "SETUP ACTIVE".

If this has already been connected to a network, stand on the scales to force it to reset WiFi settings.

### Step 2: Connect to Aria's setup network ###

Connect to the scales' WiFi network.  This is named something like "Aria 1A2B3C", where the 1A2B3C represents the upper-case base16-encoded last three bytes of the MAC address of the unit.

The network is open, and you're about to send your WiFi key in the clear...

### Step 3: Send the WiFi settings ###

Normally, this process is bootstrapped by a web application at https://www.fitbit.com/scale/setup/start

This will redirect you to `http://1.scale.www.fitbit.com/scale/setup`.  The DNS name will normally be intercepted by the scales, and redirect you to a jQuery Mobile application to setup the scales' WiFi connection.

The purpose of doing it this way is so that the Aria can pinch the `token` cookie from `www.fitbit.com`.  This is used to link the Aria to your fitbit.com account.  The token value consists of a 6-character account ID, a dash, then a 9-character key.

If we're doing this without fitbit.com, we can use cURL to send the appropriate request to setup the network, and we can just address the scales by their IP address.

```
curl 'http://192.168.240.1/scale/setup?ssid=YourSsidHere&custom_password=YourNetworkPasswordHere' -H 'Cookie: token=YourTokenHere' 
```

### Step 4: Activation ###

Aria then connects to the network and sends a request:

```
GET /scale/register?serialNumber=20F85EXXXXXX&token=ABCD&ssid=YourSsidHere HTTP/1.1
Host: www.fitbit.com
```

Serial number is MAC address of ethernet device.  The SSID is shown in the web interface normally to "help you"...

Scale expects `200 OK` response to that request.  There is no response content.

### Step 5: Upload data / settings download ##

Another settings download request is made, to get settings, which is an upload (described below) with 0 measurements included.

This is used to give information about who uses the scale (weight, height, etc.) for determining between different users of the scale, and to set preferences (system clock, measurement system).

## Measurement uploads ##

Measurement lists always show with the newest measurement first, followed by up to 16 other measurements *oldest first*.  If there is an upload failure, the scales will cache other measurements in order to ensure they are still uploaded, even if the service goes down (or you don't send a valid response).

They are all marked with timestamps as well as the current state of the clock on the device.  This allows the time of measurement to be retrieved even if the clock goes out of sync.

Some data has a CRC-16-CCITT (xmodem) checksum. (Python: `crc16.crc16xmodem`)

### Aria -> Server comms (`aria_upload_request_envolope3`): ###

```
POST /scale/upload

struct aria_upload_request_envolope3 {
	aria_upload_request_body3 body,
	
	// calculated on all bytes in body
	uint16 crc16
};

struct aria_upload_request_body3 {
	uint32 protocol_version = 3,
	uint32 battery_percent,
	char[6] mac_address,
	char[16] auth_code,
	uint32 firmware_version,
	uint32 unknown2 = 33,

	// Current UNIX time according to the Aria's clock.
	// Used to correct the time of measurements if this goes out of sync.
	uint32 timestamp,

	uint32 measurement_count,
	aria_measurement[measurement_count] measurements
};

struct aria_measurement {
	uint32 id2 = 2,
	uint32 impedence,
	uint32 weight_g,

	// UNIX time of measurement.
	uint32 timestamp,

	// These values are 0 for guest users.
	uint32 user_id,
	uint32 fat1,
	uint32 covariance,
	uint32 fat2
};
```

### Server -> Aria comms (`aria_upload_response_envolope3`): ###

```
struct aria_upload_envolope3 {
	aria_upload_response_body3 body,

	// calculated on all bytes in body
	uint16 crc16,

	uint8 unknown2 = 0x66,
	uint8 unknown3 = 0x00
};


struct aria_upload_response_body3 {
	// UNIX time for synchronising the Aria's clock
	uint32 current_timestamp,

	unit_type units,
	status_type status,
	uint8 unknown1 = 0x01,
	uint32 user_count,
	aria_user[user_count] users
}


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
	char[16] padding, // 16 * 0x00
	char[20] name,
	uint32 min_weight_tolerance,
	uint32 max_weight_tolerance,
	uint32 age_years,
	gender_type gender,
	uint32 height_mm,

	// previous known values
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

