# --------------------------------------------------------------------------------
# Script Name: UDIM Mover Tool
# Description: This script creates a Maya UI tool for moving UVs across UDIM tiles.
#              It allows the user to reset UVs to a default position, move them in
#              four directions, and jump to specific UDIM tiles.
# Usage: The script is executed in Maya's Python environment.
# Author: Kai Mallari
# Created: February 2024
# --------------------------------------------------------------------------------

import maya.cmds as mc


# Move selected UV shells up one UDIM grid tile
def move_udim_up():
    """
    Moves selected UV shells up one UDIM grid tile by increasing the V value.
    """
    mc.polyMoveUV(translateV=1)


# Move selected UV shells down one UDIM grid tile
def move_udim_down():
    """
    Moves selected UV shells down one UDIM grid tile by decreasing the V value.
    """
    mc.polyMoveUV(translateV=-1)


# Move selected UV shells left one UDIM grid tile
def move_udim_left():
    """
    Moves selected UV shells left one UDIM grid tile by decreasing the U value.
    """
    mc.polyMoveUV(translateU=-1)


# Move selected UV shells right one UDIM grid tile
def move_udim_right():
    """
    Moves selected UV shells right one UDIM grid tile by increasing the U value.
    """
    mc.polyMoveUV(translateU=1)


# Reset UVs to UDIM tile 1001
def set_udim_1001():
    """
    Sets the selected UV shells to UDIM tile 1001 (origin).
    This function is the basis for moving UVs to a "reset" position before applying other transformations.

    Utilizes the current selection in Maya. No return values.

    To use this as a reset in other functions (like `set_udim_preset_1`),
    call it at the beginning to ensure UVs move to an absolute position, not a relative one.
    """
    selected_components = mc.ls(selection=True, flatten=True)
    selected_UV_verts = mc.polyListComponentConversion(selected_components, toUV=True)
    uv_vert_value = mc.polyEditUV(selected_UV_verts[0], query=True)
    u_value = uv_vert_value[0]
    v_value = uv_vert_value[1]
    reset_u_value = (u_value // 1) * -1
    reset_v_value = (v_value // 1) * -1
    mc.polyMoveUV(translateU=reset_u_value, translateV=reset_v_value)


# --------------------------------------------------------------------------------
# HOW TO ADD A UDIM PRESET
#
# 1. Create a button using the Maya UI code inside `create_udim_mover_ui()`
# 2. Call the command "set_udim(preset_udim=1001)"
# 3. Change the `preset_udim` parameter to the desired UDIM location for the preset
#
# UDIM values start at 1001 for origin
# To increase the U value, increment the ten's digit
# To increase the V value, increment the one's digit
# --------------------------------------------------------------------------------

# Move selected UV shells to a preset UDIM tile
def set_udim(preset_udim=1001):
    """
    Moves selected UV shells to a preset location.
    Involves resetting the UV position to UDIM 1001, then moving to desired position.

    Parameters:
        preset_udim (int): 4 digit UDIM coordinate value
    """
    set_udim_1001()  # Reset to origin before moving to preset location
    target_udim_u_value = int(str(preset_udim - 1)[3])  # Third character (ten's digit) in the UDIM value
    target_udim_v_value = int(str(preset_udim)[2])  # Fourth character (ten's digit) in the UDIM value
    mc.polyMoveUV(translateU=target_udim_u_value, translateV=target_udim_v_value)  # Moves selected UV Shell


# Creates the main UI window with all controls and layouts
def create_udim_mover_ui():
    if mc.window("uv_mover", exists=True):
        mc.deleteUI("uv_mover", window=True)

    # Make a new window
    mc.window("uv_mover", title="UDIM Mover", iconName="UDIM Mover", width=(250), sizeable=False)
    button_width = 200
    button_height = 25

    # Main column layout for the buttons
    mc.columnLayout(adjustableColumn=True)

    # Add a button for resetting UVs to default UDIM tile (1001)
    mc.button(label="Reset UVs to UDIM-1001", command="set_udim_1001()")
    mc.separator(height=20)

    # Arrange buttons for moving UVs in a row layout - Top row with a single active button
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=3)
    mc.button(label="", enable=False, width=button_width, height=button_height)  # Placeholder for alignment
    mc.button(label="Move Selected UVs Up", command="move_udim_up()", width=button_width, height=button_height)
    mc.button(label="", enable=False, width=button_width, height=button_height)  # Placeholder for alignment

    # Middle row with buttons to move UVs left and right
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=3)
    mc.button(label="Move Selected UVs Left", command="move_udim_left()", width=button_width, height=button_height)
    mc.button(label="Move Selected UVs Down", command="move_udim_down()", width=button_width, height=button_height)
    mc.button(label="Move Selected UVs Right", command="move_udim_right()", width=button_width, height=button_height)
    mc.setParent("..")

    # Add a button to move UVs to a specific UDIM tile (1026)
    mc.separator(height=20)  # Add Separator
    mc.button(label="Move Selected UVs to UDIM-1026", command="set_udim(preset_udim=1026)")

    # Add a button to move UVs to a specific UDIM tile (1062)
    mc.separator(height=20)  # Add Separator
    mc.button(label="Move Selected UVs to UDIM-1062", command="set_udim(preset_udim=1062)")

    # Display the constructed UI window
    mc.showWindow("uv_mover")


# Entry point for creating and displaying the UI
create_udim_mover_ui()
