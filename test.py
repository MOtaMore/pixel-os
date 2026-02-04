"""
Script de prueba para verificar que todos los componentes funcionen
"""
import sys
import os

def test_imports():
    """Prueba que todos los módulos se importen correctamente"""
    print("🧪 Probando imports...")
    
    try:
        from core.engine import PixelOS
        print("  ✅ core.engine")
    except Exception as e:
        print(f"  ❌ core.engine: {e}")
        return False
    
    try:
        from core.window_manager import WindowManager, Window
        print("  ✅ core.window_manager")
    except Exception as e:
        print(f"  ❌ core.window_manager: {e}")
        return False
    
    try:
        from core.theme_manager import ThemeManager
        print("  ✅ core.theme_manager")
    except Exception as e:
        print(f"  ❌ core.theme_manager: {e}")
        return False
    
    try:
        from core.plugin_manager import PluginManager, Application
        print("  ✅ core.plugin_manager")
    except Exception as e:
        print(f"  ❌ core.plugin_manager: {e}")
        return False
    
    try:
        from ui.desktop import Desktop, DesktopIcon
        print("  ✅ ui.desktop")
    except Exception as e:
        print(f"  ❌ ui.desktop: {e}")
        return False
    
    try:
        from ui.taskbar import TaskBar, TaskBarButton
        print("  ✅ ui.taskbar")
    except Exception as e:
        print(f"  ❌ ui.taskbar: {e}")
        return False
    
    try:
        from apps.builtin_apps import TerminalApp, TextEditorApp, FileManagerApp, SettingsApp
        print("  ✅ apps.builtin_apps")
    except Exception as e:
        print(f"  ❌ apps.builtin_apps: {e}")
        return False
    
    try:
        from config.settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
        print("  ✅ config.settings")
    except Exception as e:
        print(f"  ❌ config.settings: {e}")
        return False
    
    return True


def test_config():
    """Prueba la configuración"""
    print("\n🧪 Probando configuración...")
    
    try:
        from config.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, Colors,
                                     BASE_DIR, ASSETS_DIR, FONTS_DIR)
        
        assert SCREEN_WIDTH > 0, "SCREEN_WIDTH debe ser positivo"
        assert SCREEN_HEIGHT > 0, "SCREEN_HEIGHT debe ser positivo"
        assert FPS > 0, "FPS debe ser positivo"
        
        # Verificar colores
        assert len(Colors.PINK) == 3, "Color debe ser RGB (3 valores)"
        assert all(0 <= c <= 255 for c in Colors.PINK), "Valores RGB deben estar entre 0-255"
        
        # Verificar rutas
        assert os.path.exists(BASE_DIR), "BASE_DIR debe existir"
        assert os.path.exists(ASSETS_DIR), "ASSETS_DIR debe existir"
        assert os.path.exists(FONTS_DIR), "FONTS_DIR debe existir"
        
        print("  ✅ Configuración válida")
        return True
    
    except AssertionError as e:
        print(f"  ❌ {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_resources():
    """Prueba que los recursos existan"""
    print("\n🧪 Probando recursos...")
    
    from config.settings import FONT_PATH, SYSTEM_LOGO
    
    # Verificar fuente
    if os.path.exists(FONT_PATH):
        print("  ✅ Fuente Monocraft encontrada")
    else:
        print("  ⚠️ Fuente Monocraft no encontrada (se usará fuente por defecto)")
    
    # Verificar logo
    if os.path.exists(SYSTEM_LOGO):
        print("  ✅ Logo del sistema encontrado")
    else:
        print("  ⚠️ Logo del sistema no encontrado")
    
    return True


def test_mods():
    """Prueba que los mods se carguen correctamente"""
    print("\n🧪 Probando sistema de mods...")
    
    try:
        from config.settings import MODS_DIR
        
        if not os.path.exists(MODS_DIR):
            print("  ⚠️ Directorio de mods no existe")
            return False
        
        # Contar archivos .py en mods
        mod_files = [f for f in os.listdir(MODS_DIR) 
                     if f.endswith('.py') and f != '__init__.py']
        
        print(f"  ✅ {len(mod_files)} archivo(s) de mods encontrado(s)")
        
        # Intentar importar mods de ejemplo
        try:
            from mods.calculator_example import CalculatorApp
            print("  ✅ calculator_example.py importado")
        except ImportError:
            print("  ⚠️ calculator_example.py no encontrado")
        
        try:
            from mods.paint_example import PaintApp
            print("  ✅ paint_example.py importado")
        except ImportError:
            print("  ⚠️ paint_example.py no encontrado")
        
        return True
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_pygame():
    """Prueba que pygame esté instalado"""
    print("\n🧪 Probando Pygame...")
    
    try:
        import pygame
        print(f"  ✅ Pygame {pygame.version.ver} instalado")
        
        # Probar inicialización
        pygame.init()
        print("  ✅ Pygame inicializado correctamente")
        pygame.quit()
        
        return True
    
    except ImportError:
        print("  ❌ Pygame no está instalado")
        print("     Ejecuta: pip install pygame")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║       🧪 Tests de Pixel-OS v1.0 🧪       ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """)
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Pygame", test_pygame()))
    results.append(("Imports", test_imports()))
    results.append(("Configuración", test_config()))
    results.append(("Recursos", test_resources()))
    results.append(("Mods", test_mods()))
    
    # Resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:20} {status}")
    
    print("="*50)
    print(f"\n{'✅ TODOS LOS TESTS PASARON' if passed == total else f'⚠️ {total - passed} TEST(S) FALLARON'}")
    print(f"Resultado: {passed}/{total} ({(passed/total)*100:.1f}%)\n")
    
    if passed == total:
        print("🎉 ¡Pixel-OS está listo para usar!")
        print("   Ejecuta: python main.py")
    else:
        print("⚠️ Algunos componentes tienen problemas.")
        print("   Revisa los errores arriba.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
