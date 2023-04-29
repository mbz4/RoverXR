extends Node

var socket = WebSocketPeer.new()
var ws_url : String = "ws://192.168.199.228:3333"

# stream fps vars
var meas_fps_start = Time.get_ticks_msec()
var fps_update_interval = 1000 # ms
var fps_counter : int = 0
var time_elapsed : float = 0
var fps : float = 0
#var packet_delay : float = 0.0 # [ms] 

func _ready():
	socket.set_inbound_buffer_size(3145728)
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

func _handle_connect(DELAY : float) -> void:
	await get_tree().create_timer(DELAY).timeout
	if socket.connect_to_url(ws_url) == OK:
		print("Connected to %s" % [ws_url])
		set_process(true) # Keep the connection open
	else:
		print("Failed to connect to %s" % [ws_url])

func _handle_stream(data: PackedByteArray) -> void:
	var frame = Image.new()
	var error = frame.load_jpg_from_buffer(data) 
	if error == OK:
		$"../TextureRect".texture = ImageTexture.create_from_image(frame)
	else:
		print("Failed to load received image, error code %s" % [error])
		pass
	#calc_FPS()
	
func calc_FPS() -> void:	
	fps_counter += 1
	time_elapsed = Time.get_ticks_msec() - meas_fps_start
	$"../FPS".text = "Delay [ms] " + str(time_elapsed)
	meas_fps_start = Time.get_ticks_msec()
	if time_elapsed > fps_update_interval:
#		$"../VBoxContainer/Debug".text += "stream delay [ms] %d\n" % [time_elapsed]
		fps = snapped(fps_counter/(time_elapsed/1000.0), 0.01)
		$"../FPS".text = "\nPress ESC to exit"+"\nFPS " + str(fps)
		fps_counter = 0
		meas_fps_start = Time.get_ticks_msec()

func _input(event):
	if event.is_action_pressed("Send"):
		ws_send($"../VBoxContainer/Input".text)
	if event.is_action_pressed("Close"):
		socket.close(1000)
		await get_tree().create_timer(4.0).timeout
		get_tree().quit()

func ws_send(msg):
	var state = socket.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		#print("Sending to server: %s" % [msg])
		var string_buffer = msg.to_utf8_buffer()
		socket.put_packet(string_buffer)
	else:
		print("Message send failed.")

func _on_send_button_pressed():
	ws_send($"../VBoxContainer/HBoxContainer/SendButton".text)
