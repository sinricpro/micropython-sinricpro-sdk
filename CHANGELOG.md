## [3.0.0]

- feat: Local control. Devices answer signed commands over the LAN on UDP 3333, so they keep working while the SinricPro cloud is unreachable. Requests are dispatched through the existing device callbacks - no application changes needed. Disable with `start(..., local_control=False)`.
- feat: The listener binds to `0.0.0.0` and joins `224.9.9.9`, so it takes unicast, multicast and subnet broadcast. Broadcast matters: it is how the app finds a device on networks that drop multicast, and this SDK publishes no mDNS record.
- fix: Outgoing messages are signed over the exact bytes transmitted - the payload is serialized once and spliced into the envelope, rather than serialized again for the signature.
- fix: A request that fails verification no longer raises out of the receive task, which stopped the SDK handling anything further. A LAN request gets a signed "Signature is invalid" reply instead, letting a client tell a wrong app secret from an unreachable device.
- fix: A message with no signature at all is now rejected rather than processed.
- fix: `sinricpro/udp_listener.py` and `sinricpro/devices/sinricpro_airquality_sensor.py` are now listed in `package.json`. The air quality sensor had never been included, so `mip install` could not use it.
- BREAKING CHANGE: a request that fails signature verification no longer raises `InvalidSignatureError` out of the receive task. Code that caught it to detect tampering should read the signed "Signature is invalid" response instead.

## [2.0.0]

- BREAKING CHANGE: Remove `restoreDeviceStates` in order to change this at device level from server side instead of fixed value in client sdk.

## [1.0.0]

- New SDK