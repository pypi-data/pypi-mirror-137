var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'ipyd3:plugin',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'ipyd3',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};


