extends Sprite3D
@onready var WS_CONF = get_node("/root/WebsocketConfig")
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
#	$SubViewport.size = $SubViewport/RichTextLabel.rect_size
	$SubViewport/RichTextLabel.text = WS_CONF.ws_url
	pass
