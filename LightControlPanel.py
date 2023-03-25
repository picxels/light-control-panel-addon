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
    "version": (1, 2),
    "blender": (3, 4, 1),
    "location": "View3D > Right-Click(ObjectContextMenu)",
    "description": "Aggregates all lights in the scene and opens a menu with controls",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

class LightControlPanelSettings(bpy.types.PropertyGroup):
    use_heavy_version: bpy.props.BoolProperty(name="Heavy Version", default=False)

class LIGHTCONTROL_OT_show_popup(bpy.types.Operator):
    bl_idname = "lightcontrol.show_popup"
    bl_label = "Light Control Panel"
    bl_options = {'REGISTER'}

    def execute(self, context):
        return context.window_manager.invoke_popup(self)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        addon_settings = scene.light_control_panel_settings

        layout.prop(addon_settings, "use_heavy_version")

        lights = [obj for obj in bpy.context.scene.objects if obj.type == 'LIGHT']

        for light in lights:
            box = layout.box()
            col = box.column()

            col.label(text=light.name)
            col.prop(light.data, "type", text="")
            col.prop(light.data, "energy")
            col.prop(light.data, "color", text="")
            col.prop(light.data, "shadow_soft_size", text="Size")

            if addon_settings.use_heavy_version:
                col.prop(light.data, "use_shadow")
                col.prop(light.data, "specular_factor")

                if light.data.type == 'SPOT':
                    col.prop(light.data, "spot_size", text="Spot Size")
                    col.prop(light.data, "spot_blend", text="Spot Blend")
                    col.prop(light.data, "show_cone")

                if light.data.type == 'AREA':
                    col.prop(light.data, "shape", text="Shape")
                    if light.data.shape == 'RECTANGLE':
                        col.prop(light.data, "size", text="Size X")
                        col.prop(light.data, "size_y", text="Size Y")
                    else:
                        col.prop(light.data, "size", text="Size")

def menu_func(self, context):
    self.layout.operator("lightcontrol.show_popup")

def register():
    bpy.utils.register_class(LightControlPanelSettings)
    bpy.types.Scene.light_control_panel_settings = bpy.props.PointerProperty(type=LightControlPanelSettings)

    bpy.utils.register_class(LIGHTCONTROL_OT_show_popup)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(LightControlPanelSettings)
    del bpy.types.Scene.light_control_panel_settings

    bpy.utils.unregister_class(LIGHTCONTROL_OT_show_popup)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()
