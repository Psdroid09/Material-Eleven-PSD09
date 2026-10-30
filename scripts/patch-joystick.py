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
    "static int stick_ready = 0;\n"
    "static int stick_candidate = 0;\n"
    "static int stick_candidate_samples = 0;\n"
    "#define STICK_CENTER_MIN 0x60\n"
    "#define STICK_CENTER_MAX 0xA0\n"
    "#define STICK_LEFT_LIMIT 0x20\n"
    "#define STICK_RIGHT_LIMIT 0xDF\n"
    "#define STICK_CONFIRM_SAMPLES 2\n")

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
    "\t\tstick_candidate = 0;\n"
    "\t\tstick_candidate_samples = 0;\n"
    "\t}\n"
    "\n"
    "\t// El stick debe permanecer dos lecturas consecutivas en el extremo.\n"
    "\t// Un pico aislado o una lectura fallida no cambia la pista.\n"
    "\t// La zona central rearma un solo cambio por movimiento completo.\n"
    "\tif (stick_screen_off && Audio_HasTrack()) {\n"
    "\t\tif (!pad_valid) {\n"
    "\t\t\tstick_candidate = 0;\n"
    "\t\t\tstick_candidate_samples = 0;\n"
    "\t\t}\n"
    "\t\telse {\n"
    "\t\t\tint direction = 0;\n"
    "\t\t\tunsigned int rx = pad.rx;\n"
    "\t\t\tif (rx >= STICK_CENTER_MIN && rx <= STICK_CENTER_MAX) {\n"
    "\t\t\t\tstick_ready = 1;\n"
    "\t\t\t\tstick_candidate = 0;\n"
    "\t\t\t\tstick_candidate_samples = 0;\n"
    "\t\t\t}\n"
    "\t\t\telse if (rx < STICK_LEFT_LIMIT)\n"
    "\t\t\t\tdirection = -1;\n"
    "\t\t\telse if (rx > STICK_RIGHT_LIMIT)\n"
    "\t\t\t\tdirection = 1;\n"
    "\t\t\telse {\n"
    "\t\t\t\tstick_candidate = 0;\n"
    "\t\t\t\tstick_candidate_samples = 0;\n"
    "\t\t\t}\n"
    "\t\t\tif (stick_ready && direction != 0) {\n"
    "\t\t\t\tif (direction == stick_candidate)\n"
    "\t\t\t\t\tstick_candidate_samples++;\n"
    "\t\t\t\telse {\n"
    "\t\t\t\t\tstick_candidate = direction;\n"
    "\t\t\t\t\tstick_candidate_samples = 1;\n"
    "\t\t\t\t}\n"
    "\t\t\t\tif (stick_candidate_samples >= STICK_CONFIRM_SAMPLES) {\n"
    "\t\t\t\t\tstick_ready = 0;\n"
    "\t\t\t\t\tstick_candidate = 0;\n"
    "\t\t\t\t\tstick_candidate_samples = 0;\n"
    "\t\t\t\t\tif (direction < 0)\n"
    "\t\t\t\t\t\tMusic_Previous();\n"
    "\t\t\t\t\telse\n"
    "\t\t\t\t\t\tMusic_Next();\n"
    "\t\t\t\t}\n"
    "\t\t\t}\n"
    "\t\t}\n"
    "\t}\n")

src = Path("material-eleven/source/utils.c").read_text()
assert src.count("Music_Previous();") == 1
assert src.count("Music_Next();") == 1
assert "scePowerRequestDisplayOff();" in src
print("Parche stick derecho aplicado. Con START la pantalla se apaga realmente.")
