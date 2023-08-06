"use strict";

(function () {
  /**
   * A drawer containing actions that can be performed on selected objects.
   *
   * This displays any actions provided by the Django
   * :py:class:`~django.contrib.admin.ModelAdmin` class that can apply to
   * selected rows in the change list.
   */
  var ActionsDrawerView = RB.DrawerView.extend({
    template: _.template("<p class=\"rb-c-drawer__summary\"></p>\n<div class=\"rb-c-drawer__actions\">\n <ul class=\"rb-c-drawer__action-group\">\n  <% _.each(actions, function(actionInfo) { %>\n   <li class=\"rb-c-drawer__action js-action-<%- actionInfo.id %>\">\n    <strong><%- actionInfo.label %></strong>\n   </li>\n  <% }) %>\n </ul>\n</div>"),

    /**
     * Initialize the drawer.
     *
     * Args:
     *     options (object):
     *         Options for the drawer.
     *
     * Option Args:
     *     actions (Array of object):
     *         The actions to show in the drawer. Each is an object with the
     *         following keys:
     *
     *         ``id`` (:js:class:`string`):
     *             The action's identifier.
     *
     *         ``label`` (:js:class:`string`):
     *             The human-readable label.
     */
    initialize: function initialize(options) {
      this.actions = options.actions;
    },

    /**
     * Render the drawer.
     *
     * Returns:
     *     ActionsDrawerView:
     *     This instance, for chaining.
     */
    render: function render() {
      RB.DrawerView.prototype.render.call(this);
      this.$content.html(this.template({
        actions: this.actions
      }));
      this.$summary = this.$('.rb-c-drawer__summary');
      return this;
    }
  });
  /**
   * The view for the Administration UI's Change List page.
   *
   * This manages the dynamic state of the Change List page, which is used for
   * showing all entries for a model.
   *
   * This includes a drawer for the actions that can be performed on selected
   * entries (defined in :py:class:`~django.contrib.admin.ModelAdmin`), and
   * managing the selection state in general.
   */

  RB.Admin.ChangeListPageView = RB.Admin.PageView.extend({
    events: {
      'change #action-toggle': '_onToggleAllCheckboxesChanged',
      'change .action-select': '_onRowSelected'
    },

    /**
     * Initialize the page view.
     */
    initialize: function initialize() {
      RB.Admin.PageView.prototype.initialize.apply(this, arguments);
      this.drawerShown = false;
    },

    /**
     * Render the page contents.
     *
     * This should be implemented by subclasses that need to render any
     * UI elements.
     */
    renderPage: function renderPage() {
      var _this = this;

      RB.Admin.PageView.prototype.renderPage.call(this);
      var model = this.model;
      this._$changelist = this.$pageContent.children('.rb-c-admin-change-list');
      this._$form = this._$changelist.children('.rb-c-admin-change-list__form');
      this._$datagrid = this._$form.children('.rb-c-admin-change-list__results');
      this._datagrid = this._$datagrid.data('datagrid');
      this.setDrawer(new ActionsDrawerView({
        actions: model.get('actions')
      }));
      var modelNameLower = model.get('modelName').toLowerCase();
      var modelNameLowerPlural = model.get('modelNamePlural').toLowerCase();
      this.listenTo(model, 'change:selectionCount', function (model, count) {
        _this.drawer.$summary.text(interpolate(ngettext("%(count)s %(modelNameLower)s selected", "%(count)s %(modelNameLowerPlural)s selected", count), {
          "count": count,
          "modelNameLower": modelNameLower,
          "modelNameLowerPlural": modelNameLowerPlural
        }, true));

        var showDrawer = count > 0;

        if (showDrawer !== _this._drawerShown) {
          if (showDrawer) {
            _this.drawer.show();
          } else {
            _this.drawer.hide();
          }

          _this._drawerShown = showDrawer;
        }
      });
    },

    /**
     * Handle a page resize.
     *
     * This will lay out the elements to take the full height of the
     * page.
     */
    onResize: function onResize() {
      this.resizeElementForFullHeight(this._$changelist);
      this.resizeElementForFullHeight(this._$form);

      this._datagrid.resizeToFit();
    },

    /**
     * Handle a toggle on the checkbox in the datagrid header.
     *
     * This will toggle all rows' checkboxes to match the state of the
     * one in the header.
     *
     * Args:
     *     e (Event):
     *         The change event.
     */
    _onToggleAllCheckboxesChanged: function _onToggleAllCheckboxesChanged(e) {
      var $toggleCheckbox = $(e.target);

      this._$datagrid.find('.action-select').prop('checked', $toggleCheckbox.prop('checked')).change();
    },

    /**
     * Handle a toggle on a checkbox in a row.
     *
     * This will mark the row as selected or unselected, depending on the
     * state of the checkbox.
     *
     * Args:
     *     e (Event):
     *         The change event.
     */
    _onRowSelected: function _onRowSelected(e) {
      var $checkbox = $(e.target);
      var objectID = $checkbox.val();

      if ($checkbox.prop('checked')) {
        this.model.select(objectID);
      } else {
        this.model.unselect(objectID);
      }
    }
  });
})();

//# sourceMappingURL=changeListPageView.js.map