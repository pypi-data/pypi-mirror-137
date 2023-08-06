# csotools-serverquery

Library to query GoldSource & CSO servers.

Implements [Valve's Server Query Protocol](https://developer.valvesoftware.com/wiki/Server_queries).

Forked from [python-a2s v1.3.0](https://github.com/Yepoleb/python-a2s),
which is also rewrite of the [python-valve](https://github.com/serverstf/python-valve) module.

Supports both synchronous and asyncronous applications.

## Requirements

Python >=3.7, no external dependencies

## Install

`pip3 install csotools-serverquery` or `python3 setup.py install`

## API

### Functions

Synchronous:
* `csotools_serverquery.info(...)`
* `csotools_serverquery.players(...)`
* `csotools_serverquery.rules(...)`
* `csotools_serverquery.ping(...)`

Asynchronous:
* `csotools_serverquery.ainfo(...)`
* `csotools_serverquery.aplayers(...)`
* `csotools_serverquery.arules(...)`
* `csotools_serverquery.aping(...)`

### Exceptions

* `csotools_serverquery.BrokenMessageError(Exception)` - General decoding error.
* `csotools_serverquery.BufferExhaustedError(BrokenMessageError)` - Response too short.
* `socket.timeout` - No response (synchronous calls).
* `asyncio.exceptions.TimeoutError` - No response (async calls).
* `socket.gaierror` - Address resolution error.
* `ConnectionRefusedError` - Target port closed.
* `OSError` - Various networking errors like routing failure.

## Examples

Example output shown may be shortened.

```py
>>> import csotools_serverquery as a2s
>>> address = ("129.226.150.30", 27116)

>>> a2s.info( address )
SourceInfo(protocol=48, server_name='[sorpack.com]116丧尸升级服(Asia.Best)', map_name='de_dust2', folder='cstrike', game='Biohazard', app_id=10, player_count=3, max_players=32, bot_count=2, server_type='d', platform='w', password_protected=False, vac_enabled=False, version='1.1.2.7/Stdio', edf=145, port=27116, steam_id=90071992547409920, stv_port=None, stv_name=None, keywords=None, game_id=10, ping=0.07799999999406282)

>>> a2s.info( address )
GoldSrcInfo(address='127.0.0.1:27116', server_name='[sorpack.com]116丧尸升级服(Asia.Best)', map_name='de_dust2', folder='cstrike', game='Biohazard', player_count=3, max_players=32, protocol=47, server_type='D', platform='W', password_protected=False, is_mod=True, vac_enabled=False, bot_count=2, mod_website='', mod_download='', mod_version=1, mod_size=0, multiplayer_only=True, uses_custom_dll=False, ping=0.031000000002677552)

>>> import asyncio

>>> asyncio.run( a2s.ainfo(address) )
GoldSrcInfo(address='127.0.0.1:27116', server_name='[sorpack.com]116丧尸升级服(Tpo.love)', map_name='de_dust2', folder='cstrike', game='Biohazard', player_count=3, max_players=32, protocol=47, server_type='d', platform='w', password_protected=False, is_mod=True, vac_enabled=False, bot_count=2, mod_website='', mod_download='', mod_version=1, mod_size=0, multiplayer_only=True, uses_custom_dll=False, ping=0.046000000002095476)

>>> address = ("169.254.250.246", 40008) #CSN:S Turkey server
>>> a2s.info( address, mutator_cls=a2s.connection.CSOStreamMutator )
GoldSrcInfo(address='169.254.250.246:40008', server_name='[TR]Come get some.', map_name='cs_italy', folder=' �\x19', game='Counter-Strike', player_count=7, max_players=9, protocol=47, server_type='D', platform='W', password_protected=False, is_mod=True, vac_enabled=False, bot_count=6, mod_website='www.counter-strike.net', mod_download='', mod_version=1, mod_size=184000000, multiplayer_only=False, uses_custom_dll=False, ping=0.21800000000803266)
```

## Notes

* Some servers return inconsistent or garbage data. Filtering this out is left to the specific application, because there is no general approach to filtering that makes sense for all use cases. In most scenarios, it makes sense to at least remove players with empty names. Also the `player_count` value in the info query and the actual number of players returned in the player query do not always match up.

* For some games, the query port is different from the actual connection port. The Steam server browser will show the connection port and querying that will not return an answer. There does not seem to be a general solution to this problem so far, but usually probing port numbers up to 10 higher and lower than the connection port usually leads to a response. There's also the option of using `http://api.steampowered.com/ISteamApps/GetServersAtAddress/v0001?addr={IP}` to get a list of game servers on an IP (thanks to Nereg for this suggestion). If you're still not successful, use a network sniffer like Wireshark to monitor outgoing packets while refreshing the server popup in Steam.

* Player counts above 255 do not work and there's no way to make them work. This is a limitation in the specification of the protocol.

* This library does not implement rate limiting. It's up to the application to limit the number of requests per second to an acceptable amount to not trigger any firewall rules.

## Tested Games

Half-Life, Counter-Strike 1.6, Counter-Strike Nexon : Studio

## License

MIT
