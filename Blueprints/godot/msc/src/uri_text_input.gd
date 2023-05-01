extends Control
# https://en.wikipedia.org/wiki/Display_resolution

@onready var DisplayURI = $Bakcground/MarginContainer/Rows/InputArea/Rows/Settings/DisplayURI
@onready var DisplayFPS = $Bakcground/MarginContainer/Rows/InputArea/Rows/Settings/DisplayFPS
@onready var DebugOverlay = $Bakcground/MarginContainer/Rows/StreamPanel/DebugOverlay

var previous_fps_msg : String
var curr_fps_msg : String
var previous_debug_msg : String
var curr_debug_msg : String

func _ready():
	DisplayURI.text = WS_CONF.WS_URI

func _process(_delta):
	if WS_CONF.SHOW_FRAME_DEBUG:
		curr_debug_msg = WS_CONF.DEBUG
		curr_fps_msg = WS_CONF.FPS
		if previous_debug_msg != curr_debug_msg:
			previous_debug_msg = curr_debug_msg
			DebugOverlay.text += curr_debug_msg#+"\n"
		if previous_fps_msg != curr_fps_msg:
			previous_fps_msg = curr_fps_msg
			DisplayFPS.text = curr_fps_msg
	
func _on_input_uri_text_submitted(new_text):
	WS_CONF.WS_URI = "ws://"+str(new_text)
	DisplayURI.text = WS_CONF.WS_URI
	DebugOverlay.text += "WS URI CHANGED: " + WS_CONF.WS_URI

func _on_show_debug_toggled(button_pressed):
	WS_CONF.SHOW_FRAME_DEBUG = button_pressed
