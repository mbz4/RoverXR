extends VideoStreamPlayer

# H264 MJPEG MKV stream from RPi Zero 1 W
#const MJPEG_STREAM_URL = "tcp://192.168.199.228"
#var http_client = null
#var buffer = PackedByteArray()
#var current_image = null
const PI_STREAM_HOST = "192.168.199.228"
const PI_STREAM_PORT = 3333


# Called when the node enters the scene tree for the first time.
func _ready():
#	var streamTCP = StreamPeerTCP.new()
#	streamTCP.connect_to_host(PI_STREAM_HOST, PI_STREAM_PORT)
#	if streamTCP.get_status() == 1:
#		print("Connecting...")
#	if streamTCP.get_status() == 2:
#		print("Connected!")
#		pass
	pass
	#pass
	## Set up HTTP client.
	#http_client = HTTPClient.new()
	#http_client.connect("request_completed", self, "_on_http_request_completed")
	#http_client.request(MJPEG_STREAM_URL)

#func search_two(byte1, byte2):
#	# run thru indices and return index of ffd8 & ffd9
#	pass

## Called when an HTTP request is completed.
#func _on_http_request_completed(result, response_code, headers, body):
	# Check if the request was successful.
	#if result == HTTPClient.STATUS_CONNECTED:
	#	# Add the received data to the buffer.
	#	buffer.append(body)
	#	# Find the end of the previous JPEG image and the start of the next one.
	#	start_of_image = buffer.find("\uffd8")
	#	end_of_image = buffer.find("\uffd9", start_of_image)
	#	# If we found a complete JPEG image, extract it and load it into Godot.
	#	if start_of_image != -1 and end_of_image != -1:
	#		image_data = buffer.subarray(start_of_image, end_of_image + 2)
	#		current_image = Image.load_jpg_from_buffer(image_data)
	#		buffer = buffer.subarray(end_of_image + 2)
	# Send a new request to continue receiving the MJPEG stream.
	#http_client.request(MJPEG_STREAM_URL)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	#if current_image != null:
	#	# Create a new texture from the current image and set it on a mesh instance.
	#	var texture = Texture.new()
	#	texture.create_from_image(current_image)
	#	var _mesh_instance = MeshInstance3D.new()
	#	mesh_instance.set_mesh()
	#	mesh_instance.set_texture(texture)
	#	add_child(mesh_instance)
	#	current_image = null
	pass
