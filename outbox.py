#!/usr/bin/env python3
"""Outbox — the desktop viewer. Renders ARRIVE here as images/video, not links.
Watches the output folders; grid of live thumbnails; double-click = in-app
image view or embedded vlc playback; new files badge + window pops up."""
import gi, os, sys, subprocess, hashlib, time, shutil
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GdkX11", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GLib, GdkX11

FOLDERS = ["/home/box/visuals/experiments", "/home/box/visuals/pilots"]
THUMB_DIR = "/tmp/outbox_thumbs"
os.makedirs(THUMB_DIR, exist_ok=True)
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
VID_EXT = {".mp4", ".webm", ".mov", ".mkv"}
AUD_EXT = {".wav", ".mp3", ".flac", ".m4a", ".ogg"}
EXTS = IMG_EXT | VID_EXT | AUD_EXT | {".md", ".txt", ".json", ".py", ".sh", ".log"}
POP_ON_NEW = True


def thumb_for(path):
    """cached thumbnail; extract video frames with ffmpeg in background callers"""
    h = hashlib.md5(path.encode()).hexdigest()[:16] + ".jpg"
    tp = os.path.join(THUMB_DIR, h)
    if not os.path.exists(tp):
        ext = os.path.splitext(path)[1].lower()
        if ext in IMG_EXT:
            try:
                pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, 320, 200, True)
                pb.savev(tp, "jpeg", [], [])
            except Exception:
                return None
        elif ext in VID_EXT:
            r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.8", "-i", path,
                                "-frames:v", "1", "-vf", "scale=320:-2", tp],
                               capture_output=True, timeout=20)
            if r.returncode != 0:
                return None
        else:
            return None
    try:
        return GdkPixbuf.Pixbuf.new_from_file_at_scale(tp, 320, 200, True)
    except Exception:
        return None


def kind_of(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in IMG_EXT: return "image"
    if ext in VID_EXT: return "video"
    if ext in AUD_EXT: return "audio"
    return "text"


class Outbox(Gtk.Window):
    def __init__(self):
        super().__init__(title="Outbox")
        self.set_default_size(1180, 760)
        self.set_icon_name("multimedia-video-player")
        self.files = {}       # path -> (mtime, size)
        self.seen = set()
        self.vlc = None
        self.thumb_queue = []

        header = Gtk.HeaderBar(title="Outbox", subtitle="renders arrive here")
        header.set_show_close_button(True)
        btn_folder = Gtk.Button.new_from_icon_name("folder-open-symbolic", Gtk.IconSize.BUTTON)
        btn_folder.connect("clicked", lambda *_: subprocess.Popen(["xdg-open", FOLDERS[0]]))
        header.pack_start(btn_folder)
        self.pop_toggle = Gtk.ToggleButton(label="pop on new")
        self.pop_toggle.set_active(True)
        self.pop_toggle.connect("toggled", self._pop_toggled)
        header.pack_end(self.pop_toggle)
        self.set_titlebar(header)

        self.stack = Gtk.Stack(transition_type=Gtk.StackTransitionType.CROSSFADE)
        # --- grid page
        self.store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str, str, float, bool)  # thumb,name,path,kind,mtime,is_new
        self.store.set_sort_column_id(4, Gtk.SortType.DESCENDING)
        self.iconview = Gtk.IconView(model=self.store)
        self.iconview.set_pixbuf_column(0)
        self.iconview.set_text_column(1)
        self.iconview.set_item_width(200)
        self.iconview.set_activate_on_single_click(False)
        self.iconview.connect("item-activated", self._open_item)
        self.iconview.connect("button-press-event", self._ctx)
        grid_scroll = Gtk.ScrolledWindow()
        grid_scroll.add(self.iconview)
        # --- detail page
        self.detail_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        dbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        dbar.set_margin_top(6); dbar.set_margin_bottom(6)
        dbar.set_margin_start(8); dbar.set_margin_end(8)
        back = Gtk.Button.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.BUTTON)
        back.connect("clicked", lambda *_: (self.stop_play(), self.stack.set_visible_child_name("grid")))
        self.detail_title = Gtk.Label(xalign=0, ellipsize=3)
        self.detail_meta = Gtk.Label(xalign=0)
        self.detail_meta.get_style_context().add_class("dim-label")
        dbar.pack_start(back, False, False, 0)
        dbar.pack_start(self.detail_title, True, True, 0)
        dbar.pack_end(self.detail_meta, False, False, 0)
        self.detail_stack = Gtk.Stack()
        dbar_wrapper = dbar
        self.detail_box.pack_start(dbar_wrapper, False, False, 0)
        self.detail_box.pack_start(self.detail_stack, True, True, 0)
        self.image_view = Gtk.Image()
        self.socket = Gtk.Socket()
        self.socket.add_events(Gdk.EventMask.STRUCTURE_MASK)
        self.text_view = Gtk.TextView(editable=False, cursor_visible=False, monospace=True)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        text_scroll = Gtk.ScrolledWindow(); text_scroll.add(self.text_view)
        self.audio_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        self.audio_box.set_valign(Gtk.Align.CENTER); self.audio_box.set_halign(Gtk.Align.CENTER)
        self.audio_icon = Gtk.Image.new_from_icon_name("audio-x-generic-symbolic", Gtk.IconSize.DIALOG)
        self.audio_lbl = Gtk.Label()
        self.audio_box.pack_start(self.audio_icon, False, False, 0)
        self.audio_box.pack_start(self.audio_lbl, False, False, 0)
        btn_open_ext = Gtk.Button(label="open in VLC window")
        btn_open_ext.connect("clicked", self._open_external)
        self.audio_box.pack_start(btn_open_ext, False, False, 8)
        self.detail_stack.add_named(self.image_view, "image")
        self.detail_stack.add_named(self.socket, "video")
        self.detail_stack.add_named(text_scroll, "text")
        self.detail_stack.add_named(self.audio_box, "audio")

        self.stack.add_named(grid_scroll, "grid")
        self.stack.add_named(self.detail_box, "detail")
        self.add(self.stack)
        self.connect("destroy", lambda *_: (self.stop_play(), Gtk.main_quit()))

        self.monitors = []
        for folder in FOLDERS:
            gfile = Gio.File.new_for_path(folder)
            m = gfile.monitor_directory(Gio.FileMonitorFlags.NONE, None)
            m.connect("changed", self._on_dir_changed)
            self.monitors.append(m)
            self._scan(folder)

        self.connect("key-press-event", self._keys)
        GLib.timeout_add_seconds(1, self._drain_thumbs)
        self.show_all()
        self.stack.set_visible_child_name("grid")

    def _pop_toggled(self, btn):
        global POP_ON_NEW
        POP_ON_NEW = btn.get_active()

    def _scan(self, folder):
        try:
            for e in sorted(os.scandir(folder), key=lambda x: x.stat().st_mtime, reverse=True):
                if e.is_file() and os.path.splitext(e.name)[1].lower() in EXTS:
                    self._add(e.path, new=False)
        except FileNotFoundError:
            pass

    def _add(self, path, new=True):
        try:
            st = os.stat(path)
        except OSError:
            return
        if path in self.files:
            if self.files[path][0] == st.st_mtime:
                return
        self.files[path] = (st.st_mtime, st.st_size)
        if path not in self.seen and new:
            kind = kind_of(path)
            self.store.append([None, os.path.basename(path), path, kind, st.st_mtime, True])
            self.thumb_queue.append(path)
            if POP_ON_NEW:
                self.deiconify()
                self.present()
                self.set_urgency_hint(True)
        else:
            for row in self.store:
                if row[2] == path:
                    row[4] = st.st_mtime
                    break
            else:
                self.store.append([None, os.path.basename(path), path, kind_of(path), st.st_mtime, False])
                self.thumb_queue.append(path)

    def _drain_thumbs(self):
        done = 0
        while self.thumb_queue and done < 3:
            path = self.thumb_queue.pop(0)
            pb = thumb_for(path)
            if pb:
                for row in self.store:
                    if row[2] == path and row[0] is None:
                        row[0] = pb
                        break
            done += 1
        return True

    def _on_dir_changed(self, monitor, gfile, other_file, event_type):
        path = gfile.get_path()
        if not path or os.path.splitext(path)[1].lower() not in EXTS:
            return
        if event_type in (Gio.FileMonitorEvent.CHANGED, Gio.FileMonitorEvent.CREATED,
                          Gio.FileMonitorEvent.MOVED_IN):
            if os.path.exists(path):
                GLib.idle_add(self._add, path, True)

    def _open_item(self, _view, path):
        self.show_file(path)

    def show_file(self, path):
        kind = kind_of(path)
        name = os.path.basename(path)
        st = os.stat(path)
        self.current_path = path
        self.pending_video = path if kind == "video" else None
        self.pending_audio = path if kind == "audio" else None
        self.detail_title.set_text(name)
        self.detail_meta.set_text(f"{st.st_size//1024} KB  ·  {time.strftime('%H:%M:%S', time.localtime(st.st_mtime))}  ·  {kind}")
        for row in self.store:
            if row[2] == path:
                row[5] = False
                break
        self.stop_play()
        if kind == "image":
            try:
                self.image_view.set_from_file(path)
                self.image_view.set_halign(Gtk.Align.CENTER); self.image_view.set_valign(Gtk.Align.CENTER)
            except Exception as e:
                self.image_view.set_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
            self.detail_stack.set_visible_child_name("image")
        elif kind == "video":
            self.pending_video = path
            self.detail_stack.set_visible_child_name("video")
            self.socket.reset()
            GLib.timeout_add(250, self._spawn_vlc)
        elif kind == "audio":
            self.audio_lbl.set_text(name)
            self.detail_stack.set_visible_child_name("audio")
        else:
            try:
                with open(path, "r", errors="replace") as f:
                    self.text_view.get_buffer().set_text(f.read(400_000))
            except Exception:
                self.text_view.get_buffer().set_text("(binary)")
            self.detail_stack.set_visible_child_name("text")
        self.stack.set_visible_child_name("detail")

    def _socket_realized(self, *_):
        pass

    def _spawn_vlc(self):
        path = getattr(self, "pending_video", None)
        if not path or self.stack.get_visible_child_name() != "video":
            return False
        self.stop_play()
        try:
            xid = self.socket.get_id()
        except Exception:
            xid = None
        cmd = ["vlc", "--no-video-title-show", "--play-and-exit", "--quiet",
               "--no-repeat", "--no-loop"]
        if xid:
            cmd += [f"--wid={xid}"]
        cmd.append(path)
        try:
            self.vlc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            subprocess.Popen(["xdg-open", path])
        return False

    def _open_external(self, *_):
        p = self.pending_audio or self.current_path
        if p:
            subprocess.Popen(["vlc", p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop_play(self):
        if self.vlc and self.vlc.poll() is None:
            self.vlc.terminate()
            try:
                self.vlc.wait(timeout=2)
            except Exception:
                self.vlc.kill()
        self.vlc = None

    def _ctx(self, view, event):
        if event.button != 3:
            return False
        path = view.get_path_at_pos(int(event.x), int(event.y))
        if not path:
            return False
        it = self.store.get_iter(path)
        fpath = self.store.get_value(it, 2)
        menu = Gtk.Menu()
        for label, fn in [
            ("open externally (vlc/xdg)", lambda: subprocess.Popen(["xdg-open", fpath])),
            ("copy path", lambda: Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).set_text(fpath, -1)),
            ("show folder", lambda: subprocess.Popen(["xdg-open", os.path.dirname(fpath)])),
        ]:
            item = Gtk.MenuItem(label=label)
            item.connect("activate", lambda _i, f=fn: f())
            menu.append(item)
        menu.show_all()
        menu.popup_at_pointer(event)
        return True

    def _keys(self, _w, event):
        from gi.repository import Gdk as _G
        if event.keyval == _G.KEY_Escape:
            self.stop_play()
            self.stack.set_visible_child_name("grid")
        return False


if __name__ == "__main__":
    Outbox()
    Gtk.main()
