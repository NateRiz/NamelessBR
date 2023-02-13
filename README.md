# Bullet Hell Battle Royale
### Todo
- Network delay: sending projectile (and other) position over the network comes with a delay. Need to send time that it was sent and extrapolate on client side. Util::CalculateFramesSinceTime or some equivalent 
- Server needs to control enemy movement.
- Network tuples: Objects sent over the network just be tuples rather than dictionaries with variable name keys
- Dash cd reset on room change: Changing room recreates the player and its cooldowns
- Actor overridden functions can be private
