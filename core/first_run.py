"""
First Run Wizard - Asistente de primera configuración estilo Windows 11
"""
from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Optional

import pygame

from config.i18n import LANGUAGE_NAMES, tr
from config.settings import (Colors, FONT_PATH, FONT_SIZE_LARGE, FONT_SIZE_MEDIUM,
                             FONT_SIZE_SMALL, FPS, SCREEN_HEIGHT, SCREEN_WIDTH,
                             SETUP_FILE, USER_DATA_DIR)


def load_setup() -> Optional[Dict]:
    """Carga la configuración inicial si existe."""
    if not os.path.exists(SETUP_FILE):
        return None
    try:
        with open(SETUP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_setup(data: Dict) -> None:
    """Guarda la configuración inicial."""
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    with open(SETUP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class FirstRunWizard:
    """Asistente de primera configuración"""

    def __init__(self, screen: pygame.Surface, theme_manager):
        self.screen = screen
        self.theme_manager = theme_manager
        self.clock = pygame.time.Clock()
        self.step = 0
        self.running = True
        self.completed = False

        self.languages = LANGUAGE_NAMES
        self.selected_language = 0

        self.apps = [
            {"id": "terminal", "name": tr("app.terminal"), "selected": True},
            {"id": "text_editor", "name": tr("app.text_editor"), "selected": True},
            {"id": "file_manager", "name": tr("app.file_manager"), "selected": True},
            {"id": "settings", "name": tr("app.settings"), "selected": True},
            {"id": "calculator", "name": tr("app.calculator"), "selected": True},
            {"id": "paint", "name": tr("app.paint"), "selected": True},
            {"id": "mini_browser", "name": tr("app.mini_browser"), "selected": False},
            {"id": "code_editor", "name": tr("app.code_editor"), "selected": False},
            {"id": "video_player", "name": tr("app.video_player"), "selected": False},
        ]

        self.account_name = ""
        self.account_password = ""
        self.active_input: Optional[str] = None

        self.back_rect = pygame.Rect(40, SCREEN_HEIGHT - 80, 140, 42)
        self.next_rect = pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 80, 140, 42)

    def run(self) -> Dict:
        """Ejecuta el asistente y devuelve la configuración seleccionada."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._render()

        selected_language = self.languages[self.selected_language]
        return {
            "language": selected_language["code"],
            "language_name": selected_language["name"],
            "apps": [app["id"] for app in self.apps if app["selected"]],
            "account": {
                "name": self.account_name.strip(),
                "password": self.account_password
            }
        }

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if self.step == 2:
                    self._handle_text_input(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(event.pos)

    def _handle_text_input(self, event: pygame.event.Event) -> None:
        if self.active_input == "name":
            if event.key == pygame.K_BACKSPACE:
                self.account_name = self.account_name[:-1]
            elif event.key == pygame.K_TAB:
                self.active_input = "password"
            elif event.unicode.isprintable() and len(self.account_name) < 24:
                self.account_name += event.unicode
        elif self.active_input == "password":
            if event.key == pygame.K_BACKSPACE:
                self.account_password = self.account_password[:-1]
            elif event.key == pygame.K_TAB:
                self.active_input = "name"
            elif event.unicode.isprintable() and len(self.account_password) < 24:
                self.account_password += event.unicode

    def _handle_mouse_click(self, pos) -> None:
        if self.back_rect.collidepoint(pos):
            if self.step > 0:
                self.step -= 1
            return

        if self.next_rect.collidepoint(pos):
            if self.step == 2:
                if self.account_name.strip():
                    self.running = False
                    self.completed = True
            else:
                self.step += 1
            return

        if self.step == 0:
            self._handle_language_click(pos)
        elif self.step == 1:
            self._handle_apps_click(pos)
        elif self.step == 2:
            self._handle_account_click(pos)

    def _handle_language_click(self, pos) -> None:
        start_y = 180
        item_height = 44
        for i, lang in enumerate(self.languages):
            rect = pygame.Rect(240, start_y + i * item_height, 800, 36)
            if rect.collidepoint(pos):
                self.selected_language = i
                return

    def _handle_apps_click(self, pos) -> None:
        start_y = 180
        item_height = 44
        for i, app in enumerate(self.apps):
            rect = pygame.Rect(240, start_y + i * item_height, 800, 36)
            if rect.collidepoint(pos):
                app["selected"] = not app["selected"]
                return

    def _handle_account_click(self, pos) -> None:
        name_rect = pygame.Rect(240, 220, 500, 40)
        pass_rect = pygame.Rect(240, 300, 500, 40)
        if name_rect.collidepoint(pos):
            self.active_input = "name"
        elif pass_rect.collidepoint(pos):
            self.active_input = "password"
        else:
            self.active_input = None

    def _render(self) -> None:
        self.screen.fill(Colors.BACKGROUND)
        self._render_header()

        if self.step == 0:
            self._render_language_step()
        elif self.step == 1:
            self._render_apps_step()
        else:
            self._render_account_step()

        self._render_footer()
        pygame.display.flip()

    def _render_header(self) -> None:
        title_font = self.theme_manager.get_font(FONT_SIZE_LARGE)
        subtitle_font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)

        title = title_font.render(tr("wizard.title"), True, Colors.TEXT_PRIMARY)
        subtitle = subtitle_font.render(tr("wizard.subtitle"), True, Colors.TEXT_SECONDARY)

        self.screen.blit(title, (240, 60))
        self.screen.blit(subtitle, (240, 100))

        # Indicador de pasos
        step_text = subtitle_font.render(
            tr("wizard.step", current=self.step + 1, total=3), True, Colors.TEXT_SECONDARY
        )
        self.screen.blit(step_text, (SCREEN_WIDTH - 240, 100))

    def _render_language_step(self) -> None:
        label_font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        label = label_font.render(tr("wizard.select_language"), True, Colors.TEXT_PRIMARY)
        self.screen.blit(label, (240, 140))

        start_y = 180
        item_height = 44
        for i, lang in enumerate(self.languages):
            rect = pygame.Rect(240, start_y + i * item_height, 800, 36)
            color = Colors.ACTIVE if i == self.selected_language else Colors.WINDOW_BG
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, Colors.BORDER, rect, width=2, border_radius=8)
            text = label_font.render(lang["name"], True, Colors.TEXT_PRIMARY)
            self.screen.blit(text, (rect.x + 12, rect.y + 8))

    def _render_apps_step(self) -> None:
        label_font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        label = label_font.render(tr("wizard.select_apps"), True, Colors.TEXT_PRIMARY)
        self.screen.blit(label, (240, 140))

        start_y = 180
        item_height = 44
        for i, app in enumerate(self.apps):
            rect = pygame.Rect(240, start_y + i * item_height, 800, 36)
            pygame.draw.rect(self.screen, Colors.WINDOW_BG, rect, border_radius=8)
            pygame.draw.rect(self.screen, Colors.BORDER, rect, width=2, border_radius=8)

            checkbox = pygame.Rect(rect.x + 12, rect.y + 8, 20, 20)
            pygame.draw.rect(self.screen, Colors.WINDOW_BG, checkbox, border_radius=4)
            pygame.draw.rect(self.screen, Colors.BORDER, checkbox, width=2, border_radius=4)
            if app["selected"]:
                pygame.draw.line(self.screen, Colors.TEXT_PRIMARY, (checkbox.x + 4, checkbox.y + 10),
                                 (checkbox.x + 9, checkbox.y + 15), 2)
                pygame.draw.line(self.screen, Colors.TEXT_PRIMARY, (checkbox.x + 9, checkbox.y + 15),
                                 (checkbox.x + 16, checkbox.y + 6), 2)

            text = label_font.render(app["name"], True, Colors.TEXT_PRIMARY)
            self.screen.blit(text, (rect.x + 44, rect.y + 8))

    def _render_account_step(self) -> None:
        label_font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        label = label_font.render(tr("wizard.create_account"), True, Colors.TEXT_PRIMARY)
        self.screen.blit(label, (240, 140))

        name_label = label_font.render(tr("wizard.username"), True, Colors.TEXT_SECONDARY)
        pass_label = label_font.render(tr("wizard.password"), True, Colors.TEXT_SECONDARY)
        self.screen.blit(name_label, (240, 190))
        self.screen.blit(pass_label, (240, 270))

        name_rect = pygame.Rect(240, 220, 500, 40)
        pass_rect = pygame.Rect(240, 300, 500, 40)

        pygame.draw.rect(self.screen, Colors.WINDOW_BG, name_rect, border_radius=8)
        pygame.draw.rect(self.screen, Colors.WINDOW_BG, pass_rect, border_radius=8)

        name_border = Colors.ACTIVE if self.active_input == "name" else Colors.BORDER
        pass_border = Colors.ACTIVE if self.active_input == "password" else Colors.BORDER
        pygame.draw.rect(self.screen, name_border, name_rect, width=2, border_radius=8)
        pygame.draw.rect(self.screen, pass_border, pass_rect, width=2, border_radius=8)

        text_font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        name_text = text_font.render(self.account_name or "", True, Colors.TEXT_PRIMARY)
        password_mask = "•" * len(self.account_password)
        pass_text = text_font.render(password_mask, True, Colors.TEXT_PRIMARY)

        self.screen.blit(name_text, (name_rect.x + 10, name_rect.y + 8))
        self.screen.blit(pass_text, (pass_rect.x + 10, pass_rect.y + 8))

        hint = self.theme_manager.get_font(FONT_SIZE_SMALL).render(
            tr("wizard.tab_hint"), True, Colors.TEXT_DISABLED
        )
        self.screen.blit(hint, (240, 350))

    def _render_footer(self) -> None:
        # Botones Back/Next
        back_color = Colors.HOVER if self.back_rect.collidepoint(pygame.mouse.get_pos()) else Colors.TASKBAR_BG
        next_color = Colors.ACTIVE if self.next_rect.collidepoint(pygame.mouse.get_pos()) else Colors.TASKBAR_BG

        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=8)
        pygame.draw.rect(self.screen, next_color, self.next_rect, border_radius=8)

        font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        back_text = font.render(tr("wizard.back"), True, Colors.TEXT_PRIMARY)
        next_label = tr("wizard.finish") if self.step == 2 else tr("wizard.next")
        next_text = font.render(next_label, True, Colors.TEXT_PRIMARY)

        self.screen.blit(back_text, (self.back_rect.centerx - back_text.get_width() // 2,
                                     self.back_rect.centery - back_text.get_height() // 2))
        self.screen.blit(next_text, (self.next_rect.centerx - next_text.get_width() // 2,
                                     self.next_rect.centery - next_text.get_height() // 2))

        # Bloquear botón finalizar si no hay nombre
        if self.step == 2 and not self.account_name.strip():
            overlay = pygame.Surface(self.next_rect.size, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 120))
            self.screen.blit(overlay, self.next_rect.topleft)
