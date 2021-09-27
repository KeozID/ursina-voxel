from ursina import *    
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()
build = "4"

window.exit_button.visible = True
window.fps_counter.enabled = True
window.title = "3D Voxel"


#assets_texture
cobblestone = load_texture('assets/texture/cobblestone.png')
diamond = load_texture('assets/texture/diamond.png')
#assets_audio
placeblocksound = Audio('assets/sound/stone1.ogg', loop=False, autoplay=False)
destroyblocksound = Audio('assets/sound/stone2.ogg', loop=False, autoplay=False)

block_select = 1

# ─── FUNCTION ───────────────────────────────────────────────────────────────────


def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.anim_act()
    else:
        hand.anim_pas()

    global block_select
    if held_keys['1']: block_select = 1
    if held_keys['2']: block_select = 2
    if held_keys['3']: block_select = 3
    if held_keys['4']: block_select = 4
    if held_keys['5']: block_select = 5

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture = 'grass'):
        super().__init__(
            parent = scene,
            position = position, 
            model = 'cube',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            highlight_color = color.gray
        )

    def input(self,key):
        if self.hovered:
            if key == 'right mouse down':
                placeblocksound.play()
                if block_select == 1:
                    voxel = Voxel(position=self.position + mouse.normal, texture='white_cube')
                if block_select == 2:
                    voxel = Voxel(position=self.position + mouse.normal, texture='grass')
                if block_select == 3:
                    voxel = Voxel(position=self.position + mouse.normal, texture='brick')
                if block_select == 4:
                    voxel = Voxel(position=self.position + mouse.normal, texture=cobblestone)
                if block_select == 5:
                    voxel = Voxel(position=self.position + mouse.normal, texture=diamond)
            if key == 'left mouse down':
                destroyblocksound.play()
                destroy(self)


class skybox(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = 'sky_default',
            scale = 300,
            double_sided = True
        )


class hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'cube',
            texture = 'white_cube',
            color = color.rgb(255, 178, 102),
            scale = (0.2, 0.2, 0.5),
            position = Vec2(0.5, -0.48),
            rotation = Vec3(150, -50, 60)
        )
    
    def anim_act(self):
        self.position = Vec2(0.3, -0.5)
        self.rotation = Vec3(180, -35, 60)

    def anim_pas(self):
        self.position = Vec2(0.5, -0.48)
        self.rotation = Vec3(150, -50, 60)


# ────────────────────────────────────────────────────────────────────────────────

for z in range(15):
    for x in range(15):
        voxel = Voxel(position=(x,0,z))

player = FirstPersonController(
    mouse_sensitivity = Vec2(40, 40),
    speed = 5,
    jump_duration = 0.23,
    jump_height = 1
)
sky_box = skybox()
hand = hand()

fullscreen_text = Text(text="Press 'F11' to enter fullscreen", position=(0.4, 0.5, 0), color=color.red)
gametext = Text(text="3d_voxel_alpha", position=(-0.8, 0.5, 0), color=color.blue)
vertext = Text(text="dev_build-" + build, position=(-0.8, 0.45, 0), color=color.blue)
control_text = Text(text="Press 'ALT+F4' to exit, Press 'F5' to reload", position=(-0.8, -0.47, 0), color=color.black)


app.run()