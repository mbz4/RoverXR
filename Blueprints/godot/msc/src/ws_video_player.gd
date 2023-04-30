extends Node3D

var socket = WebSocketPeer.new()
var ws_url : String = "ws://192.168.199.228:3333"

func _ready():
	socket.set_inbound_buffer_size(3538944)
	_handle_connect(0.5)

func _process(_delta):
	socket.poll()
	var state = socket.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:		
		while socket.get_available_packet_count() > 0:
			var data = socket.get_packet()
			_handle_stream(data)
					
	elif state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass
	elif state == WebSocketPeer.STATE_CLOSED:
		var code = socket.get_close_code()
		var reason = socket.get_close_reason()
		print("WebSocket closed with code: %d, reason %s. Clean: %s" % [code, reason, code != -1])
		set_process(false) # Stop processing
		_handle_connect(3.0)

func _handle_connect(DELAY : float) -> void:
	await get_tree().create_timer(DELAY).timeout
	var state = socket.get_ready_state()
	if state == WebSocketPeer.STATE_CLOSED:
		if socket.connect_to_url(ws_url) == OK:
			print("Connected to %s" % [ws_url])
			set_process(true) # Keep the connection open
	else:
		print("Failed to connect to %s" % [ws_url])

func _handle_stream(data: PackedByteArray) -> void:
	var frame = Image.new()
	var error = frame.load_jpg_from_buffer(data) 
	if error == OK:
#		$TextureRect.texture = ImageTexture.create_from_image(frame)
		$Sprite3D.texture = ImageTexture.create_from_image(frame)
	else:
		print("Failed to load received image, error code %s" % [error])
		pass
