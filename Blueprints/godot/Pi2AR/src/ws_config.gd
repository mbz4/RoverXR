extends Node

# ws vars
#var WS_URI : String = "ws://192.168.199.228:3333"
var WS_URI : String = "ws://192.168.8.153:3333"
#var WS_URI : String = "ws://mbzpi.local:3333"
var INBOUND_BUFFER_SIZE : int = 3538944 # max_size = 3.275MB = 27Mbps
# #VERY_LOW=6Mbps, LOW=12Mbps, MEDIUM=18Mbps, HIGH=27Mbps
var RECONNECT_WAIT : float = 1.5

# ui vars
var FPS_UPDATE_DELAY : float = 500 # ms
var SHOW_FRAME_DEBUG : bool = false
var DEBUG : String
var FPS : String
