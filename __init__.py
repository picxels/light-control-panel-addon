# LightControl panel for Blender
# A simple and intuitive way to control the lighting in your scenes
# Created by Sergiu Tavitian with love and passion
# Enjoy and happy blending!
#-------------------------------------------------------------------
#   / \  / \  / \  / \  / \  / \  / \  / \  / \  / \  / \  / \  
#  ( L )( i )( g )( h )( t )( C )( o )( n )( t )( r )( o )( l )
#   \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/ 
#   
#  
#
#    _    _    _    _    _  
#   / \  / \  / \  / \  / \  / \  / \  / \  / \ 
#  ( B )( l )( e )( n )( d )( e )( r )(-3 )( D )
#   \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/
# 
#  
# 
#
#                        /\___/\
#                       ( =^.^= )
#                        (")_(")_/regards from Gigi the cat.
    


import bpy

bl_info = {
    "name": "Light Control Panel",
    "author": "Sergiu Tavitian",
    "version": (1, 4),
    "blender": (4, 3, 0),
    "location": "View3D > Right-Click(ObjectContextMenu)",
    "description": "Aggregates all lights in the scene and opens a menu with controls",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

class LIGHTCONTROL_OT_show_popup(bpy.types.Operator):
    bl_idname = "lightcontrol.show_popup"
    bl_label = "Light Control Panel"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT'

    def execute(self, context):
        return context.window_manager.invoke_popup(self, width=300)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Light Control Panel", icon='LIGHT')
        layout.separator()

        scene = context.scene
        layout.prop(scene, "light_control_mode", expand=True)

        lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
        
        if not lights:
            layout.label(text="No lights found in the scene.", icon='ERROR')
            return

        for light in lights:
            box = layout.box()
            col = box.column()

            col.label(text=f"Light: {light.name}", icon='LIGHT')
            col.prop(light.data, "type", text="Type")
            col.prop(light.data, "energy", text="Energy")
            col.prop(light.data, "color", text="Color")
            col.prop(light.data, "shadow_soft_size", text="Size")

            if scene.light_control_mode == 'HEAVY':
                col.prop(light.data, "specular_factor", text="Specular")
                col.prop(light.data, "shadow_buffer_clip_start", text="Clip Start")
                col.prop(light.data, "shadow_buffer_clip_end", text="Clip End")

def menu_func(self, context):
    self.layout.operator(LIGHTCONTROL_OT_show_popup.bl_idname, text="Light Control Panel")

def register():
    bpy.utils.register_class(LIGHTCONTROL_OT_show_popup)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

    bpy.types.Scene.light_control_mode = bpy.props.EnumProperty(
        items=[
            ('LIGHT', 'Light', 'Basic light control'),
            ('HEAVY', 'Heavy', 'Advanced light control')],
        name="Light Control Mode",
        default='LIGHT'
    )

def unregister():
    bpy.utils.unregister_class(LIGHTCONTROL_OT_show_popup)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    del bpy.types.Scene.light_control_mode

if __name__ == "__main__":
    register()


