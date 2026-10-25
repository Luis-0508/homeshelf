# Replacing the Home button on a 2018 Samsung TV

Feasibility study for the reference TV (UE43NU7099, Tizen 4.0; see
[PLATFORM.md](PLATFORM.md)). Read-only analysis: nothing in Home routing,
firmware, boot configuration or security settings was changed.

## Result

**With documented developer features and without exploiting vulnerabilities,
there is no evidenced way to route the Home button to a third-party app on
this TV.** Building further launcher versions does not change that.

## Known approaches

**CleanFrame** ([agent-tv-setup-guide.md](https://github.com/nthnclrk/CleanFrame/blob/main/docs/agent-tv-setup-guide.md);
The Frame LS03D, Tizen 9.0, ARMv7). A temporary .NET helper runs as Samsung's
SDK user (UID 901) through what the guide calls an "undocumented package-name
command-execution workaround". It assigns the native main operation with
`app_operation_set_current_app` and writes vconf keys such as
`db/appfw/home_appid`, `db/appfw/startup_appid`,
`db/appfw/booting_appid_backup`, `db/first_screen/type` and
`db/menu/smart_hub/ontvsetting/auto_start`. The guide describes one
experiment, not a recommendation; normal power-on behaviour was not confirmed.
Similar launchers for Tizen 6.5–9 (Clean Home, AeroTizen, quiet-tizen) use the
same family of vconf changes.

**Flix Home** ([repository](https://github.com/schadogamer127-sys/Flix-Home);
UE43NU7409, 2018, Tizen 4.0, firmware T-KTM2DEUC-1360.0) is the closest
comparable case: a signed web app like HomeShelf. Its README states that
"Physical Home replacement and reliable cold-boot/standby autostart are not
implemented" and that the installer does not alter Home or startup settings.

## Classification for the reference TV

| Building block | Status on the reference TV |
|---|---|
| Developer Mode, SDB, own signed WGT | **compatible** (measured: HomeShelf installs and runs) |
| Run code as the SDK user (CleanFrame helper) | **incompatible** (measured: SDB shell closed, `appcmd_support` and root disabled); also relies on an undocumented execution path |
| Write `db/appfw/home_appid` and related vconf keys | **incompatible** through the available channels (no shell, no vconf in the web API) |
| Register Home as a key / take over the main operation via public APIs | **incompatible** (measured: Home is not registrable; no documented API) |
| Own .NET or native app with vconf write access | conceivable, untested, no evidence; write access to `db/appfw/*` is not documented for third-party apps |
| *Autorun Last App* setting | conceivable, untested; the launcher is terminated whenever it starts an app, so the "last app" is usually the streaming app |
| *Autorun Smart Hub* off | compatible, but does not replace Home |

## Next steps

1. Read the Samsung software version on the TV (Settings › Support › About
   This TV) for the record; it does not change the classification, because
   the block is the SDB channel.
2. Test the only documented approximation: enable *Autorun Last App*, open the
   launcher, power-cycle (standby and mains). Record the result.
3. Do not pursue the CleanFrame helper, vconf writes or root projects: they
   need an undocumented execution path or a vulnerability.
4. Re-evaluate only if the facts change: a firmware that opens the SDB channel,
   or an official Samsung API for default launchers.
