# Bullet Hell Battle Royale

### Next
- Enemy Health
  - enemy death
- EXP
  - Exp Particles
- Death
  - Spectator
- projectiles hit other players
- 


### Backlog
- Network delay: sending projectile (and other) position over the network comes with a delay. Need to send time that it was sent and extrapolate on client side. Util::CalculateFramesSinceTime or some equivalent 
- Network tuples: Objects sent over the network just be tuples rather than dictionaries with variable name keys
- Network dictionaries to lists: Can only send 1 update of each type currently. Network should take in list of dicts instead. ie when sending all enemy updates, should be [EnemyUpdate]
- Dash cd reset on room change: Changing room recreates the player and its cooldowns
- Actor overridden functions can be private. ie update
- Lag simulator
- Twisted: Look into twisted to replace sockets
- 
