extends Node

const HOST: String = "localhost"
const PORT: int = 5000
const RECONNECT_TIMEOUT: float = 1.0

const Client = preload("res://tcp_client.gd")
var _client: Client = Client.new()

func _ready() -> void:
	_client.connect("connected", Callable(self, "_handle_client_connected"))
	_client.connect("disconnected", Callable(self, "_handle_client_disconnected"))
	_client.connect("error", Callable(self, "_handle_client_error"))
	_client.connect("data", Callable(self, "_handle_client_data"))
	add_child(_client)
	_client.connect_to_host(HOST, PORT)

func _connect_after_timeout(timeout: float) -> void:
	await get_tree().create_timer(RECONNECT_TIMEOUT).timeout
	_client.connect_to_host(HOST, PORT)

func _handle_client_connected() -> void:
	print("Client connected to server.")
	$"../VBoxContainer/Debug".text += "Client connected to server." + "\n"

func _input(event):
	if event.is_action_pressed("Send"):
		#$"../VBoxContainer/Debug".text += "Send message."
		_client.send($"../VBoxContainer/Input".text.to_utf8_buffer())
	#if event.is_action_pressed("Close"):
	#	socket.close(1000)

func _on_send_button_pressed():
	#$"../VBoxContainer/Debug".text += "Send message."
	_client.send($"../VBoxContainer/Input".text.to_utf8_buffer())

func _handle_client_data(data: PackedByteArray) -> void:
	print("Client data: ", data.get_string_from_utf8())
	var payload = data.get_string_from_utf8()
	$"../VBoxContainer/Debug".text += "From server: " + payload  + "\n"
	#var message: PackedByteArray = [97, 99, 107] # Bytes for "ack" in ASCII
	#_client.send(message)

func _handle_client_disconnected() -> void:
	print("Client disconnected from server.")
	$"../VBoxContainer/Debug".text += "Client disconnected from server." + "\n"
	_connect_after_timeout(RECONNECT_TIMEOUT) # Try to reconnect after 3 seconds

func _handle_client_error() -> void:
	print("Client error.")
	$"../VBoxContainer/Debug".text += "Client error." + "\n"
	_connect_after_timeout(RECONNECT_TIMEOUT) # Try to reconnect after 3 seconds
