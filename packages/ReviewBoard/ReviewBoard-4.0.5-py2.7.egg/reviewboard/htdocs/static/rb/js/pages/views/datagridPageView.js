"use strict";

/**
 * Manages the UI for the page containing a main datagrid.
 *
 * This renders the datagrid, handles events, and allows for multi-row
 * actions.
 */
RB.DatagridPageView = RB.PageView.extend({
  RELOAD_INTERVAL_MS: 5 * 60 * 1000,

  /* The View class to use for an actions menu, if any. */
  actionsViewType: null,
  events: {
    'change tbody input[data-checkbox-name=select]': '_onRowSelected',
    'reloaded .datagrid-wrapper': '_setupDatagrid'
  },

  /**
   * Initialize the datagrid page.
   *
   * Args:
   *     options (object, optional):
   *         Options for the view.
   *
   * Option Args:
   *     periodicReload (boolean):
   *         Whether to periodically reload the contents of the datagrid.
   */
  initialize: function initialize() {
    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
    RB.PageView.prototype.initialize.call(this, options);
    this.periodicReload = !!options.periodicReload;
    this._reloadTimer = null;
    this._datagrid = null;
    this._$wrapper = null;
    this._$datagridBody = null;
    this._$datagridBodyContainer = null;
    this._menuShown = false;
  },

  /**
   * Render the datagrid page view, and begins listening for events.
   */
  renderPage: function renderPage() {
    var _this = this;

    RB.InfoboxManagerView.getInstance().setPositioning(RB.ReviewRequestInfoboxView, {
      /*
       * The order on the side matters. If the Summary column is
       * on the left-hand side of the datagrid, and "l" is first,
       * it can end up taking priority, even if "L" was a better
       * fit (since, if the infobox would need to be pushed a bit
       * to fit on screen, it will prefer "l"). If the column is on
       * the right-hand side of the dashboard, it will prefer "l",
       * given the room available (taking into account the sidebar).
       *
       * So "L" is a better priority for the common use, and "l"
       * works well as a fallback.
       */
      side: 'Ll',
      LDistance: 300,
      lDistance: 20,
      yOffset: -20
    });

    if (this.actionsViewType) {
      this._setupActionsDrawer();
    }

    this.listenTo(this.model, 'refresh', function () {
      return _this._reload(false);
    });

    this._setupDatagrid();

    if (this.periodicReload) {
      this._startReloadTimer();
    }

    return this;
  },

  /**
   * Handle page resizes.
   *
   * This will update the datagrid to fit on the page after a resize.
   */
  onResize: function onResize() {
    if (this._datagrid !== null) {
      this._datagrid.resizeToFit();
    }
  },

  /**
   * Set up the actions pane view.
   */
  _setupActionsDrawer: function _setupActionsDrawer() {
    var _this2 = this;

    var drawer = new RB.DrawerView();
    this.setDrawer(drawer);
    this._actionsView = new this.actionsViewType({
      model: this.model,
      datagridView: this
    });

    this._actionsView.render().$el.appendTo(drawer.$content);

    this.listenTo(this.model, 'change:count', function (model, count) {
      var showMenu = count > 0;

      if (showMenu === _this2._menuShown) {
        return;
      }

      if (showMenu) {
        _this2._showActions();
        /*
         * Don't reload the datagrid while the user is
         * preparing any actions.
         */


        _this2._stopReloadTimer();
      } else {
        _this2._hideActions();

        if (_this2.periodicReload) {
          _this2._startReloadTimer();
        }
      }

      _this2._menuShown = showMenu;
    });
  },

  /**
   * Set up parts of the datagrid.
   *
   * This will reference elements inside the datagrid and set up UI.
   * This is called when first rendering the datagrid, and any time
   * the datagrid is reloaded from the server.
   */
  _setupDatagrid: function _setupDatagrid() {
    var _this3 = this;

    this._$wrapper = this.$('#content_container');
    this._$datagrid = this._$wrapper.find('.datagrid-wrapper');
    this._datagrid = this._$datagrid.data('datagrid');
    this._$main = this._$wrapper.find('.datagrid-main');
    this.$('time.timesince').timesince();
    this.$('.user').user_infobox();
    this.$('.bugs').find('a').bug_infobox();
    this.$('.review-request-link').review_request_infobox();
    this.model.clearSelection();

    _.each(this.$('input[data-checkbox-name=select]:checked'), function (checkbox) {
      return _this3.model.select($(checkbox).data('object-id'));
    });

    if (RB.UserSession.instance.get('authenticated')) {
      this._starManager = new RB.StarManagerView({
        model: new RB.StarManager(),
        el: this._$main,
        datagridMode: true
      });
    }

    this._$datagrid.on('reloaded', this._setupDatagrid.bind(this)).on('datagridDisplayModeChanged', this._reselectBatchCheckboxes.bind(this));

    this._datagrid.resizeToFit();
  },

  /**
   * Re-select any checkboxes that are part of the current selection.
   *
   * When the datagrid transitions between mobile and desktop modes,
   * we use two different versions of the table, meaning two sets of
   * checkboxes. This function updates the checkbox selection based on the
   * currently selected items.
   */
  _reselectBatchCheckboxes: function _reselectBatchCheckboxes() {
    var checkboxMap = {};
    this.$('input[data-checkbox-name=select]').each(function (idx, checkboxEl) {
      if (checkboxEl.checked) {
        checkboxEl.checked = false;
      }

      checkboxMap[checkboxEl.dataset.objectId] = checkboxEl;
    });
    this.model.selection.each(function (selection) {
      checkboxMap[selection.id].checked = true;
    });
  },

  /**
   * Show the actions drawer.
   */
  _showActions: function _showActions() {
    this.drawer.show();
  },

  /**
   * Hide the actions drawer.
   */
  _hideActions: function _hideActions() {
    this.drawer.hide();
  },

  /**
   * Start the reload timer, if it's not already running.
   */
  _startReloadTimer: function _startReloadTimer() {
    if (!this._reloadTimer) {
      this._reloadTimer = setInterval(this._reload.bind(this), this.RELOAD_INTERVAL_MS);
    }
  },

  /**
   * Stop the reload timer, if it's running.
   */
  _stopReloadTimer: function _stopReloadTimer() {
    if (this._reloadTimer) {
      window.clearInterval(this._reloadTimer);
      this._reloadTimer = null;
    }
  },

  /**
   * Reload the datagrid contents.
   *
   * This may be called periodically to reload the contents of the
   * datagrid, if specified by the subclass.
   *
   * Args:
   *     periodicReload (boolean):
   *         Whether the datagrid should reload periodically.
   */
  _reload: function _reload(periodicReload) {
    var _this4 = this;

    var $editCols = this.$('.edit-columns');

    if (periodicReload === false) {
      this._stopReloadTimer();
    }

    this.model.clearSelection();
    $editCols.width($editCols.width() - $editCols.getExtents('b', 'lr')).html('<span class="fa fa-spinner fa-pulse"></span>');

    this._$wrapper.load(window.location + ' #content_container', function () {
      _this4.$('.datagrid-wrapper').datagrid();

      _this4._setupDatagrid();

      if (periodicReload !== false) {
        _this4._startReloadTimer();
      }
    });
  },

  /**
   * Handler for when a row is selected.
   *
   * Records the row for any actions the user may wish to invoke.
   *
   * Args:
   *     e (Event):
   *         The event that triggered the callback.
   */
  _onRowSelected: function _onRowSelected(e) {
    var $checkbox = $(e.target);
    var objectID = $checkbox.data('object-id');

    if ($checkbox.prop('checked')) {
      this.model.select(objectID);
    } else {
      this.model.unselect(objectID);
    }
  }
});

//# sourceMappingURL=datagridPageView.js.map