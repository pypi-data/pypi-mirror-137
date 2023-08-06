"use strict";

/**
 * Models a generic datagrid.
 *
 * This will keep track of any selected objects, allowing subclasses to easily
 * perform operations on them.
 */
RB.DatagridPage = RB.Page.extend({
  defaults: _.defaults({
    count: 0,
    localSiteName: null
  }, RB.Page.prototype.defaults),

  /* The type of object each row represents, for use in batch selection. */
  rowObjectType: null,

  /**
   * Initialize the model.
   */
  initialize: function initialize() {
    var _this = this;

    this.selection = new Backbone.Collection([], {
      model: this.rowObjectType
    });
    this.listenTo(this.selection, 'add remove reset', function () {
      return _this.set('count', _this.selection.length);
    });
  },

  /**
   * Add a selected row to be used for any actions.
   *
   * Args:
   *     id (string):
   *         The ID of the selected row.
   */
  select: function select(id) {
    var localSiteName = this.get('localSiteName');
    this.selection.add({
      id: id,
      localSitePrefix: localSiteName ? "s/".concat(localSiteName, "/") : null
    });
  },

  /**
   * Remove a selected row.
   *
   * Args:
   *     id (string):
   *         The ID of the row to remove.
   */
  unselect: function unselect(id) {
    this.selection.remove(this.selection.get(id));
  },

  /**
   * Clear the list of selected rows.
   */
  clearSelection: function clearSelection() {
    this.selection.reset();
  }
});

//# sourceMappingURL=datagridPageModel.js.map