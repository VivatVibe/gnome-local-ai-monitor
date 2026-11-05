import { ExtensionPreferences, gettext as _ } from 'resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js';
import Adw from 'gi://Adw';
import Gio from 'gi://Gio';
import Gtk from 'gi://Gtk';
import {
  REFRESH_INTERVALS,
  getIndexForInterval,
  getIntervalForIndex,
} from './lib/preferencesHelper.js';

export {
  REFRESH_INTERVALS,
  getIndexForInterval,
  getIntervalForIndex,
};

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

    // Refresh Rate choices: 1s, 2s, 5s
    const refreshModel = new Gtk.StringList();
    refreshModel.append(_('1s (Fast - high responsiveness)'));
    refreshModel.append(_('2s (Normal - recommended)'));
    refreshModel.append(_('5s (Relaxed - low resource usage)'));

    const currentInterval = settings.get_int('poll-interval');
    const initialIndex = getIndexForInterval(currentInterval);

    const intervalRow = new Adw.ComboRow({
      title: _('Refresh Rate'),
      subtitle: _('Polling frequency for Ollama service status and GPU VRAM.'),
      model: refreshModel,
      selected: initialIndex,
    });

    intervalRow.connect('notify::selected', () => {
      const selectedValue = getIntervalForIndex(intervalRow.selected);
      if (settings.get_int('poll-interval') !== selectedValue) {
        settings.set_int('poll-interval', selectedValue);
      }
    });

    settings.connect('changed::poll-interval', () => {
      const updatedInterval = settings.get_int('poll-interval');
      const targetIndex = getIndexForInterval(updatedInterval);
      if (intervalRow.selected !== targetIndex) {
        intervalRow.selected = targetIndex;
      }
    });

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
      title: _('Animate GPU Card Fans'),
      subtitle: _('Animate the cooling fans dynamically based on GPU compute load.'),
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
