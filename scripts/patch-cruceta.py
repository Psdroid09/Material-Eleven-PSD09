from pathlib import Path
p = Path("material-eleven/source/utils.c")
s = p.read_text()

def replace1(old, new):
    global s
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f"No coincide codigo original ({count} coincidencias): {old[:50]!r}")
    s = s.replace(old, new, 1)

replace1(
    "static ScreenOff_State screen_off = { SCE_CTRL_START, SCE_CTRL_LTRIGGER, SCE_CTRL_RTRIGGER, 1 };\n",
    "static ScreenOff_State screen_off = { SCE_CTRL_START, SCE_CTRL_LTRIGGER, SCE_CTRL_RTRIGGER, 1 };\n"
    "// El modo de cruceta se activa unicamente despues de START.\n"
    "static int dpad_screen_off = 0;\n"
    "static SceUInt32 dpad_old = 0;\n")

replace1(
    "\tmemset(&pad, 0, sizeof(SceCtrlData));\n"
    "\tsceCtrlPeekBufferPositive(0, &pad, 1);\n",
    "\tmemset(&pad, 0, sizeof(SceCtrlData));\n"
    "\tsceCtrlPeekBufferPositive(0, &pad, 1);\n"
    "\t// La lectura Ext es experimental: algunos botones digitales\n"
    "\t// pueden estar interceptados en modo pantalla apagada.\n"
    "\tSceCtrlData ext_pad;\n"
    "\tmemset(&ext_pad, 0, sizeof(ext_pad));\n"
    "\tif (dpad_screen_off && sceCtrlPeekBufferPositiveExt(0, &ext_pad, 1) > 0)\n"
    "\t\tpad.buttons |= ext_pad.buttons & (SCE_CTRL_LEFT | SCE_CTRL_RIGHT);\n")

replace1(
    "\tif (action == SCREEN_OFF_TURN_OFF)\n"
    "\t\tscePowerRequestDisplayOff();\n",
    "\tif (action == SCREEN_OFF_TURN_OFF) {\n"
    "\t\tdpad_screen_off = 1;\n"
    "\t\tdpad_old = 0;\n"
    "\t\tscePowerRequestDisplayOff();\n"
    "\t}\n")

replace1(
    "\tlist_step = KeyRepeat_Update(&key_repeat, pad.buttons & ~SCE_CTRL_START, pressed, sceKernelGetProcessTimeWide());\n",
    "\t// Solo una cancion por pulsacion, sin repetir mientras se mantiene.\n"
    "\t// Solo se activan estos controles tras apagar con START.\n"
    "\tif (dpad_screen_off) {\n"
    "\t\tSceUInt32 dirs = pad.buttons & (SCE_CTRL_LEFT | SCE_CTRL_RIGHT);\n"
    "\t\tSceUInt32 newly = dirs & ~dpad_old;\n"
    "\t\tif ((newly & SCE_CTRL_RIGHT) && !(dirs & SCE_CTRL_LEFT))\n"
    "\t\t\tMusic_Next();\n"
    "\t\telse if ((newly & SCE_CTRL_LEFT) && !(dirs & SCE_CTRL_RIGHT))\n"
    "\t\t\tMusic_Previous();\n"
    "\t\tdpad_old = dirs;\n"
    "\t\t// Evita mover la seleccion invisible de carpetas/biblioteca.\n"
    "\t\tpressed &= ~(SCE_CTRL_LEFT | SCE_CTRL_RIGHT);\n"
    "\t\t// Tras despertar con PS, cualquier otro boton de navegacion\n"
    "\t\t// devuelve el control normal de la cruceta.\n"
    "\t\tif (pressed & (SCE_CTRL_UP | SCE_CTRL_DOWN | SCE_CTRL_CROSS |\n"
    "\t\t               SCE_CTRL_CIRCLE | SCE_CTRL_TRIANGLE | SCE_CTRL_SQUARE |\n"
    "\t\t               SCE_CTRL_SELECT)) {\n"
    "\t\t\tdpad_screen_off = 0;\n"
    "\t\t\tdpad_old = 0;\n"
    "\t\t}\n"
    "\t}\n"
    "\tlist_step = KeyRepeat_Update(&key_repeat, pad.buttons & ~SCE_CTRL_START, pressed, sceKernelGetProcessTimeWide());\n")
p.write_text(s)
print("Integracion cruceta completada")
