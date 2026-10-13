from pathlib import Path

def replace_exact(path, before, after):
    p = Path("material-eleven") / path
    s = p.read_text()
    if s.count(before) != 1:
        raise RuntimeError(f"El codigo base de {path} cambio: {s.count(before)} coincidencias")
    p.write_text(s.replace(before, after, 1))

# Con el modo digital el pad no entrega rx. ElevenMPV-A usa rx
# para pasar pistas durante el modo de ahorro de energia.
replace_exact("source/main.c",
    "#include <psp2/apputil.h>\n",
    "#include <psp2/apputil.h>\n#include <psp2/ctrl.h>\n")
replace_exact("source/main.c",
    "\tUI_Debug_MarkStackBase();\n",
    "\tUI_Debug_MarkStackBase();\n"
    "\t// Habilitar las coordenadas de los sticks en el pad.\n"
    "\tsceCtrlSetSamplingMode(SCE_CTRL_MODE_ANALOG);\n")

replace_exact("source/utils.c",
    "static ScreenOff_State screen_off = { SCE_CTRL_START, SCE_CTRL_LTRIGGER, SCE_CTRL_RTRIGGER, 1 };\n",
    "static ScreenOff_State screen_off = { SCE_CTRL_START, SCE_CTRL_LTRIGGER, SCE_CTRL_RTRIGGER, 1 };\n"
    "// Se arma tras apagar la pantalla con START. No fuerza encendido.\n"
    "static int stick_screen_off = 0;\n"
    "static int stick_ready = 0;\n")

replace_exact("source/utils.c",
    "\tmemset(&pad, 0, sizeof(SceCtrlData));\n"
    "\tsceCtrlPeekBufferPositive(0, &pad, 1);\n",
    "\tmemset(&pad, 0, sizeof(SceCtrlData));\n"
    "\tint pad_valid = sceCtrlPeekBufferPositive(0, &pad, 1) > 0;\n")

replace_exact("source/utils.c",
    "\tif (action == SCREEN_OFF_TURN_OFF)\n"
    "\t\tscePowerRequestDisplayOff();\n",
    "\tif (action == SCREEN_OFF_TURN_OFF) {\n"
    "\t\t// Activar escucha del stick. Requiere volver al centro primero.\n"
    "\t\tstick_screen_off = 1;\n"
    "\t\tstick_ready = 0;\n"
    "\t\tscePowerRequestDisplayOff();\n"
    "\t}\n")

replace_exact("source/utils.c",
    "\tlist_step = KeyRepeat_Update(&key_repeat, pad.buttons & ~SCE_CTRL_START, pressed, sceKernelGetProcessTimeWide());\n",
    "\tlist_step = KeyRepeat_Update(&key_repeat, pad.buttons & ~SCE_CTRL_START, pressed, sceKernelGetProcessTimeWide());\n"
    "\n"
    "\t// Al volver a usar el menu, terminar el modo de control a ciegas.\n"
    "\t// No se recibe el PS por la API normal: la siguiente pulsacion\n"
    "\t// de navegacion cancela el modo, sin tocar L/R.\n"
    "\tif (pressed & (SCE_CTRL_UP | SCE_CTRL_DOWN | SCE_CTRL_LEFT |\n"
    "\t               SCE_CTRL_RIGHT | SCE_CTRL_CROSS | SCE_CTRL_CIRCLE |\n"
    "\t               SCE_CTRL_TRIANGLE | SCE_CTRL_SQUARE | SCE_CTRL_SELECT)) {\n"
    "\t\tstick_screen_off = 0;\n"
    "\t\tstick_ready = 0;\n"
    "\t}\n"
    "\n"
    "\t// Inspirado en ElevenMPV-A: rx bajo = anterior, alto = siguiente.\n"
    "\t// Se ejecuta en el mismo hilo de Music_Update, nunca en paralelo\n"
    "\t// con el decodificador. Una vez por movimiento, hasta volver al centro.\n"
    "\tif (stick_screen_off && pad_valid && Audio_HasTrack()) {\n"
    "\t\tunsigned int rx = pad.rx;\n"
    "\t\tif (rx >= 0x60 && rx <= 0xA0)\n"
    "\t\t\tstick_ready = 1;\n"
    "\t\telse if (stick_ready && rx < 0x20) {\n"
    "\t\t\tstick_ready = 0;\n"
    "\t\t\tMusic_Previous();\n"
    "\t\t}\n"
    "\t\telse if (stick_ready && rx > 0xDF) {\n"
    "\t\t\tstick_ready = 0;\n"
    "\t\t\tMusic_Next();\n"
    "\t\t}\n"
    "\t}\n")

src = Path("material-eleven/source/utils.c").read_text()
assert src.count("Music_Previous();") == 1
assert src.count("Music_Next();") == 1
assert "scePowerRequestDisplayOff();" in src
print("Parche stick derecho aplicado. Con START la pantalla se apaga realmente.")
