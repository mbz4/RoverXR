extends Node

signal connected
signal data
signal disconnected
signal error

var _status: int = 0
var _stream: StreamPeerTCP = StreamPeerTCP.new()

func _ready() -> void:
	_status = _stream.get_status()

func _process(_delta: float) -> void:
	_stream.poll()
	var new_status: int = _stream.get_status()
	if new_status != _status:
		_status = new_status
		match _status:
			_stream.STATUS_NONE:
				print("Disconnected from host.")
#				$VBoxContainer/Debug.text += "Disconnected from host."
				emit_signal("disconnected")
			_stream.STATUS_CONNECTING:
				print("Connecting to host...")
#				$VBoxContainer/Debug.text += "Connecting to host..."
			_stream.STATUS_CONNECTED:
				print("Connected to host.")
				#$VBoxContainer/Debug.text += "Connected to host."
				emit_signal("connected")
			_stream.STATUS_ERROR:
				print("Error with socket stream.")
				#$VBoxContainer/Debug.text += "Error with socket stream." 
				emit_signal("error")

	if _status == _stream.STATUS_CONNECTED:
		var available_bytes: int = _stream.get_available_bytes()
		if available_bytes > 0:
			print("available bytes: ", available_bytes)
			#$VBoxContainer/Debug.text += "available bytes: %x" % [available_bytes]
			var recv_data: Array = _stream.get_partial_data(available_bytes)
			# Check for read error.
			if recv_data[0] != OK:
				print("Error getting data from stream: ", recv_data[0])
				#$VBoxContainer/Debug.text += "Error getting data from stream: %x" % [data[0]]
				emit_signal("error")
			else:
				emit_signal("data", recv_data[1])

func connect_to_host(host: String, port: int) -> void:
	print("Connecting to %s:%d" % [host, port])
	#$VBoxContainer/Debug.text += "Connecting to %s:%d" % [host, port]
	# Reset status so we can tell if it changes to error again.
	_status = _stream.STATUS_NONE
	if _stream.connect_to_host(host, port) != OK:
		print("Error connecting to host.")
		#$VBoxContainer/Debug.text += "Error connecting to host."
		emit_signal("error")

func send(send_data: PackedByteArray) -> bool:
	if _status != _stream.STATUS_CONNECTED:
		print("Error: Stream is not currently connected.")
		#$VBoxContainer/Debug.text += "Error: Stream is not currently connected."
		return false
	var send_error: int = _stream.put_data(send_data)
	if send_error != OK:
		print("Error writing to stream: ", error)
		#$VBoxContainer/Debug.text += "Error writing to stream: %x" % [error]
		return false
	return true
