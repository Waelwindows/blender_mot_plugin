bl_info = {
    "name": "SEGA motion .bin format",
    "author": "Waelwindows",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "SEGA .bin motion files",
    "warning": "",
    # "doc_url": "{BLENDER_MANUAL_URL}/addons/import_export/scene_fbx.html",
    # "support": 'OFFICIAL',
    "category": "Import-Export",
}

import os
print(os.getcwd())

if "bpy" in locals():
    import importlib
    if "import_mot" in locals():
        importlib.reload(import_mot)

import bpy
from bpy.props import (
        StringProperty,
        BoolProperty,
        FloatProperty,
        EnumProperty,
        CollectionProperty,
        )
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        orientation_helper,
        path_reference_mode,
        axis_conversion,
        )

class ImportMOT(bpy.types.Operator, ImportHelper):
    """Load a SEGA motion .bin file"""
    bl_idname = "import_scene.motbin"
    bl_label = "Import SEGA motion .bin"
    bl_options = {'UNDO', 'PRESET'}

    filename_ext = ".bin"
    filter_glob: StringProperty(default="*.bin", options={'HIDDEN'})

    files: CollectionProperty(
            name="File Path",
            type=bpy.types.OperatorFileListElement,
            )
    mot_db_path: StringProperty(
            name="Motion DB path",
            description="The path to the game's respective motion db. (usually named mot_db.bin)",
            subtype="FILE_PATH",
            )
    
    bone_db_path: StringProperty(
            name="Bone DB path",
            description="The path to the game's respective bone db. (usually named bone_data.bin)",
            subtype="FILE_PATH",
            )

    def draw(self, context):
        pass

    def execute(self, context):
        from . import mot
        from . import import_mot
        import os

        if self.files:
            ret = {'CANCELLED'}
            dirname = os.path.dirname(self.filepath)
            for file in self.files:
                path = os.path.join(dirname, file.name)
                mot = mot.read_mot(path, self.mot_db_path, self.bone_db_path)
                import_mot.import_mot(mot)
            ret = {'FINISHED'}
            return ret

class MOT_PT_import_include(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Include"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "IMPORT_SCENE_OT_motbin"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, "mot_db_path")
        layout.prop(operator, "bone_db_path")

def menu_func_import(self, context):
    self.layout.operator(ImportMOT.bl_idname, text="SEGA Motion Set (mot_*.bin)")

classes = (
    ImportMOT,
    MOT_PT_import_include,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    # bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    # bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
