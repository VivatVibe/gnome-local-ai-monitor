import { ExtensionPreferences, gettext as _ } from 'resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js';
import Adw from 'gi://Adw';
import Gio from 'gi://Gio';
import Gtk from 'gi://Gtk';

export default class LocalAiMonitorPreferences extends ExtensionPreferences {
  fillPreferencesWindow(window) {
    const settings = this.getSettings();

    const page = new Adw.PreferencesPage({
      title: _('Settings'),
      icon_name: 'preferences-other-symbolic',
    });

    // 1. Connection Group
    const connectionGroup = new Adw.PreferencesGroup({
      title: _('Connection'),
      description: _('Configure the local AI server connection.'),
    });
    page.add(connectionGroup);

    const endpointRow = new Adw.EntryRow({
      title: _('Ollama API Endpoint'),
    });
    settings.bind(
      'ollama-endpoint',
      endpointRow,
      'text',
      Gio.SettingsBindFlags.DEFAULT
    );
    connectionGroup.add(endpointRow);

    const intervalRow = new Adw.SpinRow({
      title: _('Refresh Interval (seconds)'),
      subtitle: _('Frequency of status and VRAM polling.'),
      adjustment: new Gtk.Adjustment({
        lower: 1,
        upper: 60,
        step_increment: 1,
        page_increment: 5,
      }),
    });
    settings.bind(
      'poll-interval',
      intervalRow,
      'value',
      Gio.SettingsBindFlags.DEFAULT
    );
    connectionGroup.add(intervalRow);

    // 2. Display Group
    const displayGroup = new Adw.PreferencesGroup({
      title: _('Top Panel Display'),
      description: _('Choose what indicators appear on the top bar.'),
    });
    page.add(displayGroup);

    const modelRow = new Adw.SwitchRow({
      title: _('Display Active Model Name'),
      subtitle: _('Show the name of the currently loaded model on the panel.'),
    });
    settings.bind(
      'show-model-name',
      modelRow,
      'active',
      Gio.SettingsBindFlags.DEFAULT
    );
    displayGroup.add(modelRow);

    const vramRow = new Adw.SwitchRow({
      title: _('Display GPU VRAM Percentage'),
      subtitle: _('Show the memory consumption percentage on the panel.'),
    });
    settings.bind(
      'show-gpu-vram',
      vramRow,
      'active',
      Gio.SettingsBindFlags.DEFAULT
    );
    displayGroup.add(vramRow);

    const animRow = new Adw.SwitchRow({
      title: _('Animate Running Alpaca'),
      subtitle: _('Animate the Ollama mascot running dynamically based on GPU load.'),
    });
    settings.bind(
      'enable-running-animation',
      animRow,
      'active',
      Gio.SettingsBindFlags.DEFAULT
    );
    displayGroup.add(animRow);

    window.add(page);
  }
}
