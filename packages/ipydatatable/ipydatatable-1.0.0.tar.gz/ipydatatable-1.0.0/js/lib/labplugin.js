var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'ipydatatable:plugin',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'ipydatatable',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

